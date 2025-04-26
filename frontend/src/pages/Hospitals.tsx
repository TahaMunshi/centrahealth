import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Accordion, AccordionSummary, AccordionDetails, CircularProgress } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useAuth } from '../contexts/AuthContext';
import { DashboardLayout } from '../layouts/DashboardLayout';

const Hospitals: React.FC = () => {
  const { user, token } = useAuth();
  const [hospitals, setHospitals] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchHospitals = async () => {
      if (user?.role === 'admin' && token) {
        setLoading(true);
        setError('');
        try {
          const response = await fetch('/api/admin/hospitals', {
            headers: { Authorization: `Bearer ${token}` },
          });
          if (!response.ok) throw new Error('Failed to fetch hospitals');
          const data = await response.json();
          setHospitals(data);
        } catch (err: any) {
          setError(err.message || 'Error fetching hospitals');
        } finally {
          setLoading(false);
        }
      }
    };
    fetchHospitals();
  }, [user, token]);

  return (
    <DashboardLayout title="Hospitals">
      <Box sx={{ p: 2 }}>
        <Typography variant="h5" gutterBottom>All Hospitals & Patients</Typography>
        {loading ? <CircularProgress /> : error ? <Typography color="error">{error}</Typography> : (
          hospitals.length === 0 ? <Typography>No hospitals found.</Typography> : (
            hospitals.map((hosp, idx) => (
              <Accordion key={idx}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="h6">{hosp.hospital}</Typography>
                  <Typography sx={{ ml: 2 }} color="textSecondary">({hosp.patients.length} patients)</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <TableContainer component={Paper}>
                    <Table size="small">
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
                        {hosp.patients.map((p: any, i: number) => (
                          <TableRow key={i}>
                            <TableCell>{p.CNIC}</TableCell>
                            <TableCell>{p.FullName}</TableCell>
                            <TableCell>{p.Gender}</TableCell>
                            <TableCell>{p.DateOfBirth}</TableCell>
                            <TableCell>{p.ContactNumber}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </AccordionDetails>
              </Accordion>
            ))
          )
        )}
      </Box>
    </DashboardLayout>
  );
};

export default Hospitals; 