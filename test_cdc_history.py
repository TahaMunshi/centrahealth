import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timezone
import time

# Initialize Firebase Admin SDK
cred = credentials.Certificate('./centrahealth-8f543-firebase-adminsdk-fbsvc-5b82bee7cc.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def print_patient_details(doc):
    data = doc.to_dict()
    print(f"\nCNIC: {doc.id}")
    print(f"Full Name: {data.get('FullName', 'N/A')}")
    print(f"Date of Birth: {data.get('DateOfBirth', 'N/A')}")
    print(f"Gender: {data.get('Gender', 'N/A')}")
    print(f"Contact: {data.get('ContactNumber', 'N/A')}")
    print(f"Address: {data.get('Address', 'N/A')}")
    
    print("\nVisit History:")
    visits = data.get('visits', [])
    for i, visit in enumerate(visits, 1):
        print(f"\nVisit {i}:")
        print(f"  Hospital: {visit.get('hospital', 'N/A')}")
        print(f"  Status: {visit.get('status', 'N/A')}")
        print(f"  Diagnosis: {visit.get('diagnosis', 'N/A')}")
        print(f"  Location: {visit.get('location', 'N/A')}")
        print(f"  Medical Alerts: {visit.get('medical_alerts', 'N/A')}")
        print(f"  Admission Date: {visit.get('admission_date', 'N/A')}")
        print(f"  Discharge Date: {visit.get('discharge_date', 'N/A')}")
    print("-" * 50)

def add_test_patients():
    # Hospital 1 Pakistani Patients
    h1_patients = [
        {
            "CNIC": "42301-1234567-1",
            "P_ID": "H1-00001",
            "FirstName": "Ahmed",
            "LastName": "Khan",
            "DateOfBirth": datetime(1985, 3, 15, tzinfo=timezone.utc),
            "Gender": "Male",
            "ContactNumber": "+92-300-1234567",
            "Address": {"Street": "House 123, Street 5", "City": "Lahore", "Province": "Punjab"},
            "AdmissionTimestamp": datetime(2024, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
            "LastUpdateTimestamp": firestore.SERVER_TIMESTAMP,
            "ActiveWard": "Cardiology-B",
            "PrimaryDiagnosis": "Hypertension",
            "IsDischarged": False,
            "MedicalAlerts": ["Diabetes Type 2"]
        },
        {
            "CNIC": "42301-2345678-2",
            "P_ID": "H1-00002",
            "FirstName": "Fatima",
            "LastName": "Ali",
            "DateOfBirth": datetime(1990, 6, 20, tzinfo=timezone.utc),
            "Gender": "Female",
            "ContactNumber": "+92-300-2345678",
            "Address": {"Street": "House 456, Street 8", "City": "Karachi", "Province": "Sindh"},
            "AdmissionTimestamp": datetime(2024, 2, 1, 14, 0, 0, tzinfo=timezone.utc),
            "LastUpdateTimestamp": firestore.SERVER_TIMESTAMP,
            "ActiveWard": "Orthopedics-1",
            "PrimaryDiagnosis": "Fractured Femur",
            "IsDischarged": False,
            "MedicalAlerts": ["Osteoporosis"]
        },
        {
            "CNIC": "42301-3456789-3",
            "P_ID": "H1-00003",
            "FirstName": "Usman",
            "LastName": "Malik",
            "DateOfBirth": datetime(1978, 9, 5, tzinfo=timezone.utc),
            "Gender": "Male",
            "ContactNumber": "+92-300-3456789",
            "Address": {"Street": "House 789, Street 12", "City": "Islamabad", "Province": "ICT"},
            "AdmissionTimestamp": datetime(2024, 2, 10, 9, 0, 0, tzinfo=timezone.utc),
            "LastUpdateTimestamp": firestore.SERVER_TIMESTAMP,
            "ActiveWard": "Neurology-2",
            "PrimaryDiagnosis": "Migraine",
            "IsDischarged": False,
            "MedicalAlerts": ["History of Stroke"]
        },
        {
            "CNIC": "42301-4567890-4",
            "P_ID": "H1-00004",
            "FirstName": "Ayesha",
            "LastName": "Raza",
            "DateOfBirth": datetime(1995, 12, 25, tzinfo=timezone.utc),
            "Gender": "Female",
            "ContactNumber": "+92-300-4567890",
            "Address": {"Street": "House 101, Street 3", "City": "Peshawar", "Province": "KPK"},
            "AdmissionTimestamp": datetime(2024, 2, 15, 11, 0, 0, tzinfo=timezone.utc),
            "LastUpdateTimestamp": firestore.SERVER_TIMESTAMP,
            "ActiveWard": "Oncology-1",
            "PrimaryDiagnosis": "Breast Cancer",
            "IsDischarged": False,
            "MedicalAlerts": ["Family History of Cancer"]
        },
        {
            "CNIC": "42301-5678901-5",
            "P_ID": "H1-00005",
            "FirstName": "Bilal",
            "LastName": "Hussain",
            "DateOfBirth": datetime(1982, 4, 10, tzinfo=timezone.utc),
            "Gender": "Male",
            "ContactNumber": "+92-300-5678901",
            "Address": {"Street": "House 202, Street 7", "City": "Quetta", "Province": "Balochistan"},
            "AdmissionTimestamp": datetime(2024, 2, 20, 15, 0, 0, tzinfo=timezone.utc),
            "LastUpdateTimestamp": firestore.SERVER_TIMESTAMP,
            "ActiveWard": "Gastroenterology-1",
            "PrimaryDiagnosis": "Peptic Ulcer",
            "IsDischarged": False,
            "MedicalAlerts": ["H. Pylori Positive"]
        },
        {
            "CNIC": "42301-6789012-6",
            "P_ID": "H1-00006",
            "FirstName": "Sana",
            "LastName": "Iqbal",
            "DateOfBirth": datetime(1992, 7, 30, tzinfo=timezone.utc),
            "Gender": "Female",
            "ContactNumber": "+92-300-6789012",
            "Address": {"Street": "House 303, Street 9", "City": "Faisalabad", "Province": "Punjab"},
            "AdmissionTimestamp": datetime(2024, 2, 25, 10, 0, 0, tzinfo=timezone.utc),
            "LastUpdateTimestamp": firestore.SERVER_TIMESTAMP,
            "ActiveWard": "Pediatrics-A",
            "PrimaryDiagnosis": "Pneumonia",
            "IsDischarged": False,
            "MedicalAlerts": ["Asthma"]
        },
        {
            "CNIC": "42301-7890123-7",
            "P_ID": "H1-00007",
            "FirstName": "Zain",
            "LastName": "Abbas",
            "DateOfBirth": datetime(1988, 11, 15, tzinfo=timezone.utc),
            "Gender": "Male",
            "ContactNumber": "+92-300-7890123",
            "Address": {"Street": "House 404, Street 11", "City": "Multan", "Province": "Punjab"},
            "AdmissionTimestamp": datetime(2024, 3, 1, 14, 0, 0, tzinfo=timezone.utc),
            "LastUpdateTimestamp": firestore.SERVER_TIMESTAMP,
            "ActiveWard": "Dermatology-1",
            "PrimaryDiagnosis": "Psoriasis",
            "IsDischarged": False,
            "MedicalAlerts": ["Autoimmune Disorder"]
        },
        {
            "CNIC": "42301-8901234-8",
            "P_ID": "H1-00008",
            "FirstName": "Hina",
            "LastName": "Shah",
            "DateOfBirth": datetime(1993, 2, 28, tzinfo=timezone.utc),
            "Gender": "Female",
            "ContactNumber": "+92-300-8901234",
            "Address": {"Street": "House 505, Street 13", "City": "Rawalpindi", "Province": "Punjab"},
            "AdmissionTimestamp": datetime(2024, 3, 5, 9, 0, 0, tzinfo=timezone.utc),
            "LastUpdateTimestamp": firestore.SERVER_TIMESTAMP,
            "ActiveWard": "Endocrinology-1",
            "PrimaryDiagnosis": "Type 1 Diabetes",
            "IsDischarged": False,
            "MedicalAlerts": ["Insulin Dependent"]
        },
        {
            "CNIC": "42301-9012345-9",
            "P_ID": "H1-00009",
            "FirstName": "Omar",
            "LastName": "Rashid",
            "DateOfBirth": datetime(1975, 8, 12, tzinfo=timezone.utc),
            "Gender": "Male",
            "ContactNumber": "+92-300-9012345",
            "Address": {"Street": "House 606, Street 15", "City": "Gujranwala", "Province": "Punjab"},
            "AdmissionTimestamp": datetime(2024, 3, 10, 11, 0, 0, tzinfo=timezone.utc),
            "LastUpdateTimestamp": firestore.SERVER_TIMESTAMP,
            "ActiveWard": "Urology-1",
            "PrimaryDiagnosis": "Kidney Stones",
            "IsDischarged": False,
            "MedicalAlerts": ["Recurrent Stones"]
        },
        {
            "CNIC": "42301-0123456-0",
            "P_ID": "H1-00010",
            "FirstName": "Mehak",
            "LastName": "Yousuf",
            "DateOfBirth": datetime(1987, 5, 18, tzinfo=timezone.utc),
            "Gender": "Female",
            "ContactNumber": "+92-300-0123456",
            "Address": {"Street": "House 707, Street 17", "City": "Sialkot", "Province": "Punjab"},
            "AdmissionTimestamp": datetime(2024, 3, 15, 16, 0, 0, tzinfo=timezone.utc),
            "LastUpdateTimestamp": firestore.SERVER_TIMESTAMP,
            "ActiveWard": "ENT-1",
            "PrimaryDiagnosis": "Sinusitis",
            "IsDischarged": False,
            "MedicalAlerts": ["Allergy: Pollen"]
        }
    ]

    # Hospital 2 Pakistani Patients
    h2_patients = [
        {
            "CNIC": "42301-1234567-1",
            "PT_ID": "H2-00001",
            "FullName": "Ali Hassan",
            "DOB": "1980-05-10",
            "Sex": "M",
            "PhoneNumber": "+92-300-1234567",
            "FullAddress": "House 123, Street 5, Lahore, Punjab",
            "RegistrationDate": datetime(2024, 2, 1, 9, 0, 0, tzinfo=timezone.utc),
            "LastModifiedDate": firestore.SERVER_TIMESTAMP,
            "CurrentRoom": "Med-Bed7",
            "AttendingPhysicianID": "DrMILLER",
            "MedicalAlerts": ["Asthma"],
            "PrimaryDiagnosis": "Pneumonia",
            "PatientStatus": "Admitted"
        },
        {
            "CNIC": "42301-2345678-2",
            "PT_ID": "H2-00002",
            "FullName": "Sadia Khan",
            "DOB": "1992-08-22",
            "Sex": "F",
            "PhoneNumber": "+92-300-2345678",
            "FullAddress": "House 456, Street 8, Karachi, Sindh",
            "RegistrationDate": datetime(2024, 2, 15, 8, 30, 0, tzinfo=timezone.utc),
            "LastModifiedDate": firestore.SERVER_TIMESTAMP,
            "CurrentRoom": "Cardio-ICU",
            "AttendingPhysicianID": "DrSMITH",
            "MedicalAlerts": ["History: Heart Attack"],
            "PrimaryDiagnosis": "Acute Myocardial Infarction",
            "PatientStatus": "Admitted"
        },
        {
            "CNIC": "42301-3456789-3",
            "PT_ID": "H2-00003",
            "FullName": "Imran Malik",
            "DOB": "1975-11-30",
            "Sex": "M",
            "PhoneNumber": "+92-300-3456789",
            "FullAddress": "House 789, Street 12, Islamabad, ICT",
            "RegistrationDate": datetime(2023, 12, 1, 9, 0, 0, tzinfo=timezone.utc),
            "LastModifiedDate": firestore.SERVER_TIMESTAMP,
            "CurrentRoom": "GenSurg-R4",
            "AttendingPhysicianID": "DrJONES",
            "MedicalAlerts": ["Allergy: Shellfish"],
            "PrimaryDiagnosis": "Appendicitis",
            "PatientStatus": "Admitted"
        },
        {
            "CNIC": "42301-4567890-4",
            "PT_ID": "H2-00004",
            "FullName": "Nadia Raza",
            "DOB": "1990-09-12",
            "Sex": "F",
            "PhoneNumber": "+92-300-4567890",
            "FullAddress": "House 101, Street 3, Peshawar, KPK",
            "RegistrationDate": datetime(2024, 3, 5, 14, 20, 0, tzinfo=timezone.utc),
            "LastModifiedDate": firestore.SERVER_TIMESTAMP,
            "CurrentRoom": "Maternity-3",
            "AttendingPhysicianID": "DrWILSON",
            "MedicalAlerts": ["Pregnancy: 32 weeks"],
            "PrimaryDiagnosis": "Prenatal Care",
            "PatientStatus": "Admitted"
        },
        {
            "CNIC": "42301-5678901-5",
            "PT_ID": "H2-00005",
            "FullName": "Kamran Hussain",
            "DOB": "1972-12-05",
            "Sex": "M",
            "PhoneNumber": "+92-300-5678901",
            "FullAddress": "House 202, Street 7, Quetta, Balochistan",
            "RegistrationDate": datetime(2024, 2, 28, 10, 45, 0, tzinfo=timezone.utc),
            "LastModifiedDate": firestore.SERVER_TIMESTAMP,
            "CurrentRoom": "ER-2",
            "AttendingPhysicianID": "DrTAYLOR",
            "MedicalAlerts": ["Allergy: Penicillin"],
            "PrimaryDiagnosis": "Severe Allergic Reaction",
            "PatientStatus": "Discharged"
        },
        {
            "CNIC": "42301-6789012-6",
            "PT_ID": "H2-00006",
            "FullName": "Farah Iqbal",
            "DOB": "1985-03-25",
            "Sex": "F",
            "PhoneNumber": "+92-300-6789012",
            "FullAddress": "House 303, Street 9, Faisalabad, Punjab",
            "RegistrationDate": datetime(2024, 3, 10, 11, 0, 0, tzinfo=timezone.utc),
            "LastModifiedDate": firestore.SERVER_TIMESTAMP,
            "CurrentRoom": "Neurology-1",
            "AttendingPhysicianID": "DrBROWN",
            "MedicalAlerts": ["Epilepsy"],
            "PrimaryDiagnosis": "Seizure Disorder",
            "PatientStatus": "Admitted"
        },
        {
            "CNIC": "42301-7890123-7",
            "PT_ID": "H2-00007",
            "FullName": "Tariq Abbas",
            "DOB": "1995-07-20",
            "Sex": "M",
            "PhoneNumber": "+92-300-7890123",
            "FullAddress": "House 404, Street 11, Multan, Punjab",
            "RegistrationDate": datetime(2024, 3, 15, 16, 0, 0, tzinfo=timezone.utc),
            "LastModifiedDate": firestore.SERVER_TIMESTAMP,
            "CurrentRoom": "Orthopedics-2",
            "AttendingPhysicianID": "DrWHITE",
            "MedicalAlerts": ["Osteoporosis"],
            "PrimaryDiagnosis": "Hip Fracture",
            "PatientStatus": "Admitted"
        },
        {
            "CNIC": "42301-8901234-8",
            "PT_ID": "H2-00008",
            "FullName": "Zara Shah",
            "DOB": "1988-04-15",
            "Sex": "F",
            "PhoneNumber": "+92-300-8901234",
            "FullAddress": "House 505, Street 13, Rawalpindi, Punjab",
            "RegistrationDate": datetime(2024, 3, 20, 9, 0, 0, tzinfo=timezone.utc),
            "LastModifiedDate": firestore.SERVER_TIMESTAMP,
            "CurrentRoom": "Oncology-2",
            "AttendingPhysicianID": "DrGREEN",
            "MedicalAlerts": ["Family History: Cancer"],
            "PrimaryDiagnosis": "Lung Cancer",
            "PatientStatus": "Admitted"
        },
        {
            "CNIC": "42301-9012345-9",
            "PT_ID": "H2-00009",
            "FullName": "Rashid Malik",
            "DOB": "1978-09-05",
            "Sex": "M",
            "PhoneNumber": "+92-300-9012345",
            "FullAddress": "House 606, Street 15, Gujranwala, Punjab",
            "RegistrationDate": datetime(2024, 3, 25, 14, 0, 0, tzinfo=timezone.utc),
            "LastModifiedDate": firestore.SERVER_TIMESTAMP,
            "CurrentRoom": "Gastro-1",
            "AttendingPhysicianID": "DrBLACK",
            "MedicalAlerts": ["Ulcerative Colitis"],
            "PrimaryDiagnosis": "Gastroenteritis",
            "PatientStatus": "Admitted"
        },
        {
            "CNIC": "42301-0123456-0",
            "PT_ID": "H2-00010",
            "FullName": "Amina Yousuf",
            "DOB": "1993-02-28",
            "Sex": "F",
            "PhoneNumber": "+92-300-0123456",
            "FullAddress": "House 707, Street 17, Sialkot, Punjab",
            "RegistrationDate": datetime(2024, 3, 30, 10, 0, 0, tzinfo=timezone.utc),
            "LastModifiedDate": firestore.SERVER_TIMESTAMP,
            "CurrentRoom": "Pediatrics-B",
            "AttendingPhysicianID": "DrGRAY",
            "MedicalAlerts": ["Asthma"],
            "PrimaryDiagnosis": "Bronchitis",
            "PatientStatus": "Admitted"
        }
    ]

    # Add patients to respective collections
    for patient in h1_patients:
        db.collection('hospital1_patients').document(patient['CNIC']).set(patient)
    
    for patient in h2_patients:
        db.collection('hospital2_patients').document(patient['CNIC']).set(patient)
    
    # Add two unique patients to hospital1_patients
    new_h1_patients = [
        {
            "CNIC": "42301-8888888-1",
            "P_ID": "H1-00011",
            "FirstName": "Sohail",
            "LastName": "Akhtar",
            "DateOfBirth": datetime(1991, 4, 12, tzinfo=timezone.utc),
            "Gender": "Male",
            "ContactNumber": "+92-300-8888881",
            "Address": {"Street": "House 808, Street 18", "City": "Hyderabad", "Province": "Sindh"},
            "AdmissionTimestamp": datetime(2024, 4, 10, 10, 0, 0, tzinfo=timezone.utc),
            "LastUpdateTimestamp": firestore.SERVER_TIMESTAMP,
            "ActiveWard": "Cardiology-A",
            "PrimaryDiagnosis": "Arrhythmia",
            "IsDischarged": False,
            "MedicalAlerts": ["Hypertension"]
        },
        {
            "CNIC": "42301-8888888-2",
            "P_ID": "H1-00012",
            "FirstName": "Rabia",
            "LastName": "Qureshi",
            "DateOfBirth": datetime(1996, 7, 19, tzinfo=timezone.utc),
            "Gender": "Female",
            "ContactNumber": "+92-300-8888882",
            "Address": {"Street": "House 909, Street 19", "City": "Sukkur", "Province": "Sindh"},
            "AdmissionTimestamp": datetime(2024, 4, 12, 11, 0, 0, tzinfo=timezone.utc),
            "LastUpdateTimestamp": firestore.SERVER_TIMESTAMP,
            "ActiveWard": "Neurology-3",
            "PrimaryDiagnosis": "Epilepsy",
            "IsDischarged": False,
            "MedicalAlerts": ["None"]
        }
    ]
    for patient in new_h1_patients:
        db.collection('hospital1_patients').document(patient['CNIC']).set(patient)

    # Add two unique patients to hospital2_patients
    new_h2_patients = [
        {
            "CNIC": "42301-9999999-1",
            "PT_ID": "H2-00011",
            "FullName": "Imtiaz Ahmed",
            "DOB": "1983-11-23",
            "Sex": "M",
            "PhoneNumber": "+92-300-9999991",
            "FullAddress": "House 111, Street 21, Abbottabad, KPK",
            "RegistrationDate": datetime(2024, 4, 15, 9, 0, 0, tzinfo=timezone.utc),
            "LastModifiedDate": firestore.SERVER_TIMESTAMP,
            "CurrentRoom": "ICU-3",
            "AttendingPhysicianID": "DrKHAN",
            "MedicalAlerts": ["COPD"],
            "PrimaryDiagnosis": "Respiratory Failure",
            "PatientStatus": "Admitted"
        },
        {
            "CNIC": "42301-9999999-2",
            "PT_ID": "H2-00012",
            "FullName": "Nida Farooq",
            "DOB": "1998-02-14",
            "Sex": "F",
            "PhoneNumber": "+92-300-9999992",
            "FullAddress": "House 222, Street 22, Bahawalpur, Punjab",
            "RegistrationDate": datetime(2024, 4, 18, 10, 0, 0, tzinfo=timezone.utc),
            "LastModifiedDate": firestore.SERVER_TIMESTAMP,
            "CurrentRoom": "Maternity-4",
            "AttendingPhysicianID": "DrFAROOQ",
            "MedicalAlerts": ["Pregnancy: 36 weeks"],
            "PrimaryDiagnosis": "Prenatal Care",
            "PatientStatus": "Admitted"
        }
    ]
    for patient in new_h2_patients:
        db.collection('hospital2_patients').document(patient['CNIC']).set(patient)

    print("Added test patients to both hospitals, including new unique patients")

def add_second_visit():
    # Add a second visit to Hospital 1 for the same patient
    h1_second_visit = {
        "CNIC": "11111-1111111-1",
        "P_ID": "H1-00002",
        "FirstName": "Alice",
        "LastName": "Anderson",
        "DateOfBirth": datetime(1980, 5, 10, tzinfo=timezone.utc),
        "Gender": "Female",
        "ContactNumber": "+1-555-1111",
        "Address": {"Street": "10 Pine St", "City": "Metroville", "Province": "Region A"},
        "AdmissionTimestamp": datetime(2024, 3, 1, 14, 0, 0, tzinfo=timezone.utc),
        "LastUpdateTimestamp": firestore.SERVER_TIMESTAMP,
        "ActiveWard": "Orthopedics-1",
        "PrimaryDiagnosis": "Fractured Ankle",
        "IsDischarged": False,
        "DischargeTimestamp": None,
        "MedicalAlerts": ["Allergy: Penicillin", "Asthma"]
    }
    
    db.collection('hospital1_patients').document(h1_second_visit['CNIC']).set(h1_second_visit)
    print("Added second visit to Hospital 1")

def check_central_database():
    print("\nChecking central database...")
    central_ref = db.collection('central_patients')
    docs = central_ref.stream()
    
    for doc in docs:
        print_patient_details(doc)

def clear_collections():
    # Clear hospital1_patients collection
    docs = db.collection('hospital1_patients').stream()
    for doc in docs:
        doc.reference.delete()
    
    # Clear hospital2_patients collection
    docs = db.collection('hospital2_patients').stream()
    for doc in docs:
        doc.reference.delete()
    
    # Clear central_patients collection
    docs = db.collection('central_patients').stream()
    for doc in docs:
        doc.reference.delete()
    
    print("Cleared all collections")

def main():
    print("Starting CDC History Test")
    
    # Step 0: Clear existing data
    print("\nStep 0: Clearing existing data")
    clear_collections()
    
    # Step 1: Add initial test patients
    print("\nStep 1: Adding initial test patients")
    add_test_patients()
    time.sleep(5)  # Wait for CDC to process
    
    # Step 2: Check central database
    print("\nStep 2: Checking central database after initial data")
    check_central_database()
    
    # Step 3: Add second visit
    print("\nStep 3: Adding second visit")
    add_second_visit()
    time.sleep(5)  # Wait for CDC to process
    
    # Step 4: Check central database again
    print("\nStep 4: Checking central database after second visit")
    check_central_database()

if __name__ == "__main__":
    main() 