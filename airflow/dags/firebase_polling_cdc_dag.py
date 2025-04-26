from __future__ import annotations

import pendulum
import json
import logging
import base64
from datetime import datetime as dt # Alias datetime to avoid conflict
from datetime import timedelta

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.firebase.hooks.firestore import CloudFirestoreHook
from airflow.exceptions import AirflowSkipException
from airflow.models import Variable
from google.cloud.firestore_v1.base_query import FieldFilter # Correct import for FieldFilter
from google.cloud import firestore
from google.oauth2 import service_account

# --- Configuration --- 
# Replace with your actual GCP Project ID
PROJECT_ID = "centrahealth-8f543" 
# Airflow Connection ID for Google Cloud (created in Airflow UI)
GCP_CONN_ID = "google_cloud_default" 

# Source Firestore Collections
HOSPITAL1_COLLECTION = "hospital1_patients"
HOSPITAL2_COLLECTION = "hospital2_patients"
# Target Firestore Collection
CENTRAL_COLLECTION = "central_patients"
# Timestamp field name used in source collections for polling
# IMPORTANT: Ensure this field exists and is updated consistently in source documents
# Based on populate_firestore.py, hospital1 uses 'LastUpdateTimestamp' and hospital2 uses 'LastModifiedDate'.
# We should ideally make these consistent, but for now, we can handle differently or assume one.
# Let's assume we query based on 'LastUpdateTimestamp' for H1 and 'LastModifiedDate' for H2.
HOSPITAL1_TS_FIELD = "LastUpdateTimestamp"
HOSPITAL2_TS_FIELD = "LastModifiedDate"

# Airflow Variable names to store the last successful sync timestamp for each source
HOSPITAL1_SYNC_VAR = "hospital1_last_sync_timestamp"
HOSPITAL2_SYNC_VAR = "hospital2_last_sync_timestamp"

# --- Transformation Logic (Mostly reused from previous DAG) --- 
def parse_firestore_timestamp(ts_object) -> dt | None:
    """Safely parses Firestore Timestamp object or ISO string."""
    if not ts_object:
        return None
    try:
        # If it's already a datetime object (e.g., from Firestore hook)
        if isinstance(ts_object, dt):
            # Ensure it's timezone-aware (assume UTC if naive)
            if ts_object.tzinfo is None:
                return ts_object.replace(tzinfo=pendulum.timezone("UTC"))
            return ts_object
        # Handle ISO strings (might come from specific SDK versions or manual entry)
        elif isinstance(ts_object, str):
             return pendulum.parse(ts_object)
        # Handle Firestore Timestamp specific types if CloudFirestoreHook returns them directly
        # This might depend on the hook version
        elif hasattr(ts_object, 'isoformat'): # Duck-typing for Firestore Timestamp
            return pendulum.parse(ts_object.isoformat())
    except Exception as e:
        logging.warning(f"Could not parse timestamp object/string: {ts_object} - Error: {e}")
    return None

def transform_hospital_data(source: str, raw_data: dict, event_timestamp: dt | None) -> dict | None:
    """Transforms raw hospital data from Firestore document into the central schema."""
    if not raw_data:
        logging.warning(f"Received empty data from {source}.")
        return None

    cnic = raw_data.get("CNIC") 
    if not cnic:
        logging.error(f"Missing CNIC in data from {source}: {raw_data}")
        return None

    # Create a visit record for this hospital visit
    visit_record = {
        "hospital": source,
        "timestamp": parse_firestore_timestamp(event_timestamp),
        "status": "Admitted",
        "diagnosis": None,
        "location": None,
        "medical_alerts": [],
        "physician": None,
        "admission_date": None,
        "discharge_date": None
    }

    if source == "hospital1":
        visit_record.update({
            "patient_id": raw_data.get("P_ID"),
            "diagnosis": raw_data.get("PrimaryDiagnosis"),
            "location": raw_data.get("ActiveWard"),
            "medical_alerts": raw_data.get("MedicalAlerts", []),
            "admission_date": parse_firestore_timestamp(raw_data.get("AdmissionTimestamp")),
            "discharge_date": parse_firestore_timestamp(raw_data.get("DischargeTimestamp")),
            "status": "Discharged" if raw_data.get("IsDischarged", False) else "Admitted"
        })
    else:  # hospital2
        visit_record.update({
            "patient_id": raw_data.get("PT_ID"),
            "diagnosis": raw_data.get("PrimaryDiagnosis"),  # Make sure this field exists in Hospital 2 data
            "location": raw_data.get("CurrentRoom"),
            "medical_alerts": raw_data.get("MedicalAlerts", []),
            "physician": raw_data.get("AttendingPhysicianID"),
            "admission_date": parse_firestore_timestamp(raw_data.get("RegistrationDate")),
            "status": raw_data.get("PatientStatus", "Admitted")
        })

        # Log the diagnosis field for debugging
        logging.info(f"Hospital 2 diagnosis for CNIC {cnic}: {raw_data.get('PrimaryDiagnosis')}")
        logging.info(f"Raw data from Hospital 2: {raw_data}")  # Add this line for debugging

    central_data = {
        "CNIC": cnic,
        "FirstName": raw_data.get("FirstName") or raw_data.get("FullName", "").split()[0],
        "LastName": raw_data.get("LastName") or " ".join(raw_data.get("FullName", "").split()[1:]),
        "FullName": raw_data.get("FullName") or f"{raw_data.get('FirstName', '')} {raw_data.get('LastName', '')}".strip(),
        "DateOfBirth": parse_firestore_timestamp(raw_data.get("DateOfBirth")) or parse_firestore_timestamp(raw_data.get("DOB")),
        "Gender": raw_data.get("Gender") or {"M": "Male", "F": "Female"}.get(raw_data.get("Sex"), raw_data.get("Sex")),
        "ContactNumber": raw_data.get("ContactNumber") or raw_data.get("PhoneNumber"),
        "Address": raw_data.get("Address") or raw_data.get("FullAddress"),
        "visits": [visit_record],  # Initialize with current visit
        "last_updated": pendulum.now('UTC')
    }

    return central_data

