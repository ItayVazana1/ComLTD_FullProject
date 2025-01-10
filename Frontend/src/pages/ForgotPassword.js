import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../assets/styles/ForgotPassword.css';

/**
 * ForgotPassword Component:
 * This component handles the "Forgot Password" functionality.
 * - Users can enter their email to receive a password reset link.
 * - Includes navigation back to the login page.
 */
function ForgotPassword() {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    alert('Password reset link has been sent to your email.');
    navigate('/login'); // Redirect to login page
  };

  return (
    <div id="forgot-password-page" className="forgot-password-page">
      <div id="forgot-password-container" className="container">
        {/* Page Title */}
        <div id="forgot-password-title" className="title">Forgot Password</div>

        {/* Form Container */}
        <div id="forgot-password-content" className="content">
          <form id="forgot-password-form" onSubmit={handleSubmit}>
            {/* Email Input Field */}
            <div id="forgot-password-user-details" className="user-details">
              <div id="forgot-password-email-box" className="input-box">
                <span id="forgot-password-email-label" className="details">Email</span>
                <input
                  id="forgot-password-email-input"
                  type="email"
                  placeholder="Enter your email"
                  required
                />
              </div>
            </div>

            {/* Submit Button */}
            <div id="forgot-password-submit-button" className="subButton">
              <input type="submit" value="Send Reset Link" />
            </div>

            {/* Back to Login Button */}
            <div id="forgot-password-back-login-button" className="logButton">
              <input
                type="button"
                value="Back to login"
                onClick={() => navigate('/login')}
              />
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default ForgotPassword;
