from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import firebase_admin
from firebase_admin import credentials, auth, firestore
import requests
import os

# Initialize Firebase Admin
cred = credentials.Certificate("/app/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserLogin(BaseModel):
    email: str
    password: str
    role: str

class User(BaseModel):
    id: str
    email: str
    role: str
    name: str

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")

@app.post("/api/auth/login")
async def login(user_data: UserLogin):
    # Authenticate with Firebase Auth REST API
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {
        "email": user_data.email,
        "password": user_data.password,
        "returnSecureToken": True
    }
    resp = requests.post(url, json=payload)
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    auth_data = resp.json()
    uid = auth_data["localId"]

    # Special case for admin
    if user_data.email == "admin@yourdomain.com":
        return {
            "token": auth_data["idToken"],
            "user": {
                "id": uid,
                "email": user_data.email,
                "role": "admin",
                "name": "Admin User"
            }
        }

    # Fetch patient data from Firestore (central_patients)
    patient_ref = db.collection("central_patients").document(uid)
    patient_doc = patient_ref.get()
    if not patient_doc.exists:
        raise HTTPException(status_code=403, detail="No patient record found.")
    patient = patient_doc.to_dict()
    name = patient.get("FullName") or f"{patient.get('FirstName', '')} {patient.get('LastName', '')}".strip()

    # Return token and user info
    return {
        "token": auth_data["idToken"],
        "user": {
            "id": uid,
            "email": user_data.email,
            "role": "patient",
            "name": name
        }
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/patient/me")
async def get_patient_me(authorization: str = Header(...)):
    # Extract the ID token from the Authorization header
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    id_token = authorization.split(" ", 1)[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Fetch patient data from Firestore (central_patients)
    patient_ref = db.collection("central_patients").document(uid)
    patient_doc = patient_ref.get()
    if not patient_doc.exists:
        raise HTTPException(status_code=404, detail="Patient record not found.")
    patient = patient_doc.to_dict()
    return patient

@app.get("/api/admin/summary")
async def admin_summary():
    patients_ref = db.collection("central_patients")
    patients = list(patients_ref.stream())
    patient_count = len(patients)
    hospital_set = set()
    for doc in patients:
        data = doc.to_dict()
        visits = data.get("visits", [])
        for visit in visits:
            hospital = visit.get("hospital")
            if hospital:
                hospital_set.add(hospital)
    hospital_count = len(hospital_set)
    return {
        "total_hospitals": hospital_count,
        "total_patients": patient_count
    }

@app.get("/api/admin/patients")
async def admin_list_patients():
    patients_ref = db.collection("central_patients")
    patients = [doc.to_dict() for doc in patients_ref.stream()]
    return patients

@app.get("/api/admin/hospitals")
async def admin_list_hospitals():
    patients_ref = db.collection("central_patients")
    hospital_map = {}
    for doc in patients_ref.stream():
        patient = doc.to_dict()
        # Always get the correct name from the main patient record
        patient_name = patient.get("FullName") or f"{patient.get('FirstName', '')} {patient.get('LastName', '')}".strip()
        visits = patient.get("visits", [])
        for visit in visits:
            hospital = visit.get("hospital")
            if hospital:
                if hospital not in hospital_map:
                    hospital_map[hospital] = []
                hospital_map[hospital].append({
                    "CNIC": patient.get("CNIC"),
                    "FullName": patient_name,
                    "ContactNumber": patient.get("ContactNumber"),
                    "Gender": patient.get("Gender"),
                    "DateOfBirth": str(patient.get("DateOfBirth")),
                })
    hospitals = [
        {"hospital": hospital, "patients": patients}
        for hospital, patients in hospital_map.items()
    ]
    return hospitals 