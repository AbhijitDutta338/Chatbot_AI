import React, { useState, useRef, useEffect } from 'react';
import { Box, Snackbar, Alert, Modal, Paper, Typography, IconButton } from '@mui/material';
import IncidentForm from '../components/IncidentForm';
import CloseIcon from '@mui/icons-material/Close';


const ReportIncidentModal = ({ open, onClose }) => {
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const modalRef = useRef(null);

  const handleSubmit = (data) => {
    setSnackbarOpen(true);
    // You can log or process data here
    setTimeout(() => {
      setSnackbarOpen(false);
      onClose();
    }, 1500);
  };

  return (
    <Modal
      open={open}
      onClose={onClose}
      sx={{ zIndex: 1500 }}
      disableEnforceFocus
    >
      <Box
        sx={{
          position: 'fixed',
          bottom: 0,
          left: 0,
          right: 0,
          mx: 'auto',
          width: '100vw',
          maxWidth: 430,
          height: '80vh',
          bgcolor: '#f5f5f5',
          borderRadius: '16px 16px 0 0',
          boxShadow: 24,
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <Paper elevation={0} sx={{ p: 2, borderRadius: '16px 16px 0 0', bgcolor: 'primary.main', color: 'primary.contrastText', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Typography variant="h6">Report Incident</Typography>
          <IconButton onClick={onClose} sx={{ color: 'primary.contrastText' }}>
            <CloseIcon />
          </IconButton>
        </Paper>
        <Box flex={1} overflow="auto" px={2} py={1}>
          <IncidentForm onSubmit={handleSubmit} />
        </Box>
        <Snackbar open={snackbarOpen} autoHideDuration={1200} onClose={() => setSnackbarOpen(false)} anchorOrigin={{ vertical: 'top', horizontal: 'center' }}>
          <Alert severity="success" sx={{ width: '100%' }}>
            Incident reported!
          </Alert>
        </Snackbar>
      </Box>
    </Modal>
  );
};

export default ReportIncidentModal;
