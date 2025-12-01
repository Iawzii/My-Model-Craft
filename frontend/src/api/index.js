import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000
})

// 请求拦截器：添加JWT token（从localStorage）
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response,
  error => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      '请求失败'
    const err = new Error(message)
    err.original = error
    return Promise.reject(err)
  }
)

export default api

export const modelsApi = {
  recommend: () => api.get('/api/models/recommend'),
  search: (params) => api.get('/api/search', { params }),
  getById: (id) => api.get(`/api/models/${id}`)
}

export const authApi = {
  sendCode: (email) => api.post('/api/auth/send-code', { email }),
  register: (payload) => api.post('/api/auth/register', payload),
  login: (payload) => api.post('/api/auth/login', payload),
  forgotPassword: (email) => api.post('/api/auth/forgot', { email }),
  resetPassword: (payload) => api.post('/api/auth/reset', payload),
  uploadAvatar: (formData) =>
    api.post('/api/settings/user/avatar/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),
  updateProfile: (payload) => api.patch('/api/settings/user', payload),
  updateUsername: (payload) => api.patch('/api/settings/user/username', payload),
  updateEmail: (payload) => api.patch('/api/settings/user/email', payload),
  updateAvatar: (payload) => api.patch('/api/settings/user/avatar', payload),
  updateBio: (payload) => api.patch('/api/settings/user/bio', payload),
  changePassword: (payload) => api.post('/api/settings/user/password', payload)
}