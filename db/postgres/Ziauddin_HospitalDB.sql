DROP DATABASE IF EXISTS ziauddin_hospitaldb;
CREATE DATABASE ziauddin_hospitaldb;
\c ziauddin_hospitaldb

CREATE TABLE patient (
  patient_id SERIAL PRIMARY KEY,
  cnic       VARCHAR(20) UNIQUE NOT NULL,
  full_name  VARCHAR(100),
  dob        DATE,
  gender     VARCHAR(10),
  phone      VARCHAR(20)
);

CREATE TABLE record (
  record_id    SERIAL PRIMARY KEY,
  patient_cnic VARCHAR(20) REFERENCES patient(cnic),
  doctor_email VARCHAR(100),
  visit_date   TIMESTAMP,
  notes        TEXT
);

-- Seed 50 patients + one record each
INSERT INTO patient (cnic, full_name, dob, gender, phone)
SELECT
  LPAD((100000000 + s)::text, 12, '0'),
  'Patient ' || s,
  '1990-01-01'::date + (s % 1000),
  CASE WHEN s % 2 = 0 THEN 'Male' ELSE 'Female' END,
  '0300' || LPAD((100000 + s)::text, 7, '0')
FROM generate_series(1,50) AS s;

INSERT INTO record (patient_cnic, doctor_email, visit_date, notes)
SELECT
  p.cnic,
  'doctor@test.com',
  NOW() - ((random()*365)::int || ' days')::interval,
  'Initial visit'
FROM patient p;
