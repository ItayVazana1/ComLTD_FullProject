import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import '../assets/styles/ResetPassword.css';
import { useUser } from '../context/UserContext'; // Access UserContext
import { updatePassword } from '../services/api'; // Import API function

function ResetPassword({ onLogout }) {
  const { userData } = useUser(); // Access UserContext
  const [formData, setFormData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  });
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(''); // Reset message
    setLoading(true);
  
    try {
      // Include username from UserContext
      const payload = {
        ...formData,
        username: userData?.username, // Make sure this field exists
      };
  
      const response = await updatePassword(payload); // Call API
      console.log('Password update response:', response);
  
      if (response.status === 'success') {
        setFormData({
          current_password: '',
          new_password: '',
          confirm_password: '',
        });
        alert('Password updated successfully.');
      } else {
        alert(response.message || 'Failed to reset password. Please try again.');
      }
    } catch (error) {
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
      setLoading(false);
    }
  };

  return (
    <div id="reset-password-container-online">
      {/* Navbar */}
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />

      {/* Main Content */}
      <div id="reset-password-content-online" className="d-flex">
        <Sidebar />
        <main id="reset-password-main-online" className="col-md-9 col-lg-10 p-4">
          <h1 id="reset-password-title-online">Change Your Password</h1>
          <form id="reset-password-form-online" onSubmit={handleSubmit}>
            {message && <div id="reset-password-message-online">{message}</div>}
            <input
              id="current-password-online"
              type="password"
              name="current_password"
              placeholder="Current Password"
              value={formData.current_password}
              onChange={handleInputChange}
              required
            />
            <input
              id="new-password-online"
              type="password"
              name="new_password"
              placeholder="New Password"
              value={formData.new_password}
              onChange={handleInputChange}
              required
            />
            <input
              id="confirm-password-online"
              type="password"
              name="confirm_password"
              placeholder="Confirm New Password"
              value={formData.confirm_password}
              onChange={handleInputChange}
              required
            />
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
