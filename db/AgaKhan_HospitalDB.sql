-- AgaKhan_HospitalDB.sql

IF DB_ID('AgaKhan_HospitalDB') IS NOT NULL
BEGIN
    ALTER DATABASE AgaKhan_HospitalDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE AgaKhan_HospitalDB;
END;
GO

CREATE DATABASE AgaKhan_HospitalDB;
GO
USE AgaKhan_HospitalDB;
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
        CONCAT('35202', FORMAT(@i, '0000000'), '2'),
        CONCAT('Aga Khan Patient ', @i),
        DATEADD(DAY, -@i * 85, GETDATE()),
        CASE WHEN @i % 2 = 0 THEN 'Male' ELSE 'Female' END,
        CONCAT('0321', FORMAT(@i, '0000000'))
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
        CASE WHEN @j % 2 = 0 THEN 'Test' ELSE 'Visit' END,
        CONCAT('Aga Khan record #', @j),
        CASE 
            WHEN @j % 3 = 0 THEN 'doctor@test.com'
            WHEN @j % 3 = 1 THEN 'dr.zara@agakhan.com'
            ELSE 'dr.omar@agakhan.com'
        END
    );
    SET @j += 1;
END;
