import React, { useState } from 'react';
import { Box, Typography, Button, Stack } from '@mui/material';
import ReportIncidentModal from '../components/ReportIncidentModal';
import ChatbotAssistant from '../components/ChatbotAssistant';
import CrowdMeter from '../components/CrowdMeter';
import TicketCard from '../components/TicketCard';
import BottomNav from '../components/BottomNav';
import Map from '../components/Map';

const InviteeHome = () => {
  const [reportOpen, setReportOpen] = useState(false);
  const [chatbotOpen, setChatbotOpen] = useState(false);
  return (
    <Box minHeight="100vh" bgcolor="#f5f5f5" pb={7}>
      <Box bgcolor="primary.main" color="primary.contrastText" p={2}>
        <Typography variant="h6">Google Agentic AI Day</Typography>
      </Box>
      <Map />
      <Stack direction="row" spacing={2} justifyContent="center" my={2}>
        <Button variant="contained" color="primary">Now</Button>
        <Button variant="outlined" color="primary">Next</Button>
        <Button variant="outlined" color="primary">Later</Button>
      </Stack>
      <Box px={2}>
        <CrowdMeter value={68} />
        <TicketCard eventName="Google Agentic AI day" date="2025-07-26" />
        <Stack direction="row" spacing={2} justifyContent="center" mt={2}>
          <Button variant="contained" color="error" onClick={() => setReportOpen(true)}>HELP</Button>
          <Button variant="contained" color="primary" onClick={() => setChatbotOpen(true)}>CHAT</Button>
        </Stack>
      </Box>
      <ReportIncidentModal open={reportOpen} onClose={() => setReportOpen(false)} />
      <ChatbotAssistant open={chatbotOpen} onClose={() => setChatbotOpen(false)} />
      <BottomNav />
    </Box>
  );
};

export default InviteeHome;
