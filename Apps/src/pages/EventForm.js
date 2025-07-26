import React, { useState } from 'react';
import { Box, Paper, Typography, Button, Snackbar, Alert } from '@mui/material';
import EventFormFields from '../components/EventFormFields';
import { useNavigate } from 'react-router-dom';

const initialState = {
  name: '',
  location: '',
  startDate: '',
  endDate: '',
  jsonFile: null,
};

const EventForm = () => {

  const [values, setValues] = useState(initialState);
  const [submitting, setSubmitting] = useState(false);
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  const handleChange = e => {
    if (e.target.type === 'file') {
      setValues({ ...values, jsonFile: e.target.files[0] });
    } else {
      setValues({ ...values, [e.target.name]: e.target.value });
    }
  };

  const handleSubmit = e => {
    e.preventDefault();
    setSubmitting(true);
    setTimeout(() => {
      setOpen(true);
      setSubmitting(false);
      setValues(initialState);
      navigate('/admin');
    }, 1200);
  };

  return (
    <Box minHeight="100vh" bgcolor="#f5f5f5" pb={7}>
      <Box bgcolor="primary.main" color="primary.contrastText" p={2}>
        <Typography variant="h6">Book-My-Event</Typography>
      </Box>
      <Box display="flex" justifyContent="center" alignItems="center" mt={2}>
        <Paper sx={{ p: 2, width: '100%', maxWidth: 400, borderRadius: 3 }}>
          <Typography variant="h6" mb={2}>Create Event</Typography>
          <form onSubmit={handleSubmit}>
            <EventFormFields values={values} onChange={handleChange} />
            <Button type="submit" variant="contained" fullWidth sx={{ mt: 3 }} disabled={submitting}>
              {submitting ? 'Submitting...' : 'Submit'}
            </Button>
          </form>
        </Paper>
      </Box>
      <Snackbar open={open} autoHideDuration={2000} onClose={() => setOpen(false)} anchorOrigin={{ vertical: 'top', horizontal: 'center' }}>
        <Alert severity="success" sx={{ width: '100%' }}>
          Event created!
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default EventForm;
