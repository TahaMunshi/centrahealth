from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)

# Connect to central DB
central_conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=CentraHealth_CentralDB;'
    'Trusted_Connection=yes;'
)
central_cursor = central_conn.cursor()


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    central_cursor.execute("""
        SELECT Full_Name FROM Doctor
        WHERE LOWER(Email) = LOWER(?) AND Password = ?
    """, (email, password))

    row = central_cursor.fetchone()
    if row:
        return jsonify({'message': 'Login successful', 'name': row.Full_Name}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/patients')
def get_patients():
    cnic = request.args.get('cnic', '')
    doctor_email = request.args.get('doctor_email', '')

    if not doctor_email:
        return jsonify({'error': 'Doctor email is required'}), 400

    # Step 1: Get Doctor_ID using email
    central_cursor.execute("SELECT Doctor_ID FROM Doctor WHERE Email = ?", doctor_email)
    row = central_cursor.fetchone()
    if not row:
        return jsonify({'error': 'Doctor not found'}), 404

    doctor_id = row.Doctor_ID

    # Step 2: Return patients this doctor is authorized to see
    central_cursor.execute("""
        SELECT cp.Patient_ID, cp.CNIC, cp.Full_Name, cp.DOB, cp.Gender
        FROM Central_Patient cp
        JOIN Doctor_Patient dp ON cp.Patient_ID = dp.Patient_ID
        WHERE dp.Doctor_ID = ? AND cp.CNIC LIKE ?
    """, (doctor_id, f"%{cnic}%"))

    patients = central_cursor.fetchall()
    results = [{
        "Patient_ID": p.Patient_ID,
        "CNIC": p.CNIC,
        "Full_Name": p.Full_Name,
        "DOB": p.DOB.strftime('%Y-%m-%d'),
        "Gender": p.Gender
    } for p in patients]

    return jsonify(results)


@app.route('/api/records')
def get_records():
    cnic = request.args.get('cnic')
    if not cnic:
        return jsonify({'error': 'CNIC parameter is required'}), 400

    # Step 1: Get the patient ID from CNIC
    central_cursor.execute("SELECT Patient_ID FROM Central_Patient WHERE CNIC = ?", cnic)
    row = central_cursor.fetchone()
    if not row:
        return jsonify([])  # No records if patient doesn't exist

    patient_id = row.Patient_ID

    # Step 2: Get mapped records for this patient
    central_cursor.execute("""
        SELECT Hospital_Name, Record_Type, Standardized_Details, Timestamp
        FROM Mapped_Record
        WHERE Patient_ID = ?
        ORDER BY Timestamp DESC
    """, patient_id)

    records = central_cursor.fetchall()
    result = [{
        "Hospital": r.Hospital_Name,
        "Type": r.Record_Type,
        "Details": r.Standardized_Details,
        "Timestamp": r.Timestamp.strftime('%Y-%m-%d %H:%M')
    } for r in records]

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
