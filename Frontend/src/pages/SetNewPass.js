import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // For navigation after successful reset
import { resetPassword } from '../services/api'; // API call for password reset
import '../assets/styles/SetNewPass.css'; // CSS for styling the component

/**
 * ResetPassword Component:
 * Handles the process of resetting a user's password.
 */
function ResetPassword() {
  const navigate = useNavigate(); // Initialize navigate for redirection
  const [formData, setFormData] = useState({
    reset_token: '',
    new_password: '',
    confirm_password: '',
  }); // State to store form input data

  /**
   * Handles form submission for password reset
   * @param {Event} e - Form submission event
   */
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form behavior (page reload)
    try {
      console.log('Submitting reset password data:', formData); // Debugging log
      const response = await resetPassword(formData); // API call to reset password
      console.log('Reset password response:', response); // Debugging log

      if (response.status === 'success') {
        navigate('/login'); // Navigate to the login page upon success
      } else {
        alert('Failed to reset password. Please check your inputs.'); // Handle API failure
      }
    } catch (error) {
      console.error('Error resetting password:', error); // Log the error
      alert('Failed to reset password. Please try again.'); // User-friendly error message
    }
  };

  /**
   * Handles input change for form fields
   * @param {Event} e - Input change event
   */
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value }); // Update state with the new value
  };

  return (
    <div id="reset-password-page" className="forgot-password-page">
      <div id="forgot-password-container" className="container">
        <div id="forgot-password-title" className="title">Reset Your Password</div>

        {/* Form for resetting the user's password */}
        <form id="forgot-password-form" onSubmit={handleSubmit}>
          <div id="forgot-password-user-details" className="user-details">
            {/* Reset Token Input */}
            <div id="forgot-password-email-box" className="input-box">
              <span id="forgot-password-email-label" className="details">Reset Token</span>
              <input
                id="reset-token-input"
                type="text"
                name="reset_token"
                placeholder="Enter your reset token"
                value={formData.reset_token}
                onChange={handleInputChange} // Update token state
                required
              />
            </div>
            {/* New Password Input */}
            <div id="forgot-password-email-box" className="input-box">
              <span id="forgot-password-email-label" className="details">New Password</span>
              <input
                id="new-password-input"
                type="password"
                name="new_password"
                placeholder="Enter your new password"
                value={formData.new_password}
                onChange={handleInputChange} // Update new password state
                required
              />
            </div>
            {/* Confirm Password Input */}
            <div id="forgot-password-email-box" className="input-box">
              <span id="forgot-password-email-label" className="details">Confirm New Password</span>
              <input
                id="confirm-password-input"
                type="password"
                name="confirm_password"
                placeholder="Confirm your new password"
                value={formData.confirm_password}
                onChange={handleInputChange} // Update confirm password state
                required
              />
            </div>
          </div>
          {/* Submit Button */}
          <div id="forgot-password-submit-button" className="subButton">
            <input type="submit" value="Reset Password" />
          </div>
        </form>
      </div>
    </div>
  );
}

export default ResetPassword;
