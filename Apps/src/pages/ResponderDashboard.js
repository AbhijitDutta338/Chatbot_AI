import React, { useState } from 'react';
import { Box, Typography, AppBar, Toolbar, IconButton, Fab, Stack } from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';
import MyLocationIcon from '@mui/icons-material/MyLocation';
import TaskCard from '../components/TaskCard';
import Map from '../components/Map';
import BottomNav from '../components/BottomNav';
import ReportIncidentModal from '../components/ReportIncidentModal';

const mockTasks = [
  { title: 'Assist Medical Emergency', urgency: 'High', details: 'Near Gate 2' },
  { title: 'Lost Child', urgency: 'Medium', details: 'Food Court' },
];

const ResponderDashboard = () => {
  const [tasks, setTasks] = useState(mockTasks);
  const [reportOpen, setReportOpen] = useState(false);

  const handleAccept = idx => {
    // Mock accept logic
    alert('Task accepted!');
  };
  const handleResolve = idx => {
    setTasks(prev => prev.filter((_, i) => i !== idx));
  };

  return (
    <Box minHeight="100vh" bgcolor="#f5f5f5">
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>Responder Dashboard</Typography>
          <IconButton color="inherit">
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      <Box p={2}>
        <Typography variant="h6" mb={2}>Assigned Tasks</Typography>
        <Stack spacing={2}>
          {tasks.map((task, idx) => (
            <TaskCard key={idx} task={task} onAccept={() => handleAccept(idx)} onResolve={() => handleResolve(idx)} />
          ))}
        </Stack>
        <br/>
        <Map />
        <Stack direction="row" spacing={2} justifyContent="center" mt={2}>
          <Fab color="error" variant="extended" onClick={() => setReportOpen(true)} sx={{ minWidth: 120 }}>
            Report Incident
          </Fab>
        </Stack>
      </Box>
      <ReportIncidentModal open={reportOpen} onClose={() => setReportOpen(false)} />
      <Fab color="primary" sx={{ position: 'fixed', bottom: 80, right: 32 }} aria-label="location">
        <MyLocationIcon />
      </Fab>
      <BottomNav />
    </Box>
  );
};

export default ResponderDashboard;
