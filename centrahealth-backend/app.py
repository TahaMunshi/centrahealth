from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)

# Database connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'  # Or .\\SQLEXPRESS if that's your instance
    'DATABASE=CentraHealth_HospitalDB;'
    'Trusted_Connection=yes;'
)

# === ROUTES ===

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    role = data.get('role', '').strip()

    print(f"Login attempt: {email}, {password}, {role}")  # Debug

    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Doctor
        WHERE LOWER(Email) = LOWER(?) AND Password = ?
    """, (email, password))

    row = cursor.fetchone()
    print("Query result:", row)

    if row:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


# Get patients by CNIC search
@app.route('/api/patients')
def get_patients():
    cnic_query = request.args.get('cnic', '')
    print(f"Search CNIC: {cnic_query}")

    cursor = conn.cursor()
    cursor.execute("""
        SELECT P_ID, CNIC, Full_Name, DOB, Gender
        FROM Hospital_Patient
        WHERE CNIC LIKE ?
    """, f"%{cnic_query}%")

    rows = cursor.fetchall()
    print(f"Result count: {len(rows)}")

    results = []
    for row in rows:
        results.append({
            "Patient_ID": row.P_ID,
            "CNIC": row.CNIC,
            "Full_Name": row.Full_Name,
            "DOB": row.DOB.strftime('%Y-%m-%d'),
            "Gender": row.Gender
        })
    return jsonify(results)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
