// Base URL for the API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:10000';




/**
 * Login user by sending credentials to the API
 * @param {Object} data - The user credentials (e.g., { email, password })
 * @returns {Promise<any>} - The server's response data
 * @throws {Error} - Throws an error if the request fails
 */
export const loginUser = async (data) => {
  try {
    // Make the POST request using Fetch API
    const response = await fetch(`${API_BASE_URL}/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data), // Convert data object to JSON string
    });

    if (!response.ok) {
      // Throw an error if the HTTP status code indicates failure
      throw new Error(`Request failed with status ${response.status}`);
    }

    // Parse and return the response JSON
    return await response.json();
  } catch (error) {
    // Re-throw the error to propagate it to the caller
    throw error;
  }
};





/**
 * Logout user by sending a POST request to the API
 * @param {string} token - The user's token for authentication
 * @returns {Promise<any>} - The server's response data
 * @throws {Error} - Throws an error if the token is missing or the request fails
 */
export const logoutUser = async (token) => {
  try {
    // Validate that a token is provided
    if (!token) {
      throw new Error('Token is missing. Cannot log out.');
    }

    // Make the POST request to the logout endpoint
    const response = await fetch(`${API_BASE_URL}/users/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({ token }), // Send the token in the request body
    });

    // Check if the response indicates a failure
    if (!response.ok) {
      const errorDetails = await response.json();
      console.error('Logout failed:', errorDetails); // Log the error details for debugging
      throw new Error(`Logout failed: ${errorDetails.detail || 'Unknown error'}`);
    }

    // Parse and return the JSON response
    return await response.json();
  } catch (error) {
    // Log and propagate the error
    console.error('Error during logout:', error);
    throw error;
  }
};






/**
 * Register a new user by sending user details to the API
 * @param {Object} data - The user data to register (e.g., { name, email, password })
 * @returns {Promise<any>} - The server's response data
 * @throws {Error} - Throws an error if the registration fails
 */
export const registerUser = async (data) => {
  try {
    // Make the POST request to the registration endpoint
    const response = await fetch(`${API_BASE_URL}/users/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Ensure JSON format for request body
      },
      body: JSON.stringify(data), // Convert the data object to JSON string
    });

    // Check if the response indicates failure
    if (!response.ok) {
      throw new Error('Registration failed'); // Throw a general error for non-200 responses
    }

    // Parse and return the JSON response
    return await response.json();
  } catch (error) {
    // Propagate the error to the caller
    throw error;
  }
};





/**
 * Fetch user details using the provided token
 * @param {string} token - The user's authentication token
 * @returns {Promise<any>} - The user's details from the server
 * @throws {Error} - Throws an error if the request fails
 */
export const fetchUserData = async (token) => {
  try {
    // Validate the token before making the request
    if (!token) {
      throw new Error('Token is required to fetch user details.');
    }

    // Make the GET request to fetch user details
    const response = await fetch(`${API_BASE_URL}/users/user-details?token=${encodeURIComponent(token)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json', // Ensure the request is in JSON format
        Accept: 'application/json', // Expect JSON response
      },
    });

    // Check if the response indicates failure
    if (!response.ok) {
      throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }

    // Parse and return the JSON response
    return await response.json();
  } catch (error) {
    // Propagate the error to the caller
    throw error;
  }
};








/**
 * Fetch available data plans from the API
 * @returns {Promise<any>} - An array of data plans from the server
 * @throws {Error} - Throws an error if the request fails
 */
export const fetchDataPlans = async () => {
  try {
    // Make the GET request to fetch data plans
    const response = await fetch(`${API_BASE_URL}/packages`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json', // Ensure request is in JSON format
        Accept: 'application/json', // Expect JSON response
      },
    });

    // Check if the response indicates failure
    if (!response.ok) {
      throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }

    // Parse and return the JSON response
    return await response.json();
  } catch (error) {
    // Propagate the error to the caller
    throw error;
  }
};








/**
 * Send a password reset link to the user's email
 * @param {string} email - The email address of the user
 * @returns {Promise<any>} - The server's response data
 * @throws {Error} - Throws an error if the request fails
 */
export const sendResetLink = async (email) => {
  try {
    // Make the POST request to send the reset link
    const response = await fetch(`${API_BASE_URL}/users/ask-for-password-reset`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Ensure the request is in JSON format
        Accept: 'application/json', // Expect JSON response
      },
      body: JSON.stringify({ email }), // Include the email in the request body
    });

    // Check if the response indicates failure
    if (!response.ok) {
      throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }

    // Parse and return the JSON response
    return await response.json();
  } catch (error) {
    // Log the error for debugging and propagate it to the caller
    console.error('Error sending reset link:', error);
    throw error;
  }
};







