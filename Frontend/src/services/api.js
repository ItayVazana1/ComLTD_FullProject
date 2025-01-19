import axios from 'axios';

// Base URL for the API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:10000';

// Create an Axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Login user
export const loginUser = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/users/login`, data, {
      headers: { 'Content-Type': 'application/json' },
    });
    return response.data; // Return the response data
  } catch (error) {
    throw error; // Propagate the error
  }
};


// Logout user
export const logoutUser = async (token) => {
  try {
    if (!token) {
      throw new Error('Token is missing. Cannot log out.');
    }

    const response = await fetch(`${process.env.REACT_APP_API_URL}/users/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({ token }),
    });

    if (!response.ok) {
      const errorDetails = await response.json();
      console.error('Logout failed:', errorDetails);
      throw new Error(`Logout failed: ${errorDetails.detail || 'Unknown error'}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error during logout:', error);
    throw error;
  }
};

// Register user
export const registerUser = async (data) => {
  try {
    const response = await fetch(`${process.env.REACT_APP_API_URL}/users/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Registration failed');
    }

    return await response.json();
  } catch (error) {
    throw error; // Allow the caller to handle the error
  }
};

// Fetch user details
export const fetchUserData = async (token) => {
  try {
    const response = await fetch(`${API_BASE_URL}/users/user-details?token=${token}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json', 
      },
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }
    return await response.json(); // Parse JSON response
  } catch (error) {
    throw error; // Allow the caller to handle the error
  }
};

// Fetch data plans
export const fetchDataPlans = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/packages`);
    return response.data; // Return the array of plans
  } catch (error) {
    throw error; // Allow the caller to handle the error
  }
};

// Forgot password - ask for token to email
export const sendResetLink = async (email) => {
  try {
    const response = await apiClient.post('/users/ask-for-password-reset', { email });
    return response.data; // Return response data
  } catch (error) {
    console.error('Error sending reset link:', error);
    throw error; // Propagate the error
  }
};

// Forgot password - use the token received to set new password
export const resetPassword = async (data) => {
  try {
    const response = await apiClient.post('/users/confirm-reset-password', data);
    return response.data; // Return response data
  } catch (error) {
    console.error('Error resetting password:', error);
    throw error; // Propagate the error
  }
};

// Update password - change password for online user in the personal area of the application
export const updatePassword = async (data) => {
  try {
    const response = await fetch(`${process.env.REACT_APP_API_URL}/users/change-password-authenticated`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data), // Ensure data includes username
    });

    if (!response.ok) {
      const errorDetails = await response.json();
      console.error('Error details:', errorDetails);
      throw new Error(errorDetails.detail || 'Password update failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Error updating password:', error);
    throw error;
  }
};

// Add customer - add customer to the DB 
export const addCustomer = async (data) => {
  try {
    const response = await fetch(`${process.env.REACT_APP_API_URL}/customers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorDetails = await response.json();
      console.error('Error adding customer:', errorDetails);
      throw new Error(errorDetails.message || 'Failed to add customer.');
    }

    return await response.json(); // Return the parsed response
  } catch (error) {
    console.error('Error in addCustomer API:', error);
    throw error;
  }
};

// Search customers - fetch customers based on search query
export const searchCustomers = async (query) => {
  try {
    const response = await apiClient.post('/customers/search', {
      query, // Send query in the request body
    });
    return response.data; // Return response data
  } catch (error) {
    console.error('Error fetching customer search results:', error);
    throw error;
  }
};


// Contact us (email)
export const sendContactMessage = async (data) => {
  try {
    const response = await apiClient.post('/contact-us-send', data);
    return response.data; // Return the response data
  } catch (error) {
    console.error('Error sending contact message:', error);
    throw error; // Propagate the error
  }
};