# --- Airflow Task Functions --- 

def get_last_sync_time(sync_variable_name: str) -> str:
    """Gets the last sync timestamp from Airflow Variables, defaults to epoch.
       Returns timestamp as ISO 8601 string.
    """
    # Default to epoch timestamp if variable doesn't exist
    default_epoch_ts = pendulum.datetime(1970, 1, 1, tz='UTC').isoformat()
    try:
        last_sync_ts_str = Variable.get(sync_variable_name, default_var=default_epoch_ts)
        # Validate it's a parseable timestamp string
        pendulum.parse(last_sync_ts_str)
        logging.info(f"Retrieved last sync time for {sync_variable_name}: {last_sync_ts_str}")
        return last_sync_ts_str
    except Exception as e:
        logging.warning(f"Could not get or parse Airflow Variable '{sync_variable_name}'. Defaulting to epoch. Error: {e}")
        # Set the variable to default if it was invalid or missing
        Variable.set(sync_variable_name, default_epoch_ts)
        return default_epoch_ts

def process_firestore_changes(hospital_id, source_collection, timestamp_field, target_collection, **context):
    try:
        logging.info(f"Starting to process documents for hospital {hospital_id}")
        
        # Initialize Firestore client with explicit credentials
        credentials = service_account.Credentials.from_service_account_file(
            '/opt/airflow/dags/keys/service-account-key.json'
        )
        db = firestore.Client(
            project=PROJECT_ID,
            credentials=credentials
        )
        
        # Get references to collections
        source_ref = db.collection(source_collection)
        target_ref = db.collection(target_collection)
        
        # Get all documents from source collection
        docs = list(source_ref.stream())
        logging.info(f"Found {len(docs)} documents in {source_collection}")
        
        # Process each document
        processed_count = 0
        for doc in docs:
            try:
                doc_data = doc.to_dict()
                logging.info(f"Processing document {doc.id} with fields: {list(doc_data.keys())}")
                
                # Transform the data
                transformed_data = transform_hospital_data(hospital_id, doc_data, doc_data.get(timestamp_field))
                
                if transformed_data:
                    # Get existing document if it exists
                    target_doc = target_ref.document(doc.id)
                    target_snapshot = target_doc.get()
                    existing_data = target_snapshot.to_dict() if target_snapshot.exists else {}
                    
                    # Merge the data
                    if existing_data:
                        # Preserve existing visits
                        existing_visits = existing_data.get("visits", [])
                        current_visit = transformed_data["visits"][0]
                        
                        # Log the current visit data for debugging
                        logging.info(f"Current visit data for {doc.id}: {current_visit}")
                        
                        # Check if this visit already exists
                        visit_exists = False
                        for i, visit in enumerate(existing_visits):
                            if (visit["hospital"] == current_visit["hospital"] and 
                                visit["admission_date"] == current_visit["admission_date"]):
                                # Update existing visit with new data, preserving non-None values
                                for key, value in current_visit.items():
                                    if value is not None:  # Only update if the new value is not None
                                        visit[key] = value
                                        logging.info(f"Updated {key} to {value} for visit in {doc.id}")
                                visit_exists = True
                                # Remove any duplicate visits with the same hospital and admission date
                                existing_visits = [v for j, v in enumerate(existing_visits) if j == i or 
                                                not (v["hospital"] == visit["hospital"] and 
                                                     v["admission_date"] == visit["admission_date"])]
                                break
                        
                        if not visit_exists:
                            # Log the new visit being added
                            logging.info(f"Adding new visit for {doc.id}: {current_visit}")
                            existing_visits.append(current_visit)
                        
                        # Sort visits by admission date
                        existing_visits.sort(key=lambda x: x["admission_date"] if x["admission_date"] else pendulum.datetime(1970, 1, 1))
                        
                        transformed_data["visits"] = existing_visits
                        
                        # Preserve other fields if they don't exist in new data
                        for key, value in existing_data.items():
                            if key not in transformed_data and key != "visits":
                                transformed_data[key] = value
                    
                    # Log the final transformed data
                    logging.info(f"Final transformed data for {doc.id}: {transformed_data}")
                    
                    # Add to target collection
                    target_doc.set(transformed_data)
                    processed_count += 1
                    logging.info(f"Successfully processed document {doc.id} from {source_collection}")
                else:
                    logging.warning(f"Skipped document {doc.id} due to transformation failure")
                    
            except Exception as e:
                logging.error(f"Error processing document {doc.id}: {str(e)}")
                continue
        
        logging.info(f"Successfully processed {processed_count} documents from {source_collection} to {target_collection}")
        
        # Update the last sync time to current time
        current_time = pendulum.now('UTC').isoformat()
        Variable.set(f"{hospital_id}_last_sync_timestamp", current_time)
        logging.info(f"Updated last sync time for {hospital_id} to {current_time}")
        
    except Exception as e:
        logging.error(f"Error in process_firestore_changes for hospital {hospital_id}: {str(e)}")
        raise

