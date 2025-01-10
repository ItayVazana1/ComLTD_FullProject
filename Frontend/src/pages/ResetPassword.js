import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import '../assets/styles/ResetPassword.css';

/**
 * ResetPassword Component:
 * Provides a form for choosing a new password and validating it.
 */
function ResetPassword({ username, onLogout }) {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');

  const validatePassword = (pwd) => {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(pwd);
    const hasLowerCase = /[a-z]/.test(pwd);
    const hasNumber = /[0-9]/.test(pwd);
    const hasSpecialChar = /[!@#$%^&*]/.test(pwd);

    return (
      pwd.length >= minLength &&
      hasUpperCase &&
      hasLowerCase &&
      hasNumber &&
      hasSpecialChar
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validatePassword(password)) {
      setMessage(
        'Password must be at least 8 characters long and include uppercase, lowercase, a number, and a special character.'
      );
      return;
    }

    if (password !== confirmPassword) {
      setMessage('Passwords do not match.');
      return;
    }

    setMessage('Password has been reset successfully!');
    setPassword('');
    setConfirmPassword('');
  };

  return (
    <div id="reset-password-container">
      {/* Navbar */}
      <Navbar username={username} onLogout={onLogout} />

      {/* Main Content */}
      <div id="reset-password-content" className="d-flex">
        <Sidebar />
        <main id="reset-password-main" className="col-md-9 col-lg-10 p-4">
          <h1 id="reset-password-title">Set Your New Password</h1>
          <form id="reset-password-form" onSubmit={handleSubmit}>
            {message && <div id="reset-password-message">{message}</div>}
            <input
              id="new-password"
              type="password"
              placeholder="New Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <input
              id="confirm-password"
              type="password"
              placeholder="Confirm New Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
            <button id="reset-password-button" type="submit">
              Reset Password
            </button>
          </form>
        </main>
      </div>
    </div>
  );
}

export default ResetPassword;
