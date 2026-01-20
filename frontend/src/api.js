import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to include the auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export const auth = {
    login: (email, password) => api.post('/auth/login', { email, password }),
    register: (data) => api.post('/auth/register', data),
    me: () => api.get('/auth/me'),
};

export const resume = {
    upload: (formData) => api.post('/api/upload-resume', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    }),
};

export const job = {
    extract: (text) => api.post('/api/submit-jd', null, { params: { jd_text: text } }),
};

export const generator = {
    create: (data) => api.post('/api/generate-cover-letter', data),
};

export const user = {
    getHistory: () => api.get('/api/get-history'),
};

export default api;