def update_last_sync_time(sync_variable_name: str, **context):
    """Updates the Airflow Variable with the latest processed timestamp from XComs."""
    # Determine which task's XCom to pull based on the variable name
    source_task_id = "process_hospital1_changes" if sync_variable_name == HOSPITAL1_SYNC_VAR else "process_hospital2_changes"
    
    latest_processed_ts_str = context["ti"].xcom_pull(task_ids=source_task_id)
    
    if latest_processed_ts_str:
        try:
            # Validate timestamp before setting
            pendulum.parse(latest_processed_ts_str)
            Variable.set(sync_variable_name, latest_processed_ts_str)
            logging.info(f"Updated Airflow Variable {sync_variable_name} to {latest_processed_ts_str}")
        except Exception as e:
            logging.error(f"Failed to update Airflow Variable {sync_variable_name} with value {latest_processed_ts_str}. Error: {e}")
            # Optionally fail the task if update fails
            # raise e 
    else:
        logging.warning(f"No timestamp pushed from task {source_task_id} for variable {sync_variable_name}. Variable not updated.")


# --- DAG Definition --- 
with DAG(
    dag_id="firebase_polling_cdc_dag",
    start_date=pendulum.datetime(2023, 10, 26, tz="UTC"), 
    schedule="*/5 * * * *", # Run every 5 minutes using cron format
    catchup=False,
    tags=["firebase", "cdc", "firestore", "polling"],
    default_args={
        'owner': 'airflow',
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
        'gcp_conn_id': GCP_CONN_ID 
    }
) as dag:

    # --- Tasks for Hospital 1 --- 
    process_h1 = PythonOperator(
        task_id="process_hospital1_changes",
        python_callable=process_firestore_changes,
        op_kwargs={
            "hospital_id": "hospital1",
            "source_collection": HOSPITAL1_COLLECTION, 
            "timestamp_field": HOSPITAL1_TS_FIELD, 
            "target_collection": CENTRAL_COLLECTION
        }
    )

    update_h1_sync_time = PythonOperator(
        task_id="update_hospital1_sync_time",
        python_callable=update_last_sync_time,
        op_kwargs={"sync_variable_name": HOSPITAL1_SYNC_VAR}
    )

    # --- Tasks for Hospital 2 --- 
    process_h2 = PythonOperator(
        task_id="process_hospital2_changes",
        python_callable=process_firestore_changes,
        op_kwargs={
            "hospital_id": "hospital2",
            "source_collection": HOSPITAL2_COLLECTION, 
            "timestamp_field": HOSPITAL2_TS_FIELD, 
            "target_collection": CENTRAL_COLLECTION
        }
    )

    update_h2_sync_time = PythonOperator(
        task_id="update_hospital2_sync_time",
        python_callable=update_last_sync_time,
        op_kwargs={"sync_variable_name": HOSPITAL2_SYNC_VAR}
    )

    # Define task dependencies (Process H1 and H2 in parallel, then update sync times)
    process_h1 >> update_h1_sync_time
    process_h2 >> update_h2_sync_time 