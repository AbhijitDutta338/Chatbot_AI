import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import QrCode2Icon from '@mui/icons-material/QrCode2';

const TicketCard = ({ eventName, date }) => (
  <Card sx={{ mt: 2, mb: 2, p: 1, maxWidth: 340 }}>
    <CardContent>
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Box>
          <Typography variant="subtitle1" fontWeight={600}>{eventName}</Typography>
          <Typography variant="body2" color="text.secondary">{date}</Typography>
        </Box>
        <QrCode2Icon sx={{ fontSize: 48, color: 'grey.700' }} />
      </Box>
    </CardContent>
  </Card>
);

export default TicketCard;
