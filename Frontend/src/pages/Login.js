import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../assets/styles/Login.css';
import { loginUser } from '../services/api'; // Import the API function

function Login({ onLogin }) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username_or_email: '',
    password: '',
    remember_me: false, // Default value
  });

  // Map of error codes to user-friendly messages
  const errorMessages = {
    400: 'Invalid input detected. Please check your details.',
    401: 'Invalid username or password.',
    403: 'Your account is locked due to multiple failed login attempts.',
    409: 'User is already logged in from another device.',
    500: 'An internal server error occurred. Please try again later.',
  };

  // Update form data state on input change
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior

    try {
      // Call the API function
      const response = await loginUser(formData);
      // Call the onLogin function passed as a prop
      onLogin(response.token); // Pass the token to App.js for context update
      navigate('/'); // Redirect to home page
    } catch (error) {
      const status = error.response?.status;
      const message = errorMessages[status] || 'An unexpected error occurred.';
      alert(message);
    }
  };

  return (
    <div id="login-page" className="login-page">
      <div id="login-container" className="container">
        {/* Page Title */}
        <div id="login-title" className="title">Login</div>

        {/* Form Container */}
        <div id="login-content" className="content">
          <form id="login-form" onSubmit={handleSubmit}>
            {/* User Input Fields */}
            <div id="user-details" className="user-details">
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
                onClick={() => navigate('/forgot-password')}
              />
            </div>
            <div id="register-button" className="logButton">
              <input
                type="button"
                value="Don't have an account? Register here"
                onClick={() => navigate('/register')}
              />
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
