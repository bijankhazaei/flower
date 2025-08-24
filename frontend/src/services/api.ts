import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const userService = {
  getAll: () => api.get('/users').then(res => res.data),
  create: (data: any) => api.post('/users', data).then(res => res.data),
  update: (id: string, data: any) => api.put(`/users/${id}`, data).then(res => res.data),
  delete: (id: string) => api.delete(`/users/${id}`).then(res => res.data),
};

export const projectService = {
  getAll: () => api.get('/projects').then(res => res.data),
  create: (data: any) => api.post('/projects', data).then(res => res.data),
  update: (id: string, data: any) => api.put(`/projects/${id}`, data).then(res => res.data),
  delete: (id: string) => api.delete(`/projects/${id}`).then(res => res.data),
  createFlow: (projectId: string, data: any) => 
    api.post(`/projects/${projectId}/flows`, data).then(res => res.data),
};

export const flowService = {
  get: (projectId: string, flowId: string) => 
    api.get(`/projects/${projectId}/flows/${flowId}`).then(res => res.data),
  save: (projectId: string, flowId: string, data: any) => 
    api.put(`/projects/${projectId}/flows/${flowId}`, data).then(res => res.data),
  execute: (projectId: string, flowId: string) => 
    api.post(`/projects/${projectId}/flows/${flowId}/execute`).then(res => res.data),
};

export default api;