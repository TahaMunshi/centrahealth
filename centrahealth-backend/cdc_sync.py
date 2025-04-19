import os
import psycopg2
import datetime

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "centrahealth")
DB_USER = os.getenv("DB_USER", "centrauser")
DB_PASS = os.getenv("DB_PASS", "centrapass")

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cursor = conn.cursor()

# Define hospital databases
hospitals = [
    {
        'name': 'Ziauddin',
        'db': 'Ziauddin_HospitalDB'
    },
    {
        'name': 'Aga Khan',
        'db': 'AgaKhan_HospitalDB'
    }
]

for hospital in hospitals:
    print(f"🔄 Syncing from {hospital['name']}")

    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=localhost;DATABASE={hospital["db"]};Trusted_Connection=yes;'
    )
    cursor = conn.cursor()

    # Fetch new CDC records
    cursor.execute("""
        SELECT r.Record_ID, r.P_ID, r.Record_Type, r.Details, r.Timestamp, r.Doctor_Email
        FROM cdc.dbo_Hospital_Record_CT r
        WHERE r.__$operation = 2
    """)

    records = cursor.fetchall()
    print(f"Found {len(records)} new records")

    for record in records:
        record_id, p_id, record_type, details, timestamp, doctor_email = record

        # Get patient info from hospital DB
        cursor.execute("SELECT CNIC, Full_Name, DOB, Gender, Phone FROM Hospital_Patient WHERE P_ID = ?", p_id)
        patient = cursor.fetchone()
        if not patient:
            print(f"⚠️ No patient found for P_ID {p_id}")
            continue

        cnic, full_name, dob, gender, phone = patient

        # Insert patient into central DB if not exists
        central_cursor.execute("SELECT Patient_ID FROM Central_Patient WHERE CNIC = ?", cnic)
        row = central_cursor.fetchone()
        if row:
            patient_id = row.Patient_ID
        else:
            central_cursor.execute("""
                INSERT INTO Central_Patient (CNIC, Full_Name, DOB, Gender, Phone)
                VALUES (?, ?, ?, ?, ?)
            """, (cnic, full_name, dob, gender, phone))
            central_cursor.execute("SELECT @@IDENTITY")
            patient_id = central_cursor.fetchone()[0]

        # Insert into Mapped_Record
        central_cursor.execute("""
            INSERT INTO Mapped_Record (Patient_ID, Source_Record_ID, Hospital_Name, Record_Type, Standardized_Details, Timestamp, Operation_Type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (patient_id, record_id, hospital['name'], record_type, details, timestamp, 'INSERT'))

        # Get Doctor_ID from Doctor_Email
        central_cursor.execute("SELECT Doctor_ID FROM Doctor WHERE Email = ?", doctor_email)
        doc_row = central_cursor.fetchone()
        if not doc_row:
            print(f"⚠️ Doctor not found in central DB: {doctor_email}")
            continue

        doctor_id = doc_row.Doctor_ID

        # Link Doctor to Patient if not already linked
        central_cursor.execute("""
            SELECT * FROM Doctor_Patient
            WHERE Doctor_ID = ? AND Patient_ID = ?
        """, (doctor_id, patient_id))

        if not central_cursor.fetchone():
            central_cursor.execute("""
                INSERT INTO Doctor_Patient (Doctor_ID, Patient_ID)
                VALUES (?, ?)
            """, (doctor_id, patient_id))
            print(f"✅ Linked {doctor_email} to patient {cnic}")

    # Commit changes after each hospital
    central_conn.commit()

print("✅ Sync complete.")
