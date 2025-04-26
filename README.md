# CentraHealth Hospital Dashboard

A full-stack hospital dashboard with real-time patient and hospital management, built with React, FastAPI, Firebase, and Docker.

---

## Features

- Patient, doctor, and admin roles with secure login (Firebase Auth)
- Real-time patient and hospital data from Firestore
- Admin dashboard: see all patients, hospitals, and stats
- CDC (Change Data Capture) test scripts for simulating new data

---

## Getting Started

### 1. **Clone the Repository**

```sh
git clone <your-repo-url>
cd centrahealth-dashboard
```

### 2. **Firebase Setup**

- Create a Firebase project at [Firebase Console](https://console.firebase.google.com/).
- Enable Firestore Database and Email/Password Authentication.
- Download a service account key JSON file and place it at:
  ```
  ./airflow/dags/keys/service-account-key.json
  ```
- Copy your Firebase Web API Key from Project Settings > General.

### 3. **Configure Docker**

- Edit `docker-compose.yml`:
  - Set the path to your service account key.
  - Set the `FIREBASE_WEB_API_KEY` environment variable.

### 4. **Run the Application**

```sh
docker-compose up --build
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)
- Airflow: [http://localhost:8080](http://localhost:8080)

### 5. **Add Test Data**

- Use the provided scripts (e.g., `test_cdc_history.py`, `add_new_patients.py`) to add patients to your Firestore collections.

```sh
python test_cdc_history.py
python add_new_patients.py
```

---

## **Default Admin Login**

- **Email:** `admin@yourdomain.com`
- **Password:** `changeme123`

---

## **Development Notes**

- Do NOT commit `node_modules` or your service account key to GitHub.
- All dependencies are managed via `package.json` (frontend) and `requirements.txt` (backend).
- To install frontend dependencies locally:
  ```sh
  cd frontend
  npm install
  ```

---

## **Contributing**

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## **License**

MIT 