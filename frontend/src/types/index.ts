export interface User {
  id: string;
  email: string;
  role: 'admin' | 'doctor' | 'patient';
  name: string;
}

export interface Patient {
  id: string;
  cnic: string;
  name: string;
  dateOfBirth: string;
  gender: string;
  contactNumber: string;
  address: string;
  medicalHistory: MedicalHistory[];
}

export interface MedicalHistory {
  id: string;
  patientId: string;
  hospitalId: string;
  doctorId: string;
  visitDate: string;
  diagnosis: string;
  prescription: string;
  notes: string;
  followUpDate?: string;
}

export interface Doctor {
  id: string;
  name: string;
  specialization: string;
  licenseNumber: string;
  hospitalId: string;
  patients: Patient[];
}

export interface Hospital {
  id: string;
  name: string;
  address: string;
  contactNumber: string;
  doctors: Doctor[];
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
} 