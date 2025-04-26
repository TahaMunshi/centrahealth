import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to add the auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const authService = {
  login: async (email: string, password: string, role: string) => {
    const response = await api.post('/auth/login', { email, password, role });
    return response.data;
  },
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
};

export const patientService = {
  getPatients: async () => {
    const response = await api.get('/patients');
    return response.data;
  },
  getPatientById: async (id: string) => {
    const response = await api.get(`/patients/${id}`);
    return response.data;
  },
  getPatientHistory: async (id: string) => {
    const response = await api.get(`/patients/${id}/history`);
    return response.data;
  },
};

export const doctorService = {
  getDoctors: async () => {
    const response = await api.get('/doctors');
    return response.data;
  },
  getDoctorPatients: async (doctorId: string) => {
    const response = await api.get(`/doctors/${doctorId}/patients`);
    return response.data;
  },
  getDoctorAppointments: async (doctorId: string) => {
    const response = await api.get(`/doctors/${doctorId}/appointments`);
    return response.data;
  },
};

export const hospitalService = {
  getHospitals: async () => {
    const response = await api.get('/hospitals');
    return response.data;
  },
  getHospitalDoctors: async (hospitalId: string) => {
    const response = await api.get(`/hospitals/${hospitalId}/doctors`);
    return response.data;
  },
};

export default api; 