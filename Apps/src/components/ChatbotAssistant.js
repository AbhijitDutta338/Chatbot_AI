import React, { useState, useRef, useEffect } from 'react';
import { Box, Paper, Typography, TextField, IconButton, CircularProgress, Stack, Modal } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

const ChatBubble = ({ message, isUser }) => (
  <Box display="flex" justifyContent={isUser ? 'flex-end' : 'flex-start'} mb={1}>
    <Paper
      elevation={2}
      sx={{
        p: 1.5,
        maxWidth: 320,
        bgcolor: isUser ? 'primary.main' : 'grey.100',
        color: isUser ? 'primary.contrastText' : 'text.primary',
        borderRadius: isUser ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
      }}
    >
      <Typography variant="body1">{message.text}</Typography>
      <Typography variant="caption" color="text.secondary" sx={{ float: 'right' }}>
        {message.time}
      </Typography>
    </Paper>
  </Box>
);

const ChatbotAssistant = ({ open, onClose }) => {
  const [chat, setChat] = useState([
    { text: 'Hi! How can I help you today?', isUser: false, time: '09:00' },
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (open) {
      chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chat, isTyping, open]);

  const handleSend = () => {
    if (!input.trim()) return;
    const now = new Date();
    const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setChat(prev => [...prev, { text: input, isUser: true, time }]);
    setInput('');
    setIsTyping(true);
    setTimeout(() => {
      setChat(prev => [...prev, { text: 'This is a mock bot reply.', isUser: false, time }]);
      setIsTyping(false);
    }, 1200);
  };

  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter') handleSend();
  };

  return (
    <Modal open={open} onClose={onClose} sx={{ zIndex: 1500 }}>
      <Box
        sx={{
          position: 'fixed',
          bottom: 0,
          left: 0,
          right: 0,
          mx: 'auto',
          width: '100vw',
          maxWidth: 430,
          height: '70vh',
          bgcolor: '#f5f5f5',
          borderRadius: '16px 16px 0 0',
          boxShadow: 24,
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <Typography variant="h6" p={2} bgcolor="primary.main" color="primary.contrastText" sx={{ borderRadius: '16px 16px 0 0' }}>
          Chatbot Assistant
        </Typography>
        <Box flex={1} overflow="auto" px={2} py={1}>
          {chat.map((msg, idx) => (
            <ChatBubble key={idx} message={msg} isUser={msg.isUser} />
          ))}
          {isTyping && (
            <Box display="flex" alignItems="center" mb={1}>
              <CircularProgress size={18} sx={{ mr: 1 }} />
              <Typography variant="body2" color="text.secondary">Bot is typing...</Typography>
            </Box>
          )}
          <div ref={chatEndRef} />
        </Box>
        <Box p={2} borderTop={1} borderColor="grey.200" bgcolor="#fff">
          <Stack direction="row" spacing={1}>
            <TextField
              fullWidth
              size="small"
              placeholder="Type your message..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleInputKeyDown}
              disabled={isTyping}
            />
            <IconButton color="primary" onClick={handleSend} disabled={isTyping || !input.trim()}>
              <SendIcon />
            </IconButton>
          </Stack>
        </Box>
      </Box>
    </Modal>
  );
};

export default ChatbotAssistant;
