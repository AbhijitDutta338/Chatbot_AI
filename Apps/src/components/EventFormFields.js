import React from 'react';
import { TextField, MenuItem, Stack, Box, Button, Typography } from '@mui/material';

const categories = [
  { value: 'Music', label: 'Music' },
  { value: 'Sports', label: 'Sports' },
  { value: 'Conference', label: 'Conference' },
  { value: 'Other', label: 'Other' },
];

const EventFormFields = ({ values, onChange }) => (
  <Stack spacing={2}>
    <TextField
      label="Event Name"
      name="name"
      value={values.name}
      onChange={onChange}
      required
    />
    <TextField
      label="Location"
      name="location"
      value={values.location}
      onChange={onChange}
      required
    />
    <TextField
      label="Start Date & Time"
      name="startDate"
      type="datetime-local"
      value={values.startDate}
      onChange={onChange}
      InputLabelProps={{ shrink: true }}
      required
      fullWidth
    />
    <TextField
      label="End Date & Time"
      name="endDate"
      type="datetime-local"
      value={values.endDate}
      onChange={onChange}
      InputLabelProps={{ shrink: true }}
      required
      fullWidth
    />
    <Box>
      <Typography variant="subtitle2" mb={0.5}>
        Upload Event Mapping JSON
      </Typography>
      <Button
        variant="outlined"
        component="label"
        fullWidth
        sx={{ justifyContent: 'flex-start', textTransform: 'none' }}
      >
        {values.jsonFile ? values.jsonFile.name : 'Upload File'}
        <input
          type="file"
          accept="application/json"
          hidden
          name="jsonFile"
          onChange={onChange}
        />
      </Button>
    </Box>
  </Stack>
);

export default EventFormFields;
