import React, { useState, useCallback, useEffect } from 'react';
import {
  Container, Box, TextField, Button, Typography,
  Paper, Alert, CircularProgress, Grid,
  FormControl, InputLabel, MenuItem, Select,
  Accordion, AccordionSummary, AccordionDetails,
  List, ListItemButton, ListItemText, FormHelperText
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import SendIcon from '@mui/icons-material/Send';
import { useApi } from './hooks/useApi';
import ChatWindow from './components/ChatWindow';

function App() {
  const [messages, setMessages] = useState([]);
  const [responses, setResponses] = useState([]);
  const { loading, error, callApi } = useApi();

  const [formData, setFormData] = useState({
    username: '', display_name: '', profile: '',
    chatTitle: '', chatUserIds: [],
    providerName: '', apiEndpoint: '', apiKey: '',
    llmName: '', userInput: ''
  });

  const [users, setUsers] = useState([]);
  const [chats, setChats] = useState([]);
  const [providers, setProviders] = useState([]);
  const [llms, setLlms] = useState([]);

  const [selectedUser, setSelectedUser] = useState(null);
  const [selectedChat, setSelectedChat] = useState(null);
  const [selectedProvider, setSelectedProvider] = useState(null);
  const [selectedLlm, setSelectedLlm] = useState(null);

  const handleInputChange = useCallback((e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }, []);

  const fetchList = useCallback(async (endpoint, setter, key) => {
    try {
      const response = await callApi(endpoint, {}, 'GET');
      if (response.status === 'success') {
        setter(response.data[key] || []);
      } else {
        console.error(`Error fetching ${key}:`, response.message);
      }
    } catch (err) {
      console.error(`Failed to fetch ${key}:`, err);
    }
  }, [callApi]);

  useEffect(() => {
    fetchList('/user/list', setUsers, 'users');
    fetchList('/chat/list', setChats, 'chats');
    fetchList('/llm_provider/list', setProviders, 'providers');
    fetchList('/llm/list', setLlms, 'llms');
  }, [fetchList]);

  useEffect(() => {
    if (selectedUser) {
      callApi(`/user/${selectedUser.user_id}`, {}, 'GET')
        .then((response) => {
          if (response.status === 'success') {
            setSelectedUser((prev) => ({ ...prev, ...response.data.user }));
          }
        })
        .catch((err) => console.error('Error fetching user details:', err));
      
      callApi(`/chat/user/${selectedUser.user_id}`, {}, 'GET')
        .then((response) => {
          if (response.status === 'success') {
            setChats(response.data.chats);
          }
        })
        .catch((err) => console.error('Error loading chats:', err));
    }
  }, [selectedUser, callApi]);

  useEffect(() => {
    if (selectedChat) {
      callApi(`/chat/id/${selectedChat.chat_id}`, {}, 'GET')
        .then((response) => {
          if (response.status === 'success') {
            const chatHistory = response.data.chat.messages.map(msg => ({
              sender: msg.role === 'user' ? 'user' : 'llm',
              text: msg.content,
              timestamp: new Date(msg.created_at).toLocaleString()
            }));
            setMessages(chatHistory);
          }
        })
        .catch((err) => console.error('Error loading chat history:', err));
    } else {
      setMessages([]);
    }
  }, [selectedChat, selectedUser, callApi]);

  useEffect(() => {
    if (selectedProvider) {
      callApi(`/llm/llm_provider/${selectedProvider.provider_id}`, {}, 'GET')
        .then((response) => {
          if (response.status === 'success') {
            setLlms(response.data.llms);
          }
        })
        .catch((err) => console.error('Error loading LLMs:', err));
    }
  }, [selectedProvider, callApi]);

  const handleApiCall = useCallback(async (endpoint, data) => {
    try {
      const response = await callApi(endpoint, data);
      const timestamp = new Date().toISOString();

      setResponses((prev) => [
        { timestamp, endpoint, status: response.status, message: response.message, data: response.data },
        ...prev
      ]);

      if (response.status === 'success') {
        switch (endpoint) {
          case '/llm/response_generate':
            setMessages((prev) => [
              ...prev,
              { sender: 'user', text: data.user_input, timestamp: new Date().toLocaleString() },
              { sender: 'llm', text: response.data.llm_response.content, timestamp: new Date().toLocaleString() }
            ]);
            break;
          
          case '/user/create':
            await fetchList('/user/list', setUsers, 'users');
            setFormData((prev) => ({ ...prev, username: '', display_name: '', profile: '' }));
            break;
          case '/chat/create':
            await fetchList('/chat/list', setChats, 'chats');
            setFormData((prev) => ({ ...prev, chatTitle: '', chatUserIds: [] }));
            break;
          case '/llm_provider/add':
            await fetchList('/llm_provider/list', setProviders, 'providers');
            setFormData((prev) => ({ ...prev, providerName: '', apiEndpoint: '', apiKey: '' }));
            break;
          case '/llm/add':
            await fetchList('/llm/list', setLlms, 'llms');
            setFormData((prev) => ({ ...prev, llmName: '' }));

            if (selectedProvider && selectedProvider.name === data.provider_name) {
              const response = await callApi(`/llm/llm_provider/${selectedProvider.provider_id}`, {}, 'GET');
              if (response.status === 'success') {
                setLlms(response.data.llms || []);
              }
              else {
                console.error('Error loading LLMs:', response.message);
                setLlms([]);
              }
            }
            break;
        }
      }
    } catch (err) {
      console.error('Error during API call:', err);
    }
  }, [callApi]);

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
      <Grid item xs={12} md={4}>
          {/* User Management */}
          <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">User Management</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <TextField
                  label="Username"
                  name="username"
                  value={formData.username}
                  onChange={handleInputChange}
                  required
                />
                <TextField
                  label="Display Name (Optional)"
                  name="display_name"
                  value={formData.display_name}
                  onChange={handleInputChange}
                />
                <TextField
                  label="Profile"
                  name="profile"
                  value={formData.profile}
                  onChange={handleInputChange}
                  multiline
                  rows={3}
                />
                <Button
                  variant="contained"
                  onClick={() => handleApiCall('/user/create', {
                    username: formData.username,
                    display_name: formData.display_name,
                    profile: formData.profile
                  })}
                  disabled={loading || !formData.username}
                >
                  Create User
                </Button>
                <List>
                  {users.map((user) => (
                    <ListItemButton key={user.user_id}>
                      <ListItemText
                        primary={user.display_name || user.username}
                        secondary={user.profile || ''}
                      />
                    </ListItemButton>
                  ))}
                </List>
              </Box>
            </AccordionDetails>
          </Accordion>

          {/* Chat Management */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">Chat Management</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <TextField
                  label="Chat Title"
                  name="chatTitle"
                  value={formData.chatTitle}
                  onChange={handleInputChange}
                  required
                />
                <FormControl fullWidth>
                  <InputLabel>Users</InputLabel>
                  <Select
                    name="chatUserIds"
                    multiple
                    value={formData.chatUserIds || []}
                    onChange={(e) => setFormData((prev) => ({ ...prev, chatUserIds: e.target.value }))}
                    renderValue={(selected) => {
                      return users
                        .filter(user => selected.includes(user.user_id))
                        .map(user => user.username)
                        .join(', ');
                    }}
                  >
                    {users.map((user) => (
                      <MenuItem key={user.user_id} value={user.user_id}>
                        {user.username}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <Button
                  variant="contained"
                  onClick={() => handleApiCall('/chat/create', {
                    title: formData.chatTitle,
                    user_ids: formData.chatUserIds
                  })}
                  disabled={loading || !formData.chatTitle || !(formData.chatUserIds?.length > 0)}
                >
                  Create Chat
                </Button>
                <List>
                  {chats.map((chat) => (
                    <ListItemButton key={chat.chat_id}>
                      <ListItemText 
                        primary={chat.title}
                        secondary={chat.users?.map(user => user.username).join(', ')}
                      />
                    </ListItemButton>
                  ))}
                </List>
              </Box>
            </AccordionDetails>
          </Accordion>

          {/* LLM Provider Management */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">LLM Provider Management</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <TextField
                  label="Provider Name"
                  name="providerName"
                  value={formData.providerName}
                  onChange={handleInputChange}
                  required
                />
                <TextField
                  label="API Endpoint"
                  name="apiEndpoint"
                  value={formData.apiEndpoint}
                  onChange={handleInputChange}
                />
                <TextField
                  label="API Key (Optional)"
                  name="apiKey"
                  value={formData.apiKey || ''}
                  onChange={handleInputChange}
                  type="password"
                  helperText="Leave empty if not required"
                />
                <Button
                  variant="contained"
                  onClick={() => handleApiCall('/llm_provider/add', {
                    name: formData.providerName,
                    api_endpoint: formData.apiEndpoint,
                    api_key: formData.apiKey || undefined
                  })}
                  disabled={loading || !formData.providerName}
                >
                  Add Provider
                </Button>
                <List>
                  {providers.map((provider) => (
                    <ListItemButton key={provider.provider_id}>
                      <ListItemText primary={provider.name} />
                    </ListItemButton>
                  ))}
                </List>
              </Box>
            </AccordionDetails>
          </Accordion>

          {/* LLM Management */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">LLM Management</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <FormControl fullWidth>
                  <InputLabel>Provider Name</InputLabel>
                  <Select
                    name="providerId"
                    value={formData.providerId}
                    onChange={(e) => setFormData((prev) => ({ ...prev, providerId: e.target.value }))}
                  >
                    {providers.map((provider) => (
                      <MenuItem key={provider.provider_id} value={provider.provider_id}>
                        {provider.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <TextField
                  label="LLM Name"
                  name="llmName"
                  value={formData.llmName}
                  onChange={handleInputChange}
                  required
                />
                <Button
                  variant="contained"
                  onClick={() => handleApiCall('/llm/add', {
                    provider_id: formData.providerId,
                    llm_name: formData.llmName
                  })}
                  disabled={loading || !formData.llmName || !formData.providerId}
                >
                  Add LLM
                </Button>
                <List>
                  {llms.map((llm) => (
                    <ListItemButton key={llm.llm_id}>
                      <ListItemText primary={llm.name} />
                    </ListItemButton>
                  ))}
                </List>
              </Box>
            </AccordionDetails>
          </Accordion>
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, mb: 3 }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mb: 3 }}>
              <Typography variant="h6">Chat Configuration</Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <FormControl fullWidth>
                    <InputLabel>User</InputLabel>
                    <Select
                      value={selectedUser?.username || ''}
                      onChange={(e) => {
                        const user = users.find((u) => u.username === e.target.value);
                        setSelectedUser(user || null);
                        setSelectedChat(null);
                      }}
                    >
                      <MenuItem value="" disabled>Select a user</MenuItem>
                      {users.map((user) => (
                        <MenuItem key={user.user_id} value={user.username}>
                          {user.username}
                        </MenuItem>
                      ))}
                    </Select>
                    <FormHelperText>Select a user to start chat</FormHelperText>
                  </FormControl>
                </Grid>

                <Grid item xs={6}>
                  <FormControl fullWidth>
                    <InputLabel>Chat</InputLabel>
                    <Select
                      value={selectedChat?.title || ''}
                      onChange={(e) => {
                        const chat = chats.find((c) => c.title === e.target.value);
                        setSelectedChat(chat || null);
                      }}
                    >
                      <MenuItem value="" disabled>Select a chat</MenuItem>
                      {chats.map((chat) => (
                        <MenuItem key={chat.chat_id} value={chat.title}>
                          {chat.title}
                        </MenuItem>
                      ))}
                    </Select>
                    <FormHelperText>
                      {!selectedUser ? 'Select a user first' :
                      Array.isArray(chats) && chats.length === 0 ? 'No chats available' : 
                      'Select a chat'}
                    </FormHelperText>
                  </FormControl>
                </Grid>

                <Grid item xs={6}>
                  <FormControl fullWidth>
                    <InputLabel>Provider</InputLabel>
                    <Select
                      value={selectedProvider?.name || ''}
                      onChange={(e) => {
                        const provider = providers.find((p) => p.name === e.target.value);
                        setSelectedProvider(provider || null);
                        setSelectedLlm(null);
                      }}
                    >
                      <MenuItem value="" disabled>Select a provider</MenuItem>
                      {providers.map((provider) => (
                        <MenuItem key={provider.provider_id} value={provider.name}>
                          {provider.name}
                        </MenuItem>
                      ))}
                    </Select>
                    <FormHelperText>Select a provider</FormHelperText>
                  </FormControl>
                </Grid>

                <Grid item xs={6}>
                  <FormControl fullWidth>
                    <InputLabel>LLM Model</InputLabel>
                    <Select
                      value={selectedLlm?.name || ''}
                      onChange={(e) => {
                        const llm = llms.find((l) => l.name === e.target.value);
                        setSelectedLlm(llm || null);
                      }}
                    >
                      <MenuItem value="" disabled>Select a LLM</MenuItem>
                      {llms.map((llm) => (
                        <MenuItem key={llm.llm_id} value={llm.name}>
                          {llm.name}
                        </MenuItem>
                      ))}
                    </Select>
                    <FormHelperText>
                      {!selectedProvider ? 'Select a provider first' :
                      Array.isArray(llms) && llms.length === 0 ? 'No models available' :
                      'Select a LLM'}
                    </FormHelperText>
                  </FormControl>
                </Grid>
              </Grid>
            </Box>
            
            <ChatWindow messages={messages} />
            <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
              <TextField
                fullWidth
                label="Message"
                name="userInput"
                value={formData.userInput}
                onChange={handleInputChange}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey && selectedUser && selectedChat && selectedProvider && selectedLlm) {
                    e.preventDefault();
                    handleApiCall('/llm/response_generate', {
                      user_id: selectedUser.user_id,
                      chat_id: selectedChat.chat_id,
                      provider_id: selectedProvider.provider_id,
                      llm_id: selectedLlm.llm_id,
                      user_input: formData.userInput
                    });
                    setFormData((prev) => ({ ...prev, userInput: '' }));
                  }
                }}
              />
              <Button
                variant="contained"
                endIcon={<SendIcon />}
                onClick={() => {
                  handleApiCall('/llm/response_generate', {
                    user_id: selectedUser.user_id,
                    chat_id: selectedChat.chat_id,
                    provider_id: selectedProvider.provider_id,
                    llm_id: selectedLlm.llm_id,
                    user_input: formData.userInput
                  });
                  setFormData((prev) => ({ ...prev, userInput: '' }));
                }}
                disabled={!selectedUser || !selectedChat || !selectedProvider || !selectedLlm || loading}
              >
                Send
              </Button>
            </Box>
          </Paper>

          {error && <Alert severity="error">{error}</Alert>}
          
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">Response History</Typography>
            </AccordionSummary>
            <AccordionDetails>
              {responses.map((item, index) => (
                <Box key={index} sx={{ mt: 2 }}>
                  <Typography variant="subtitle2">Endpoint: {item.endpoint}</Typography>
                  <Typography variant="caption" display="block">
                    {new Date(item.timestamp).toLocaleString()}
                  </Typography>
                  <Typography color={item.status === 'success' ? 'primary' : 'error'}>
                    Status: {item.status} - {item.message}
                  </Typography>
                  <pre style={{ margin: 0, overflowX: 'auto', background: '#f5f5f5', padding: 1 }}>
                    {JSON.stringify(item.data, null, 2)}
                  </pre>
                </Box>
              ))}
            </AccordionDetails>
          </Accordion>
        </Grid>
      </Grid>

      {loading && <CircularProgress sx={{ position: 'fixed', bottom: 20, right: 20, zIndex: 2000 }} />}
    </Container>
  );
}

export default App;