import React, { useEffect, useState } from 'react';
import {
  Box,
  Stack,
  Paper,
  Typography,
  Card,
  CardContent,
  CardHeader,
  List,
  ListItem,
  ListItemText,
  Divider,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  People as PeopleIcon,
  LocalHospital as HospitalIcon,
  EventNote as EventIcon,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { DashboardLayout } from '../layouts/DashboardLayout';

export const Dashboard: React.FC = () => {
  const { user, token } = useAuth();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [patientData, setPatientData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [adminSummary, setAdminSummary] = useState<{ total_hospitals: number; total_patients: number } | null>(null);

  useEffect(() => {
    const fetchPatientData = async () => {
      if (user?.role === 'patient' && token) {
        setLoading(true);
        setError('');
        try {
          const response = await fetch('/api/patient/me', {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          if (!response.ok) {
            throw new Error('Failed to fetch patient data');
          }
          const data = await response.json();
          setPatientData(data);
        } catch (err: any) {
          setError(err.message || 'Error fetching patient data');
        } finally {
          setLoading(false);
        }
      }
    };
    fetchPatientData();
  }, [user, token]);

  useEffect(() => {
    const fetchAdminSummary = async () => {
      if (user?.role === 'admin' && token) {
        setLoading(true);
        setError('');
        try {
          const response = await fetch('/api/admin/summary', {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          if (!response.ok) {
            throw new Error('Failed to fetch admin summary');
          }
          const data = await response.json();
          setAdminSummary(data);
        } catch (err: any) {
          setError(err.message || 'Error fetching admin summary');
        } finally {
          setLoading(false);
        }
      }
    };
    fetchAdminSummary();
  }, [user, token]);

  const renderAdminDashboard = () => {
    if (loading) return <Typography>Loading admin data...</Typography>;
    if (error) return <Typography color="error">{error}</Typography>;
    if (!adminSummary) return <Typography>No admin data found.</Typography>;
    return (
      <Stack spacing={3} direction={isMobile ? 'column' : 'row'}>
        <Box sx={{ flex: 1 }}>
          <Card>
            <CardHeader avatar={<PeopleIcon />} title="Total Patients" />
            <CardContent>
              <Typography variant="h4">{adminSummary.total_patients}</Typography>
              <Typography color="textSecondary">Active Patients</Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ flex: 1 }}>
          <Card>
            <CardHeader avatar={<HospitalIcon />} title="Total Hospitals" />
            <CardContent>
              <Typography variant="h4">{adminSummary.total_hospitals}</Typography>
              <Typography color="textSecondary">Registered Hospitals</Typography>
            </CardContent>
          </Card>
        </Box>
      </Stack>
    );
  };

  const renderDoctorDashboard = () => (
    <Stack spacing={3} direction={isMobile ? 'column' : 'row'}>
      <Box sx={{ flex: 1 }}>
        <Card>
          <CardHeader title="My Patients" />
          <CardContent>
            <List>
              <ListItem>
                <ListItemText
                  primary="John Doe"
                  secondary="Last Visit: 2024-04-25"
                />
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText
                  primary="Jane Smith"
                  secondary="Last Visit: 2024-04-24"
                />
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText
                  primary="Mike Johnson"
                  secondary="Last Visit: 2024-04-23"
                />
              </ListItem>
            </List>
          </CardContent>
        </Card>
      </Box>
      <Box sx={{ flex: 1 }}>
        <Card>
          <CardHeader title="Upcoming Appointments" />
          <CardContent>
            <List>
              <ListItem>
                <ListItemText
                  primary="Sarah Wilson"
                  secondary="Today, 2:00 PM"
                />
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText
                  primary="Tom Brown"
                  secondary="Tomorrow, 10:30 AM"
                />
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText
                  primary="Emily Davis"
                  secondary="Apr 28, 3:15 PM"
                />
              </ListItem>
            </List>
          </CardContent>
        </Card>
      </Box>
    </Stack>
  );

  const renderPatientDashboard = () => {
    if (loading) return <Typography>Loading patient data...</Typography>;
    if (error) return <Typography color="error">{error}</Typography>;
    if (!patientData) return <Typography>No patient data found.</Typography>;
    const visits = Array.isArray(patientData.visits) ? patientData.visits : [];
    return (
      <Stack spacing={3} direction={isMobile ? 'column' : 'row'}>
        <Box sx={{ flex: 1 }}>
          <Card>
            <CardHeader title="My Medical Info" />
            <CardContent>
              <Typography variant="h6">Name: {patientData.FullName || `${patientData.FirstName} ${patientData.LastName}`}</Typography>
              <Typography>Date of Birth: {patientData.DateOfBirth}</Typography>
              <Typography>Gender: {patientData.Gender}</Typography>
              <Typography>Contact: {patientData.ContactNumber}</Typography>
              <Typography>Address: {typeof patientData.Address === 'string' ? patientData.Address : JSON.stringify(patientData.Address)}</Typography>
              <Typography>Primary Diagnosis: {patientData.PrimaryDiagnosis}</Typography>
              <Typography>Active Ward: {patientData.ActiveWard}</Typography>
              <Typography>Medical Alerts: {Array.isArray(patientData.MedicalAlerts) ? patientData.MedicalAlerts.join(', ') : patientData.MedicalAlerts}</Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ flex: 1 }}>
          <Card>
            <CardHeader title="Visit History" />
            <CardContent>
              {visits.length === 0 ? (
                <Typography>No visit history found.</Typography>
              ) : (
                <List>
                  {visits.map((visit: any, idx: number) => (
                    <React.Fragment key={idx}>
                      <ListItem alignItems="flex-start">
                        <ListItemText
                          primary={`Hospital: ${visit.hospital || 'N/A'}`}
                          secondary={
                            <>
                              <Typography component="span" variant="body2" color="text.primary">
                                Status: {visit.status || 'N/A'}<br />
                                Diagnosis: {visit.diagnosis || 'N/A'}<br />
                                Location: {visit.location || 'N/A'}<br />
                                Medical Alerts: {Array.isArray(visit.medical_alerts) ? visit.medical_alerts.join(', ') : visit.medical_alerts || 'N/A'}<br />
                                Admission Date: {visit.admission_date || 'N/A'}<br />
                                Discharge Date: {visit.discharge_date || 'N/A'}
                              </Typography>
                            </>
                          }
                        />
                      </ListItem>
                      <Divider component="li" />
                    </React.Fragment>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>
        </Box>
      </Stack>
    );
  };

  const getDashboardContent = () => {
    switch (user?.role) {
      case 'admin':
        return renderAdminDashboard();
      case 'doctor':
        return renderDoctorDashboard();
      case 'patient':
        return renderPatientDashboard();
      default:
        return null;
    }
  };

  return (
    <DashboardLayout title="Dashboard">
      <Box sx={{ flexGrow: 1 }}>
        {getDashboardContent()}
      </Box>
    </DashboardLayout>
  );
}; 