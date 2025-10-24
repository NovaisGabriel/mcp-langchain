import axios from 'axios';
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000/api';

export const postMessage = (text) => axios.post(`${API_BASE}/messages`, { text }).then(r => r.data);
export const analyzeMessage = (id, tasks) => axios.post(`${API_BASE}/messages/${id}/analyze`, { tasks }).then(r => r.data);
export const getMessage = (id) => axios.get(`${API_BASE}/messages/${id}`).then(r => r.data);
export const listMessages = () => axios.get(`${API_BASE}/messages`).then(r => r.data);
