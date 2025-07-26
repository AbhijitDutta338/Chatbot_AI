import React from 'react';
import { Card, CardContent, Typography, Chip, Stack } from '@mui/material';

const IncidentCard = ({ type, time, location }) => (
  <Card
    variant="outlined"
    sx={{
      mb: 2,
      width: '100%',
      height: 120,
      maxWidth: 180,
      minWidth: 120,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'stretch',
      boxSizing: 'border-box',
    }}
  >
    <CardContent>
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Typography variant="subtitle1" fontWeight={600}>{type}</Typography>
        <Chip label={time} size="small" color="info" />
      </Stack>
      <Typography variant="body2" color="text.secondary">Location: {location}</Typography>
    </CardContent>
  </Card>
);

export default IncidentCard;
