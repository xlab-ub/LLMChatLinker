// src/hooks/useApi.js
import { useState, useCallback } from 'react';
import axios from 'axios';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const callApi = useCallback(async (endpoint, data = {}, method = 'POST') => {
    setLoading(true);
    setError(null);
    try {
      let response;
      if (method === 'GET') {
        response = await axios.get(`${apiUrl}${endpoint}`);
      } else {
        response = await axios.post(`${apiUrl}${endpoint}`, data);
      }
      setLoading(false);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.message || 'An error occurred');
      setLoading(false);
      throw err;
    }
  }, [apiUrl]);

  return { loading, error, callApi };
};