-- Ziauddin_HospitalDB.sql

IF DB_ID('Ziauddin_HospitalDB') IS NOT NULL
BEGIN
    ALTER DATABASE Ziauddin_HospitalDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE Ziauddin_HospitalDB;
END;
GO

CREATE DATABASE Ziauddin_HospitalDB;
GO
USE Ziauddin_HospitalDB;
GO

EXEC sys.sp_cdc_enable_db;
GO

CREATE TABLE Hospital_Patient (
    P_ID INT PRIMARY KEY IDENTITY,
    CNIC VARCHAR(20) UNIQUE,
    Full_Name VARCHAR(100),
    DOB DATE,
    Gender VARCHAR(10),
    Phone VARCHAR(20)
);

CREATE TABLE Hospital_Record (
    Record_ID INT PRIMARY KEY IDENTITY,
    P_ID INT FOREIGN KEY REFERENCES Hospital_Patient(P_ID),
    Record_Type VARCHAR(50),
    Details VARCHAR(255),
    Timestamp DATETIME DEFAULT GETDATE(),
    Doctor_Email VARCHAR(100)
);
GO

EXEC sys.sp_cdc_enable_table  
    @source_schema = N'dbo',  
    @source_name   = N'Hospital_Record',  
    @role_name     = NULL,  
    @supports_net_changes = 1;
GO

-- Patients
DECLARE @i INT = 1;
WHILE @i <= 50
BEGIN
    INSERT INTO Hospital_Patient (CNIC, Full_Name, DOB, Gender, Phone)
    VALUES (
        CONCAT('42101', FORMAT(@i, '0000000'), '1'),
        CONCAT('Ziauddin Patient ', @i),
        DATEADD(DAY, -@i * 90, GETDATE()),
        CASE WHEN @i % 2 = 0 THEN 'Male' ELSE 'Female' END,
        CONCAT('0300', FORMAT(@i, '0000000'))
    );
    SET @i += 1;
END;

-- Records
DECLARE @j INT = 1;
WHILE @j <= 50
BEGIN
    INSERT INTO Hospital_Record (P_ID, Record_Type, Details, Doctor_Email)
    VALUES (
        @j,
        CASE WHEN @j % 2 = 0 THEN 'Visit' ELSE 'Test' END,
        CONCAT('Ziauddin record #', @j),
        CASE 
            WHEN @j % 3 = 0 THEN 'doctor@test.com'
            WHEN @j % 3 = 1 THEN 'dr.ali@ziauddin.com'
            ELSE 'dr.sana@ziauddin.com'
        END
    );
    SET @j += 1;
END;
