import React, { useState } from 'react';
import { Box, Snackbar, Alert } from '@mui/material';
import IncidentForm from './IncidentForm';

const ReportIncident = () => {
  const [open, setOpen] = useState(false);

  const handleSubmit = (data) => {
    // Mock save logic
    setOpen(true);
    // You can log or process data here
  };

  return (
    <Box minHeight="100vh" bgcolor="#f5f5f5" display="flex" flexDirection="column" justifyContent="center" alignItems="center">
      <IncidentForm onSubmit={handleSubmit} />
      <Snackbar open={open} autoHideDuration={2000} onClose={() => setOpen(false)} anchorOrigin={{ vertical: 'top', horizontal: 'center' }}>
        <Alert severity="success" sx={{ width: '100%' }}>
          Incident reported!
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default ReportIncident;
