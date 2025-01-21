import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import '../assets/styles/ResetPassword.css'; // Import CSS for styling
import { useUser } from '../context/UserContext'; // Access UserContext for global user data
import { updatePassword } from '../services/api'; // API function to update password

/**
 * ResetPassword Component:
 * Allows logged-in users to reset their passwords while authenticated.
 * @param {Function} onLogout - Function to handle user logout
 */
function ResetPassword({ onLogout }) {
  const { userData } = useUser(); // Access user data from context
  const [formData, setFormData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  }); // State to manage form input data
  const [message, setMessage] = useState(''); // State to store feedback messages
  const [loading, setLoading] = useState(false); // State to manage loading spinner

  /**
   * Handle input change for the form
   * @param {Event} e - Input change event
   */
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value }); // Update form data state
  };

  /**
   * Handle form submission to update the password
   * @param {Event} e - Form submission event
   */
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page reload on form submission
    setMessage(''); // Clear any previous messages
    setLoading(true); // Show loading spinner

    try {
      // Construct payload including username
      const payload = {
        ...formData,
        username: userData?.username, // Ensure username is included
      };

      const response = await updatePassword(payload); // Call API to update password
      console.log('Password update response:', response); // Debugging log

      if (response.status === 'success') {
        // Reset form fields upon success
        setFormData({
          current_password: '',
          new_password: '',
          confirm_password: '',
        });
        alert('Password updated successfully.'); // Show success message
      } else {
        // Handle API failure response
        alert(response.message || 'Failed to reset password. Please try again.');
      }
    } catch (error) {
      // Log the error and set appropriate feedback messages
      console.error('Error resetting password:', error);
      const status = error.response?.status;
      switch (status) {
        case 400:
          setMessage('Invalid input. Please check your details.');
          break;
        case 404:
          setMessage('User not found.');
          break;
        case 500:
          setMessage('Internal server error. Please try again later.');
          break;
        default:
          setMessage('An unknown error occurred.');
      }
    } finally {
      setLoading(false); // Hide loading spinner
    }
  };

  return (
    <div id="reset-password-container-online">
      {/* Navbar */}
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />

      {/* Main Content Area */}
      <div id="reset-password-content-online" className="d-flex">
        <Sidebar />
        <main id="reset-password-main-online" className="col-md-9 col-lg-10 p-4">
          <h1 id="reset-password-title-online">Change Your Password</h1>

          {/* Password Reset Form */}
          <form id="reset-password-form-online" onSubmit={handleSubmit}>
            {/* Feedback Message */}
            {message && <div id="reset-password-message-online">{message}</div>}

            {/* Current Password Input */}
            <input
              id="current-password-online"
              type="password"
              name="current_password"
              placeholder="Current Password"
              value={formData.current_password}
              onChange={handleInputChange}
              required
            />

            {/* New Password Input */}
            <input
              id="new-password-online"
              type="password"
              name="new_password"
              placeholder="New Password"
              value={formData.new_password}
              onChange={handleInputChange}
              required
            />

            {/* Confirm New Password Input */}
            <input
              id="confirm-password-online"
              type="password"
              name="confirm_password"
              placeholder="Confirm New Password"
              value={formData.confirm_password}
              onChange={handleInputChange}
              required
            />

            {/* Submit Button */}
            <button
              id="reset-password-button-online"
              type="submit"
              disabled={loading}
              style={{ cursor: loading ? 'not-allowed' : 'pointer' }}
            >
              {loading ? 'Processing...' : 'Reset Password'}
            </button>
          </form>
        </main>
      </div>
    </div>
  );
}

export default ResetPassword;
