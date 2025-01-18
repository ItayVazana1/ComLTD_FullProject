import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../assets/styles/Register.css';
import { registerUser } from '../services/api'; // Import the API function

function Register() {
  const navigate = useNavigate(); // Enables navigation between pages

  const [formData, setFormData] = useState({
    fullName: '',
    username: '',
    email: '',
    phoneNumber: '',
    password: '',
    confirmPassword: '',
    gender: '',
    acceptTerms: true, // Default value is true since there's a checkbox
  });

  // Error messages mapping
  const errorMessages = {
    400: "Invalid input. Please check your details.",
    422: "Missing or invalid fields. Please fill out all required fields.",
    500: "Internal server error. Please try again later.",
  };

  // Update state when input values change
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior

    // Convert keys from CamelCase to SnakeCase
    const snakeCaseFormData = {
      full_name: formData.fullName,
      username: formData.username,
      email: formData.email,
      phone_number: formData.phoneNumber,
      password: formData.password,
      confirm_password: formData.confirmPassword,
      gender: formData.gender,
      accept_terms: formData.acceptTerms,
    };

    try {
      // Use the API function for registration
      await registerUser(snakeCaseFormData);
      navigate('/login'); // Redirect to login page
    } catch (error) {
      // Handle error responses
      const statusCode = error.response?.status || 500;
      const errorMessage =
        errorMessages[statusCode] || "An unexpected error occurred.";
      alert(errorMessage);
    }
  };

  return (
    <div id="registration-page" className="registration-page">
      <div id="registration-container" className="container">
        {/* Page Title */}
        <div id="registration-title" className="title">Registration</div>

        {/* Registration Form */}
        <div id="registration-content" className="content">
          <form id="registration-form" onSubmit={handleSubmit}>
            {/* User Details Section */}
            <div id="user-details" className="user-details">
              <div id="name-box" className="input-box">
                <span id="name-label" className="details">Full Name</span>
                <input
                  id="name-input"
                  type="text"
                  name="fullName"
                  placeholder="Enter your name"
                  value={formData.fullName}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div id="username-box" className="input-box">
                <span id="username-label" className="details">Username</span>
                <input
                  id="username-input"
                  type="text"
                  name="username"
                  placeholder="Enter your username"
                  value={formData.username}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div id="email-box" className="input-box">
                <span id="email-label" className="details">Email</span>
                <input
                  id="email-input"
                  type="email"
                  name="email"
                  placeholder="Enter your email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div id="phone-box" className="input-box">
                <span id="phone-label" className="details">Phone Number</span>
                <input
                  id="phone-input"
                  type="text"
                  name="phoneNumber"
                  placeholder="Enter your number"
                  value={formData.phoneNumber}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div id="password-box" className="input-box">
                <span id="password-label" className="details">Password</span>
                <input
                  id="password-input"
                  type="password"
                  name="password"
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div id="confirm-password-box" className="input-box">
                <span id="confirm-password-label" className="details">Confirm Password</span>
                <input
                  id="confirm-password-input"
                  type="password"
                  name="confirmPassword"
                  placeholder="Confirm your password"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>

            {/* Terms of Use Checkbox */}
            <div id="terms-box" className="validBox">
              <label id="terms-label" className="checkbox-container">
                <input
                  id="terms-checkbox"
                  type="checkbox"
                  name="acceptTerms"
                  checked={formData.acceptTerms}
                  onChange={handleInputChange}
                  required
                />
                <span className="details">Click here to accept terms of use</span>
              </label>
            </div>

            {/* Gender Selection */}
            <div id="gender-details" className="gender-details">
              <span id="gender-title" className="gender-title">Gender</span>
              <div id="gender-category" className="category">
                <label htmlFor="dot-1">
                  <input
                    id="gender-male"
                    type="radio"
                    name="gender"
                    value="Male"
                    onChange={handleInputChange}
                  />
                  <span className="gender">Male</span>
                </label>
                <label htmlFor="dot-2">
                  <input
                    id="gender-female"
                    type="radio"
                    name="gender"
                    value="Female"
                    onChange={handleInputChange}
                  />
                  <span className="gender">Female</span>
                </label>
                <label htmlFor="dot-3">
                  <input
                    id="gender-other"
                    type="radio"
                    name="gender"
                    value="Other"
                    onChange={handleInputChange}
                  />
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
