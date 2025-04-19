DROP DATABASE IF EXISTS agakhan_hospitaldb;
CREATE DATABASE agakhan_hospitaldb;
\c agakhan_hospitaldb

-- Same schema as Ziauddin, but different seed values
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

-- Seed 50 AK patients
INSERT INTO patient (cnic, full_name, dob, gender, phone)
SELECT
  LPAD((200000000 + s)::text, 12, '0'),
  'AK Patient ' || s,
  '1990-06-01'::date + (s % 1000),
  CASE WHEN s % 2 = 0 THEN 'Male' ELSE 'Female' END,
  '0310' || LPAD((200000 + s)::text, 7, '0')
FROM generate_series(1,50) AS s;

INSERT INTO record (patient_cnic, doctor_email, visit_date, notes)
SELECT
  p.cnic,
  'doctor@test.com',
  NOW() - ((random()*365)::int || ' days')::interval,
  'Initial visit'
FROM patient p;
