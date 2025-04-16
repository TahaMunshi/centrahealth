-- CentraHealth_CentralDB.sql

IF DB_ID('CentraHealth_CentralDB') IS NOT NULL
BEGIN
    ALTER DATABASE CentraHealth_CentralDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE CentraHealth_CentralDB;
END;
GO

CREATE DATABASE CentraHealth_CentralDB;
GO
USE CentraHealth_CentralDB;
GO

CREATE TABLE Central_Patient (
    Patient_ID INT PRIMARY KEY IDENTITY(1,1),
    CNIC VARCHAR(20) UNIQUE NOT NULL,
    Full_Name VARCHAR(100),
    DOB DATE,
    Gender VARCHAR(10),
    Phone VARCHAR(20)
);

CREATE TABLE Doctor (
    Doctor_ID INT PRIMARY KEY IDENTITY(1,1),
    Full_Name VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(20),
    Hospital_Name VARCHAR(100),
    Password VARCHAR(100)
);

CREATE TABLE Doctor_Patient (
    Relation_ID INT PRIMARY KEY IDENTITY(1,1),
    Doctor_ID INT FOREIGN KEY REFERENCES Doctor(Doctor_ID),
    Patient_ID INT FOREIGN KEY REFERENCES Central_Patient(Patient_ID),
    Created_At DATETIME DEFAULT GETDATE()
);

CREATE TABLE Mapped_Record (
    Mapped_ID INT PRIMARY KEY IDENTITY(1,1),
    Patient_ID INT FOREIGN KEY REFERENCES Central_Patient(Patient_ID),
    Source_Record_ID INT,
    Hospital_Name VARCHAR(100),
    Record_Type VARCHAR(50),
    Standardized_Details VARCHAR(255),
    Timestamp DATETIME,
    Operation_Type VARCHAR(10)
);

-- Sample doctors including 'doctor@test.com'
INSERT INTO Doctor (Full_Name, Email, Phone, Hospital_Name, Password)
VALUES
-- Ziauddin doctors
('Dr. Taha Munshi', 'doctor@test.com', '03001112222', 'Ziauddin', '1234'),
('Dr. Ali Zia', 'dr.ali@ziauddin.com', '03009991111', 'Ziauddin', '1234'),
('Dr. Sana Sheikh', 'dr.sana@ziauddin.com', '03009992222', 'Ziauddin', '1234'),
-- Aga Khan doctors
('Dr. Zara Khan', 'dr.zara@agakhan.com', '03219993333', 'Aga Khan', '1234'),
('Dr. Omar Jamil', 'dr.omar@agakhan.com', '03219994444', 'Aga Khan', '1234'),
('Dr. Zeeshan Rafiq', 'dr.zeeshan@agakhan.com', '03219995555', 'Aga Khan', '1234');