/**
 * Reset the user's password using the provided token and new password
 * @param {Object} data - The data containing the token and the new password (e.g., { token, newPassword })
 * @returns {Promise<any>} - The server's response data
 * @throws {Error} - Throws an error if the request fails
 */
export const resetPassword = async (data) => {
  try {
    // Make the POST request to reset the password
    const response = await fetch(`${API_BASE_URL}/users/confirm-reset-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Ensure the request is in JSON format
        Accept: 'application/json', // Expect JSON response
      },
      body: JSON.stringify(data), // Include the token and new password in the request body
    });

    // Check if the response indicates failure
    if (!response.ok) {
      throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }

    // Parse and return the JSON response
    return await response.json();
  } catch (error) {
    // Log the error for debugging and propagate it to the caller
    console.error('Error resetting password:', error);
    throw error;
  }
};








/**
 * Update the password for an authenticated user in the personal area
 * @param {Object} data - The data required for updating the password (e.g., { oldPassword, newPassword })
 * @returns {Promise<any>} - The server's response data
 * @throws {Error} - Throws an error if the request fails
 */
export const updatePassword = async (data) => {
  try {
    // Make the POST request to update the password
    const response = await fetch(`${API_BASE_URL}/users/change-password-authenticated`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Ensure JSON format for the request body
      },
      body: JSON.stringify(data), // Convert the data object to a JSON string
    });

    // Check if the response indicates failure
    if (!response.ok) {
      const errorDetails = await response.json(); // Extract error details from the response
      console.error('Error details:', errorDetails); // Log the error details for debugging
      throw new Error(errorDetails.detail || 'Password update failed'); // Throw detailed or general error
    }

    // Parse and return the JSON response
    return await response.json();
  } catch (error) {
    // Log and propagate the error
    console.error('Error updating password:', error);
    throw error;
  }
};







/**
 * Add a new customer to the database
 * @param {Object} data - The customer data to be added (e.g., { name, email, phone })
 * @returns {Promise<any>} - The server's response data
 * @throws {Error} - Throws an error if the request fails
 */
export const addCustomer = async (data) => {
  try {
    // Make the POST request to add a new customer
    const response = await fetch(`${API_BASE_URL}/customers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Ensure the request body is JSON formatted
      },
      body: JSON.stringify(data), // Convert the customer data to JSON string
    });

    // Check if the response indicates failure
    if (!response.ok) {
      const errorDetails = await response.json(); // Extract error details from the response
      console.error('Error adding customer:', errorDetails); // Log error details for debugging
      throw new Error(errorDetails.message || 'Failed to add customer.'); // Use detailed or general error message
    }

    // Parse and return the JSON response
    return await response.json();
  } catch (error) {
    // Log and propagate the error
    console.error('Error in addCustomer API:', error);
    throw error;
  }
};







/**
 * Search for customers based on a search query
 * @param {string} query - The search query to filter customers
 * @returns {Promise<any>} - The server's response data containing matching customers
 * @throws {Error} - Throws an error if the request fails
 */
export const searchCustomers = async (query) => {
  try {
    // Make the POST request to search for customers
    const response = await fetch(`${API_BASE_URL}/customers/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Ensure the request body is JSON formatted
      },
      body: JSON.stringify({ query }), // Send the search query in the request body
    });

    // Check if the response indicates failure
    if (!response.ok) {
      const errorDetails = await response.json(); // Extract error details from the response
      console.error('Error fetching customer search results:', errorDetails); // Log error details
      throw new Error(errorDetails.message || 'Failed to fetch customer search results.'); // Use detailed or general error message
    }

    // Parse and return the JSON response
    return await response.json();
  } catch (error) {
    // Log and propagate the error
    console.error('Error in searchCustomers API:', error);
    throw error;
  }
};







/**
 * Send a contact message through the "Contact Us" form
 * @param {Object} data - The data to be sent in the contact message (e.g., { name, email, message })
 * @returns {Promise<any>} - The server's response data
 * @throws {Error} - Throws an error if the request fails
 */
export const sendContactMessage = async (data) => {
  try {
    // Make the POST request to send the contact message
    const response = await fetch(`${API_BASE_URL}/contact-us-send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Ensure the request body is JSON formatted
      },
      body: JSON.stringify(data), // Convert the contact data to a JSON string
    });

    // Check if the response indicates failure
    if (!response.ok) {
      const errorDetails = await response.json(); // Extract error details from the response
      console.error('Error sending contact message:', errorDetails); // Log error details
      throw new Error(errorDetails.message || 'Failed to send contact message.'); // Use detailed or general error message
    }

    // Parse and return the JSON response
    return await response.json();
  } catch (error) {
    // Log and propagate the error
    console.error('Error sending contact message:', error);
    throw error;
  }
};
