import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const API_BASE = 'http://localhost:5000';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await axios.post(`${API_BASE}/login`, {
        email,
        password
      });
  
      if (res.status === 200) {
        localStorage.setItem('doctorName', res.data.name);
        localStorage.setItem('doctorEmail', email); // NEW LINE ✅
        navigate('/dashboard');
      }
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: '400px' }}>
      <h3 className="text-center mb-4">Login to CentraHealth</h3>
      <div className="card p-4">
        <div className="mb-3">
          <label>Email</label>
          <input className="form-control" type="email" value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <div className="mb-3">
          <label>Password</label>
          <input className="form-control" type="password" value={password} onChange={e => setPassword(e.target.value)} />
        </div>
        <button className="btn btn-primary w-100" onClick={handleLogin}>Login</button>
        {error && <div className="text-danger mt-3 text-center">{error}</div>}
      </div>
    </div>
  );
}

function Dashboard() {
  const [searchCNIC, setSearchCNIC] = useState('');
  const [patients, setPatients] = useState([]);
  const doctorName = localStorage.getItem('doctorName') || 'Doctor';

  const fetchPatients = async () => {
    const doctorEmail = localStorage.getItem('doctorEmail');
    const res = await axios.get(`${API_BASE}/api/patients`, {
      params: {
        cnic: searchCNIC,
        doctor_email: doctorEmail
      }
    });
    if (!doctorEmail) {
      alert("Doctor not authenticated");
      return;
    }    
    setPatients(res.data);
  };
  

  return (
    <div className="container mt-4">
      <h2>Welcome, Dr. {doctorName}</h2>
      <div className="mb-3">
        <input className="form-control" placeholder="Search by CNIC" value={searchCNIC} onChange={(e) => setSearchCNIC(e.target.value)} />
        <button className="btn btn-secondary mt-2" onClick={fetchPatients}>Search</button>
      </div>
      {patients.length > 0 && (
        <table className="table table-bordered">
          <thead>
            <tr>
              <th>CNIC</th>
              <th>Name</th>
              <th>DOB</th>
              <th>Gender</th>
            </tr>
          </thead>
          <tbody>
            {patients.map((p, index) => (
              <tr key={index}>
                <td>{p.CNIC}</td>
                <td>{p.Full_Name}</td>
                <td>{p.DOB}</td>
                <td>{p.Gender}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

function AppWrapper() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default AppWrapper;
