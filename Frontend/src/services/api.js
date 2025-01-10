import axios from 'axios';

// Create an Axios instance
const api = axios.create({
    baseURL: 'http://localhost:8000', // Update this to your backend URL
    timeout: 5000, // 5 seconds timeout
    headers: {
        'Content-Type': 'application/json',
    },
});


// Login function
export const login = async (username, password) => {
    try {
        const response = await api.post('/auth/login', {
            username,
            password,
        });
        return response.data; // Return the server's response
    } catch (error) {
        console.warn(
            'Backend is not available. Fallback to auto-login for development purposes.'
        );
        // Fallback: Return mock data
        return {
            username: username,
            token: 'mock-token-for-development',
        };
    }
};


// Logout function
export const logout = async (username) => {
    try {
      const response = await api.post('/auth/logout', { username });
      console.log('Logout response:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error during logout:', error);
      throw error;
    }
  };
  


export default api;