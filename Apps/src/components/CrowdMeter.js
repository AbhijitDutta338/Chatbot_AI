import React from 'react';
import { Box, LinearProgress, Typography } from '@mui/material';

const CrowdMeter = ({ value }) => (
  <Box my={2}>
    <Typography variant="body2" mb={0.5}>Crowd Level</Typography>
    <LinearProgress variant="determinate" value={value} sx={{ height: 10, borderRadius: 5 }} />
    <Typography variant="caption" color="text.secondary">{value}% full</Typography>
  </Box>
);

export default CrowdMeter;
