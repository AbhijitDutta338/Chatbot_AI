import React from 'react';
import { Box } from '@mui/material';
import RoomIcon from '@mui/icons-material/Room';

const EventMap = () => (
  <Box display="flex" alignItems="center" justifyContent="center" height={180} bgcolor="#e3e3e3" borderRadius={2} my={2}>
    <RoomIcon sx={{ fontSize: 48, color: 'primary.main' }} />
  </Box>
);

export default EventMap;
