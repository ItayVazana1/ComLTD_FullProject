import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import { resetPassword } from '../services/api'; // Import API function
import '../assets/styles/SetNewPass.css'; // Reuse the same CSS file

function ResetPassword() {
  const navigate = useNavigate(); // Initialize navigate function
  const [formData, setFormData] = useState({
    reset_token: '',
    new_password: '',
    confirm_password: '',
  }); // State to store form input data

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    try {
      console.log('Submitting reset password data:', formData); // Debug log
      const response = await resetPassword(formData); // Call API
      console.log('Reset password response:', response); // Debug log

      if (response.status === 'success') {
        navigate('/login'); // Navigate to Login page
      } else {
        alert('Failed to reset password. Please check your inputs.');
      }
    } catch (error) {
      console.error('Error resetting password:', error);
      alert('Failed to reset password. Please try again.');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value }); // Update form data state
  };

  return (
    <div id="reset-password-page" className="forgot-password-page">
      <div id="forgot-password-container" className="container">
        <div id="forgot-password-title" className="title">Reset Your Password</div>

        {/* Form for resetting password */}
        <form id="forgot-password-form" onSubmit={handleSubmit}>
          <div id="forgot-password-user-details" className="user-details">
            <div id="forgot-password-email-box" className="input-box">
              <span id="forgot-password-email-label" className="details">Reset Token</span>
              <input
                id="reset-token-input"
                type="text"
                name="reset_token"
                placeholder="Enter your reset token"
                value={formData.reset_token}
                onChange={handleInputChange} // Update token state on change
                required
              />
            </div>
            <div id="forgot-password-email-box" className="input-box">
              <span id="forgot-password-email-label" className="details">New Password</span>
              <input
                id="new-password-input"
                type="password"
                name="new_password"
                placeholder="Enter your new password"
                value={formData.new_password}
                onChange={handleInputChange} // Update new password state on change
                required
              />
            </div>
            <div id="forgot-password-email-box" className="input-box">
              <span id="forgot-password-email-label" className="details">Confirm New Password</span>
              <input
                id="confirm-password-input"
                type="password"
                name="confirm_password"
                placeholder="Confirm your new password"
                value={formData.confirm_password}
                onChange={handleInputChange} // Update confirm password state on change
                required
              />
            </div>
          </div>
          <div id="forgot-password-submit-button" className="subButton">
            <input type="submit" value="Reset Password" />
          </div>
        </form>
      </div>
    </div>
  );
}

export default ResetPassword;
