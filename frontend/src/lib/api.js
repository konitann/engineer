import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  withCredentials: true // セッション管理のためのクッキーを送信
});

export const userAPI = {
  getAll: () => api.get('/users'),
  create: (data) => api.post('/users', data),
  delete: (id) => api.delete(`/users/${id}`)
};

export const qrAPI = {
  generate: (data) => api.post('/generate-qr', data),
  sendEmail: (data) => api.post('/send-qr-email', data)
};

export const attendanceAPI = {
  check: (data) => api.post('/attendance/check', data),
  getAll: (params) => api.get('/attendance', { params })
};

export const authAPI = {
  login: (password) => api.post('/auth/login', { password }),
  logout: () => api.post('/auth/logout'),
  getStatus: () => api.get('/auth/status')
};

export default api;