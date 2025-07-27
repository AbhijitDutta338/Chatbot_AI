
import React, { useState } from 'react';
import { Box, Typography, AppBar, Toolbar, IconButton, Paper, Fab, Grid, Tabs, Tab } from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';
import ChatIcon from '@mui/icons-material/Chat';
import IncidentList from '../components/IncidentList';
import Map from '../components/Map';
import BottomNav from '../components/BottomNav';
import ChatbotAssistant from '../components/ChatbotAssistant';
import Heatmap from '../components/Heatmap';

const mockEvent = {
  name: 'Google Agentic AI Day',
  date: '2025-07-26',
  venue: 'Bangalore International Exhibition Centre (BIEC)',
};

const mockIncidents = [
  { type: 'Medical', time: '10:15', location: 'Gate 2' },
  { type: 'Panic', time: '10:30', location: 'Main Stage' },
  { type: 'Lost', time: '10:45', location: 'Food Court' },
  { type: 'Security', time: '11:00', location: 'VIP Area' },
  { type: 'Medical', time: '11:10', location: 'Stands' },
  { type: 'Security', time: '11:20', location: 'Parking' },
];

const INCIDENT_CATEGORIES = ['Medical', 'Lost', 'Panic', 'Security'];

const AdminDashboard = () => {
  const [chatbotOpen, setChatbotOpen] = useState(false);
  const [tab, setTab] = useState(0);
  const handleTabChange = (e, newValue) => setTab(newValue);
  const filteredIncidents = mockIncidents.filter(
    inc => inc.type.toLowerCase() === INCIDENT_CATEGORIES[tab].toLowerCase()
  );
  return (
    <Box sx={{ minHeight: '100vh', bgcolor: '#f5f5f5', width: '100vw', maxWidth: 430, mx: 'auto', position: 'relative' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>Event Overview</Typography>
          <IconButton color="inherit">
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      <Box component="main" sx={{ flexGrow: 1, px: 2, pt: 1, pb: 8 }}>
        <Paper sx={{ p: 1.5, mb: 2, borderRadius: 2 }}>
          <Typography variant="subtitle1" sx={{ fontSize: '1rem', fontWeight: 600 }}>{mockEvent.name}</Typography>
          <Typography variant="body2" sx={{ fontSize: '0.95rem' }}>Date: {mockEvent.date}</Typography>
          <Typography variant="body2" sx={{ fontSize: '0.95rem' }}>Venue: {mockEvent.venue}</Typography>
        </Paper>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Paper sx={{ p: 1.5, minHeight: 220, display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 2, borderRadius: 2 }}>
              <Box sx={{ width: '100%', height: '180px', maxWidth: '100vw' }}>
                <Heatmap />
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="h6" mb={1}>Reported Incidents</Typography>
            <Paper sx={{ mb: 2, borderRadius: 2 }}>
              <Tabs
                value={tab}
                onChange={handleTabChange}
                variant="scrollable"
                scrollButtons="auto"
                aria-label="incident category tabs"
                sx={{ borderBottom: 1, borderColor: 'divider' }}
              >
                {INCIDENT_CATEGORIES.map((cat, idx) => (
                  <Tab key={cat} label={cat} />
                ))}
              </Tabs>
              <Box p={2}>
                {filteredIncidents.length === 0 ? (
                  <Typography variant="body2" color="text.secondary">No incidents in this category.</Typography>
                ) : (
                  <IncidentList incidents={filteredIncidents} />
                )}
              </Box>
            </Paper>
          </Grid>
        </Grid>
        <Fab color="primary" sx={{ position: 'fixed', bottom: 80, right: 20, zIndex: 1000 }} aria-label="chatbot" onClick={() => setChatbotOpen(true)}>
          <ChatIcon sx={{ fontSize: 28 }} />
        </Fab>
        <ChatbotAssistant open={chatbotOpen} onClose={() => setChatbotOpen(false)} />
      </Box>
      <BottomNav />
    </Box>
  );
};

export default AdminDashboard;
