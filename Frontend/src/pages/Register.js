import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../assets/styles/Register.css';

function Register() {
  const navigate = useNavigate(); // Enables navigation between pages

  return (
    <div id="registration-page" className="registration-page">
      <div id="registration-container" className="container">
        {/* Page Title */}
        <div id="registration-title" className="title">Registration</div>

        {/* Registration Form */}
        <div id="registration-content" className="content">
          <form id="registration-form" action="#">
            {/* User Details Section */}
            <div id="user-details" className="user-details">
              <div id="name-box" className="input-box">
                <span id="name-label" className="details">Full Name</span>
                <input
                  id="name-input"
                  type="text"
                  placeholder="Enter your name"
                  required
                />
              </div>
              <div id="username-box" className="input-box">
                <span id="username-label" className="details">Username</span>
                <input
                  id="username-input"
                  type="text"
                  placeholder="Enter your username"
                  required
                />
              </div>
              <div id="email-box" className="input-box">
                <span id="email-label" className="details">Email</span>
                <input
                  id="email-input"
                  type="email"
                  placeholder="Enter your email"
                  required
                />
              </div>
              <div id="phone-box" className="input-box">
                <span id="phone-label" className="details">Phone Number</span>
                <input
                  id="phone-input"
                  type="text"
                  placeholder="Enter your number"
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
              <div id="confirm-password-box" className="input-box">
                <span id="confirm-password-label" className="details">Confirm Password</span>
                <input
                  id="confirm-password-input"
                  type="password"
                  placeholder="Confirm your password"
                  required
                />
              </div>
            </div>

            {/* Terms of Use Checkbox */}
            <div id="terms-box" className="validBox">
              <label id="terms-label" className="checkbox-container">
                <input id="terms-checkbox" type="checkbox" required />
                <span className="details">Click here to accept terms of use</span>
              </label>
            </div>

            {/* Gender Selection */}
            <div id="gender-details" className="gender-details">
              <span id="gender-title" className="gender-title">Gender</span>
              <div id="gender-category" className="category">
                <label htmlFor="dot-1">
                  <input id="gender-male" type="radio" name="gender" />
                  <span className="gender">Male</span>
                </label>
                <label htmlFor="dot-2">
                  <input id="gender-female" type="radio" name="gender" />
                  <span className="gender">Female</span>
                </label>
                <label htmlFor="dot-3">
                  <input id="gender-other" type="radio" name="gender" />
                  <span className="gender">Prefer not to say</span>
                </label>
              </div>
            </div>

            {/* Submit Button */}
            <div id="register-submit-button" className="subButton">
              <input type="submit" value="Register" />
            </div>

            {/* Back to Login Button */}
            <div id="register-back-login-button" className="logButton">
              <input
                type="button"
                value="Already registered? Back to login"
                onClick={() => navigate('/login')}
              />
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Register;
