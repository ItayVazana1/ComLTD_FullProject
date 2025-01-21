import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // For navigation between pages
import { sendResetLink } from '../services/api'; // API function to send password reset link
import '../assets/styles/ForgotPassword.css'; // CSS for styling the component

/**
 * ForgotPassword Component:
 * Allows users to request a password reset link by providing their email address.
 */
function ForgotPassword() {
  const navigate = useNavigate(); // Initialize navigation function
  const [email, setEmail] = useState(''); // State to store email input

  /**
   * Handle sending the reset link when the form is submitted
   * @param {Event} e - Form submission event
   */
  const handleSendLink = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior

    try {
      console.log('Sending reset link for email:', email); // Debugging log
      const response = await sendResetLink(email); // Call the API function to send the reset link
      console.log('Reset link response:', response); // Debugging log

      if (response.status === 'success') {
        // Navigate to the next step where the user enters the token and new password
        navigate('/insert-token-and-pass');
      } else {
        // Handle API response failure
        alert('Failed to send reset link. Please try again.');
      }
    } catch (error) {
      // Handle errors from the API call
      console.error('Error sending reset link:', error);
      alert('Failed to send reset link. Please try again.');
    }
  };

  /**
   * Handle input change for the email field
   * @param {Event} e - Input change event
   */
  const handleInputChange = (e) => {
    setEmail(e.target.value); // Update the email state with the input value
  };

  return (
    <div id="forgot-password-page" className="forgot-password-page">
      <div id="forgot-password-container" className="container">
        {/* Page Title */}
        <div id="forgot-password-title" className="title">Forgot Password</div>

        {/* Form for sending the reset link */}
        <form id="forgot-password-form" onSubmit={handleSendLink}>
          <div id="forgot-password-user-details" className="user-details">
            {/* Email Input */}
            <div id="forgot-password-email-box" className="input-box">
              <span id="forgot-password-email-label" className="details">Email</span>
              <input
                id="forgot-password-email-input"
                type="email"
                name="email"
                placeholder="Enter your email"
                value={email} // Controlled input value
                onChange={handleInputChange} // Update email state on change
                required // Mark field as required
              />
            </div>
          </div>
          {/* Submit Button */}
          <div id="forgot-password-submit-button" className="subButton">
            <input type="submit" value="Send Reset Link" />
          </div>
        </form>
      </div>
    </div>
  );
}

export default ForgotPassword;
