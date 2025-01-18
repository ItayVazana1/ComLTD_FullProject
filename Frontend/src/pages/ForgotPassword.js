import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import { sendResetLink } from '../services/api'; // Import API function
import '../assets/styles/ForgotPassword.css';

function ForgotPassword() {
  const navigate = useNavigate(); // Initialize navigate function
  const [email, setEmail] = useState(''); // State to store email input

  const handleSendLink = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    try {
      console.log('Sending reset link for email:', email); // Debug log
      const response = await sendResetLink(email); // Call API
      console.log('Reset link response:', response); // Debug log
  
      if (response.status === 'success') {
        navigate('/insert-token-and-pass'); // Navigate to ResetPassword page
      } else {
        alert('Failed to send reset link. Please try again.');
      }
    } catch (error) {
      console.error('Error sending reset link:', error);
      alert('Failed to send reset link. Please try again.');
    }
  };

  const handleInputChange = (e) => {
    setEmail(e.target.value); // Update email state
  };

  return (
    <div id="forgot-password-page" className="forgot-password-page">
      <div id="forgot-password-container" className="container">
        <div id="forgot-password-title" className="title">Forgot Password</div>

        {/* Form for sending reset link */}
        <form id="forgot-password-form" onSubmit={handleSendLink}>
          <div id="forgot-password-user-details" className="user-details">
            <div id="forgot-password-email-box" className="input-box">
              <span id="forgot-password-email-label" className="details">Email</span>
              <input
                id="forgot-password-email-input"
                type="email"
                name="email"
                placeholder="Enter your email"
                value={email}
                onChange={handleInputChange} // Update email state on change
                required
              />
            </div>
          </div>
          <div id="forgot-password-submit-button" className="subButton">
            <input type="submit" value="Send Reset Link" />
          </div>
        </form>
      </div>
    </div>
  );
}

export default ForgotPassword;
