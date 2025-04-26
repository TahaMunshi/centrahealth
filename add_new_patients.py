import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

cred = credentials.Certificate('./centrahealth-8f543-firebase-adminsdk-fbsvc-5b82bee7cc.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def add_new_patients():
    # New patient for hospital1_patients
    patient1 = {
        "CNIC": "42301-7777777-1",
        "P_ID": "H1-00013",
        "FirstName": "Hassan",
        "LastName": "Raza",
        "DateOfBirth": datetime(1994, 8, 21, tzinfo=timezone.utc),
        "Gender": "Male",
        "ContactNumber": "+92-300-7777771",
        "Address": {"Street": "House 111, Street 23", "City": "Rawalpindi", "Province": "Punjab"},
        "AdmissionTimestamp": datetime(2024, 4, 20, 10, 0, 0, tzinfo=timezone.utc),
        "LastUpdateTimestamp": firestore.SERVER_TIMESTAMP,
        "ActiveWard": "Cardiology-C",
        "PrimaryDiagnosis": "Heart Block",
        "IsDischarged": False,
        "MedicalAlerts": ["None"]
    }
    db.collection('hospital1_patients').document(patient1['CNIC']).set(patient1)

    # New patient for hospital2_patients
    patient2 = {
        "CNIC": "42301-7777777-2",
        "PT_ID": "H2-00013",
        "FullName": "Sara Imran",
        "DOB": "1997-03-15",
        "Sex": "F",
        "PhoneNumber": "+92-300-7777772",
        "FullAddress": "House 333, Street 24, Lahore, Punjab",
        "RegistrationDate": datetime(2024, 4, 22, 9, 0, 0, tzinfo=timezone.utc),
        "LastModifiedDate": firestore.SERVER_TIMESTAMP,
        "CurrentRoom": "ER-3",
        "AttendingPhysicianID": "DrIMRAN",
        "MedicalAlerts": ["None"],
        "PrimaryDiagnosis": "Migraine",
        "PatientStatus": "Admitted"
    }
    db.collection('hospital2_patients').document(patient2['CNIC']).set(patient2)

    print("Added two new patients to hospital1_patients and hospital2_patients.")

if __name__ == "__main__":
    add_new_patients() 