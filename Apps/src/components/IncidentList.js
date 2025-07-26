import React from 'react';
import { Box, Typography } from '@mui/material';
import IncidentCard from './IncidentCard';

const IncidentList = ({ incidents }) => (
  <Box>
    
    {incidents.length === 0 ? (
      <Typography color="text.secondary">No incidents reported.</Typography>
    ) : (
      incidents.map((incident, idx) => (
        <IncidentCard key={idx} {...incident} />
      ))
    )}
  </Box>
);

export default IncidentList;
