import firebase_admin
from firebase_admin import credentials, auth, firestore

cred = credentials.Certificate('./centrahealth-8f543-firebase-adminsdk-fbsvc-5b82bee7cc.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

DEFAULT_PASSWORD = "changeme123"

# Add admin user
ADMIN_EMAIL = "admin@yourdomain.com"
ADMIN_PASSWORD = DEFAULT_PASSWORD
ADMIN_DISPLAY_NAME = "Admin User"

def create_admin_user():
    try:
        user = auth.create_user(
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD,
            display_name=ADMIN_DISPLAY_NAME
        )
        print(f"Created admin user: {ADMIN_EMAIL}")
    except Exception as e:
        print(f"Admin user may already exist or another error: {e}")

def main():
    create_admin_user()
    patients_ref = db.collection('central_patients')
    docs = patients_ref.stream()
    for doc in docs:
        data = doc.to_dict()
        cnic = data.get('CNIC') or doc.id
        display_name = f"{data.get('FirstName', '')} {data.get('LastName', '')}".strip() or data.get('FullName', '')
        email = f"{cnic}@yourdomain.com"  # Optional, for Firebase Auth
        try:
            user = auth.create_user(
                uid=cnic,
                email=email,
                password=DEFAULT_PASSWORD,
                display_name=display_name
            )
            print(f"Created user for CNIC: {cnic}")
        except Exception as e:
            print(f"User for CNIC {cnic} may already exist or another error: {e}")

if __name__ == "__main__":
    main() 