-- Use the database
USE CentraHealth_HospitalDB;
GO

-- Enable CDC on the database
EXEC sys.sp_cdc_enable_db;
GO

-- Table: Hospital
CREATE TABLE Hospital (
    Hospital_ID INT PRIMARY KEY IDENTITY,
    Hospital_Name VARCHAR(100),
    Location VARCHAR(100)
);

-- Table: Doctor (for login)
CREATE TABLE Doctor (
    Doctor_ID INT PRIMARY KEY IDENTITY,
    Full_Name VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(100),
    Hospital_ID INT FOREIGN KEY REFERENCES Hospital(Hospital_ID)
);

-- Table: Hospital_Patient
CREATE TABLE Hospital_Patient (
    P_ID INT PRIMARY KEY IDENTITY,
    Full_Name VARCHAR(100),
    CNIC VARCHAR(15) UNIQUE,
    DOB DATE,
    Gender VARCHAR(10),
    Phone VARCHAR(20),
    Hospital_ID INT FOREIGN KEY REFERENCES Hospital(Hospital_ID)
);

-- Table: Hospital_Record (CDC enabled here)
CREATE TABLE Hospital_Record (
    Record_ID INT PRIMARY KEY IDENTITY,
    P_ID INT FOREIGN KEY REFERENCES Hospital_Patient(P_ID),
    Hospital_ID INT FOREIGN KEY REFERENCES Hospital(Hospital_ID),
    Record_Type VARCHAR(50),  -- Test, Visit, etc.
    Details VARCHAR(255),
    Timestamp DATETIME DEFAULT GETDATE()
);
GO

-- Enable CDC on Hospital_Record
EXEC sys.sp_cdc_enable_table  
    @source_schema = N'dbo',  
    @source_name   = N'Hospital_Record',  
    @role_name     = NULL,  
    @supports_net_changes = 1;
GO

-- Insert sample data
INSERT INTO Hospital (Hospital_Name, Location)
VALUES ('Aga Khan Hospital', 'Karachi');

INSERT INTO Doctor (Full_Name, Email, Password, Hospital_ID)
VALUES ('Dr. Taha', 'doctor@test.com', '1234', 1);

INSERT INTO Hospital_Patient (Full_Name, CNIC, DOB, Gender, Phone, Hospital_ID)
VALUES 
('Ali Khan', '42101-1234567-1', '1990-05-10', 'Male', '03001234567', 1),
('Sara Ahmed', '35202-9876543-2', '1985-03-15', 'Female', '03219876543', 1);

INSERT INTO Hospital_Record (P_ID, Hospital_ID, Record_Type, Details)
VALUES 
(1, 1, 'Test', 'Blood test - Normal'),
(2, 1, 'Visit', 'Routine checkup');
GO


select * from Hospital_Patient;