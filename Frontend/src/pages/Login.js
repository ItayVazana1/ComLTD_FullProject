import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../assets/styles/Login.css';

function Login({ onLogin }) {
  const navigate = useNavigate();
  const [username, setUsername] = useState(''); // State to store username

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent default form submission
    if (username.trim() === '') {
      alert('Please enter a username.');
      return;
    }
    onLogin(username); // Pass username to App.js
    navigate('/'); // Redirect to the Home page
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
                <span id="username-label" className="details">Username</span>
                <input
                  id="username-input"
                  type="text"
                  placeholder="Enter your username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)} // Update username state
                  required
                />
              </div>
              <div id="password-box" className="input-box">
                <span id="password-label" className="details">Password</span>
                <input
                  id="password-input"
                  type="password"
                  placeholder="Enter your password"
                  required
                />
              </div>
            </div>

            {/* Remember Me Checkbox */}
            <div id="remember-box" className="validBox">
              <label id="remember-label" className="checkbox-container">
                <input id="remember-checkbox" type="checkbox" />
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
