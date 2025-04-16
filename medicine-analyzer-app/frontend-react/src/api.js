import axios from 'axios';

const API = axios.create({
  baseURL: 'https://your-backend-url.onrailway.app', // Replace with real backend URL
});

export const analyzeImage = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return API.post('/analyze-image/', formData);
};

export const translateText = (original_text, language) => {
  const formData = new FormData();
  formData.append('original_text', original_text);
  formData.append('language', language);
  return API.post('/translate/', formData);
};