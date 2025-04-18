# 🏥 CentraHealth Database Setup

This folder contains SQL setup scripts for the complete CentraHealth project, including all databases and initial test data.

## 📦 Included SQL Files

| File                        | Purpose                                     |
|----------------------------|---------------------------------------------|
| `Ziauddin_HospitalDB.sql`  | Creates the Ziauddin hospital DB, enables CDC, and populates 50 patients + records |
| `AgaKhan_HospitalDB.sql`   | Creates the Aga Khan hospital DB, enables CDC, and populates 50 patients + records |
| `CentraHealth_CentralDB.sql` | Creates the central database with schema, doctor accounts, and relationship mapping support |

---

## ✅ Setup Instructions

### Prerequisites:
- Microsoft SQL Server (Express or Developer)
- SQL Server Agent **must be running** for CDC
- Python + `pyodbc` + `cdc_sync.py` ready to run

---

### 🛠 Step-by-Step Setup

1. Open **SQL Server Management Studio (SSMS)**

2. **Run in Order**:
   - `Ziauddin_HospitalDB.sql`
   - `AgaKhan_HospitalDB.sql`
   - `CentraHealth_CentralDB.sql`

3. Verify:
   - `cdc.dbo_Hospital_Record_CT` exists in both hospital DBs
   - `Doctor` and `Doctor_Patient` are created in central DB

---

### 🔄 Sync the Data

After running the scripts, run the CDC sync script from the backend directory:

```bash
python cdc_sync.py
