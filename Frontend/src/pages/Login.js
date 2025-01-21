import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // For navigation between pages
import '../assets/styles/Login.css'; // Import CSS for styling
import { loginUser } from '../services/api'; // API function to handle user login

/**
 * Login Component:
 * Provides a login form for users to authenticate themselves.
 * @param {Function} onLogin - Function to handle login and update user context
 */
function Login({ onLogin }) {
  const navigate = useNavigate(); // Enables navigation between pages

  // State to store form input data
  const [formData, setFormData] = useState({
    username_or_email: '', // Username or email input
    password: '', // Password input
    remember_me: false, // Default value for "Remember me" checkbox
  });

  // Map error status codes to user-friendly messages
  const errorMessages = {
    400: 'Invalid input detected. Please check your details.',
    401: 'Invalid username or password.',
    403: 'Your account is locked due to multiple failed login attempts.',
    409: 'User is already logged in from another device.',
    500: 'An internal server error occurred. Please try again later.',
  };

  /**
   * Handle input changes for form fields
   * @param {Event} e - Input change event
   */
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value, // Update state for text or checkbox inputs
    });
  };

  /**
   * Handle form submission to log in the user
   * @param {Event} e - Form submission event
   */
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior

    try {
      // Call the API function to authenticate the user
      const response = await loginUser(formData);
      // Use the onLogin prop to update the user context with the token
      onLogin(response.token);
      navigate('/'); // Redirect to the home page upon successful login
    } catch (error) {
      // Handle API error responses
      const status = error.response?.status;
      const message = errorMessages[status] || 'An unexpected error occurred.';
      alert(message); // Display the error message to the user
    }
  };

  return (
    <div id="login-page" className="login-page">
      <div id="login-container" className="container">
        {/* Page Title */}
        <div id="login-title" className="title">Login</div>

        {/* Login Form */}
        <div id="login-content" className="content">
          <form id="login-form" onSubmit={handleSubmit}>
            {/* User Input Fields */}
            <div id="user-details" className="user-details">
              {/* Username or Email Input */}
              <div id="username-box" className="input-box">
                <span id="username-label" className="details">Username or Email</span>
                <input
                  id="username-input"
                  type="text"
                  name="username_or_email"
                  placeholder="Enter your username or email"
                  value={formData.username_or_email}
                  onChange={handleInputChange}
                  required
                />
              </div>
              {/* Password Input */}
              <div id="password-box" className="input-box">
                <span id="password-label" className="details">Password</span>
                <input
                  id="password-input"
                  type="password"
                  name="password"
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>

            {/* Remember Me Checkbox */}
            <div id="remember-box" className="validBox">
              <label id="remember-label" className="checkbox-container">
                <input
                  id="remember-checkbox"
                  type="checkbox"
                  name="remember_me"
                  checked={formData.remember_me}
                  onChange={handleInputChange}
                />
                <span className="details">Remember me</span>
              </label>
            </div>

            {/* Submit Button */}
            <div id="submit-button" className="subButton">
              <input type="submit" value="Login" />
            </div>

            {/* Forgot Password and Register Buttons */}
            <div id="forgot-password-button" className="logButton">
              <input
                type="button"
                value="Forgot Password?"
                onClick={() => navigate('/forgot-password')} // Navigate to forgot password page
              />
            </div>
            <div id="register-button" className="logButton">
              <input
                type="button"
                value="Don't have an account? Register here"
                onClick={() => navigate('/register')} // Navigate to register page
              />
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
