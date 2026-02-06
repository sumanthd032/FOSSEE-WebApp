import axios from 'axios';

// Create an axios instance with base configuration
const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000/api', 
    headers: {
        'Content-Type': 'application/json',
    },
});

// Define API endpoints
export const api = {
    // Upload CSV File
    uploadFile: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        return apiClient.post('/upload/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
    },

    // Get Dashboard Data (Charts + Table)
    getDashboardData: async () => {
        return apiClient.get('/dashboard/');
    },

    // Get Upload History
    getHistory: async () => {
        return apiClient.get('/history/');
    },

    downloadPDF: async () => {
        return apiClient.get('/report/pdf/', {
            responseType: 'blob', 
        });
    },

}

export default api;