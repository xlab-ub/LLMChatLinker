import React, { useRef, useEffect } from 'react';
import { Paper, List, ListItem, Typography, Box } from '@mui/material';

const ChatWindow = ({ messages }) => {
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);
  const prevMessageLengthRef = useRef(messages.length);

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    // Scroll when a new chat is loaded (messages array changes completely)
    // or when a new message is added
    const isNewChat = prevMessageLengthRef.current === 0 && messages.length > 0;
    const isNewMessage = messages.length > prevMessageLengthRef.current;
    
    if (isNewChat || isNewMessage) {
      const timeoutId = setTimeout(() => {
        scrollToBottom();
      }, 100);
      return () => clearTimeout(timeoutId);
    }

    prevMessageLengthRef.current = messages.length;
  }, [messages]);

  return (
    <Paper 
      elevation={3} 
      sx={{ height: '400px', overflow: 'auto', p: 2, mb: 2 }}
      ref={chatContainerRef}
    >
      <List>
        {messages.map((message, index) => (
          <ListItem
            key={index}
            sx={{
              justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
              mb: 1
            }}
          >
            <Box
              sx={{
                maxWidth: '70%',
                backgroundColor: message.sender === 'user' ? '#1976d2' : '#f5f5f5',
                borderRadius: 2,
                p: 1
              }}
            >
              <Typography
                color={message.sender === 'user' ? 'white' : 'text.primary'}
              >
                {message.text}
              </Typography>
              <Typography
                variant="caption"
                color={message.sender === 'user' ? 'rgba(255,255,255,0.7)' : 'text.secondary'}
                sx={{ display: 'block', mt: 0.5 }}
              >
                {message.timestamp}
              </Typography>
            </Box>
          </ListItem>
        ))}
        <div ref={messagesEndRef} />
      </List>
    </Paper>
  );
};

export default ChatWindow;