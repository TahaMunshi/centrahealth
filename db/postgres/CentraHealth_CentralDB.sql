-- Drop & recreate the central DB
DROP TABLE IF EXISTS hospital_record;
DROP TABLE IF EXISTS doctor;
DROP TABLE IF EXISTS central_patient;

-- Central patients
CREATE TABLE central_patient (
  patient_id SERIAL PRIMARY KEY,
  cnic       VARCHAR(20) UNIQUE NOT NULL,
  full_name  VARCHAR(100),
  dob        DATE,
  gender     VARCHAR(10),
  phone      VARCHAR(20)
);

-- Central doctors
CREATE TABLE doctor (
  doctor_id    SERIAL PRIMARY KEY,
  email        VARCHAR(100) UNIQUE NOT NULL,
  full_name    VARCHAR(100),
  hospital_src VARCHAR(50)    -- e.g. 'Ziauddin' or 'Aga Khan'
);

-- Records (links patients → doctors)
CREATE TABLE hospital_record (
  record_id    SERIAL PRIMARY KEY,
  patient_cnic VARCHAR(20)    REFERENCES central_patient(cnic),
  doctor_id    INTEGER         REFERENCES doctor(doctor_id),
  visit_date   TIMESTAMP,
  notes        TEXT
);
