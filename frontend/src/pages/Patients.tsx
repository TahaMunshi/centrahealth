import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, CircularProgress } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { DashboardLayout } from '../layouts/DashboardLayout';

const Patients: React.FC = () => {
  const { user, token } = useAuth();
  const [patients, setPatients] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPatients = async () => {
      if (user?.role === 'admin' && token) {
        setLoading(true);
        setError('');
        try {
          const response = await fetch('/api/admin/patients', {
            headers: { Authorization: `Bearer ${token}` },
          });
          if (!response.ok) throw new Error('Failed to fetch patients');
          const data = await response.json();
          setPatients(data);
        } catch (err: any) {
          setError(err.message || 'Error fetching patients');
        } finally {
          setLoading(false);
        }
      }
    };
    fetchPatients();
  }, [user, token]);

  return (
    <DashboardLayout title="Patients">
      <Box sx={{ p: 2 }}>
        <Typography variant="h5" gutterBottom>All Patients</Typography>
        {loading ? <CircularProgress /> : error ? <Typography color="error">{error}</Typography> : (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>CNIC</TableCell>
                  <TableCell>Name</TableCell>
                  <TableCell>Gender</TableCell>
                  <TableCell>Date of Birth</TableCell>
                  <TableCell>Contact</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {patients.map((p, idx) => (
                  <TableRow key={idx}>
                    <TableCell>{p.CNIC}</TableCell>
                    <TableCell>{p.FullName || `${p.FirstName} ${p.LastName}`}</TableCell>
                    <TableCell>{p.Gender}</TableCell>
                    <TableCell>{typeof p.DateOfBirth === 'string' ? p.DateOfBirth : (p.DateOfBirth?.toDate?.() || '')}</TableCell>
                    <TableCell>{p.ContactNumber}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Box>
    </DashboardLayout>
  );
};

export default Patients; 