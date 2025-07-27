import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import AdminDashboard from './pages/AdminDashboard';
import InviteeHome from './pages/InviteeHome';
import ResponderDashboard from './pages/ResponderDashboard';
import EventForm from './pages/EventForm';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/invitee" element={<InviteeHome />} />
        <Route path="/responder" element={<ResponderDashboard />} />
        <Route path="/" element={<EventForm />} />
        <Route path="*" element={<AdminDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
