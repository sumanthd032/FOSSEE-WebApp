import axios from 'axios';

// Create axios instance
const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export const api = {
    // Auth Endpoints
    login: (username, password) => apiClient.post('/login/', { username, password }),
    register: (username, password) => apiClient.post('/register/', { username, password }),

    // Data Endpoints
    uploadFile: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        return apiClient.post('/upload/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
    },
    getDashboardData: () => apiClient.get('/dashboard/'),
    getHistory: () => apiClient.get('/history/'),
    downloadPDF: () => apiClient.get('/report/pdf/', { responseType: 'blob' }),
};

export default api;