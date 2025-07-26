import React, { useState } from 'react';
import { Box, Button, MenuItem, TextField, Typography, Stack } from '@mui/material';
import FileUpload from './FileUpload';

const INCIDENT_TYPES = [
  { value: 'Medical', label: 'Medical' },
  { value: 'Panic', label: 'Panic' },
  { value: 'Lost', label: 'Lost' },
];

const IncidentForm = ({ onSubmit }) => {
  const [type, setType] = useState('Medical');
  const [description, setDescription] = useState('');
  const [file, setFile] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitting(true);
    setTimeout(() => {
      onSubmit({ type, description, file });
      setSubmitting(false);
      setType('Medical');
      setDescription('');
      setFile(null);
    }, 1000);
  };

  return (
    <Box component="form" onSubmit={handleSubmit} p={2}>
      <Stack spacing={2}>
        <Typography variant="h6">Report an Incident</Typography>
        <TextField
          select
          label="Type"
          value={type}
          onChange={e => setType(e.target.value)}
          required
          SelectProps={{
            MenuProps: {
              disablePortal: true
            }
          }}
        >
          {INCIDENT_TYPES.map(option => (
            <MenuItem key={option.value} value={option.value}>{option.label}</MenuItem>
          ))}
        </TextField>
        <TextField
          label="Description"
          multiline
          minRows={3}
          value={description}
          onChange={e => setDescription(e.target.value)}
          required
        />
        <FileUpload file={file} setFile={setFile} />
        <Button type="submit" variant="contained" disabled={submitting}>
          {submitting ? 'Submitting...' : 'Submit'}
        </Button>
      </Stack>
    </Box>
  );
};

export default IncidentForm;
