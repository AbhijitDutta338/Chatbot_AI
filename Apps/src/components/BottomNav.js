
import React, { useState } from 'react';
import { BottomNavigation, BottomNavigationAction, Paper } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import EventNoteIcon from '@mui/icons-material/EventNote';
import GroupsIcon from '@mui/icons-material/Groups';
import PersonIcon from '@mui/icons-material/Person';
import { useNavigate } from 'react-router-dom';

const BottomNav = () => {
  const [value, setValue] = useState(0);
  const navigate = useNavigate();

  const handleNavChange = (_, newValue) => {
    setValue(newValue);
    switch (newValue) {
      case 0:
        navigate('/admin');
        break;
      case 1:
        navigate('/invitee');
        break;
      case 2:
        navigate('/responder');
        break;
      default:
        navigate('/');
    }
  };

  return (
    <Paper sx={{ position: 'fixed', bottom: 0, left: 0, right: 0 }} elevation={3}>
      <BottomNavigation
        showLabels
        value={value}
        onChange={handleNavChange}
      >
        <BottomNavigationAction label="Admin" icon={<PersonIcon />} />
        <BottomNavigationAction label="Invitee" icon={<GroupsIcon />} />
        <BottomNavigationAction label="Responder" icon={<EventNoteIcon />} />
      </BottomNavigation>
    </Paper>
  );
};

export default BottomNav;
