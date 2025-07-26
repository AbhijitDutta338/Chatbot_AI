import React from 'react';
import { Card, CardContent, Typography, Chip, Stack, Button } from '@mui/material';

const TaskCard = ({ task, onAccept, onResolve }) => (
  <Card variant="outlined" sx={{ mb: 2 }}>
    <CardContent>
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Typography variant="subtitle1" fontWeight={600}>{task.title}</Typography>
        <Chip label={task.urgency} color={task.urgency === 'High' ? 'error' : 'warning'} size="small" />
      </Stack>
      <Typography variant="body2" color="text.secondary">{task.details}</Typography>
      <Stack direction="row" spacing={1} mt={2}>
        <Button size="small" variant="outlined" color="primary" onClick={onAccept}>Accept</Button>
        <Button size="small" variant="contained" color="success" onClick={onResolve}>Resolve</Button>
      </Stack>
    </CardContent>
  </Card>
);

export default TaskCard;
