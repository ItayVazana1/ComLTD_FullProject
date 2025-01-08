import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../assets/styles/Register.css'; // ייבוא CSS מותאם

function Register() {
  const navigate = useNavigate(); // מאפשר ניווט בין דפים

  return (
    <div className="registration-page">
      <div className="container">
        <div className="title">Registration</div>
        <div className="content">
          <form action="#">
            <div className="user-details">
              <div className="input-box">
                <span className="details">Full Name</span>
                <input type="text" placeholder="Enter your name" required />
              </div>
              <div className="input-box">
                <span className="details">Username</span>
                <input type="text" placeholder="Enter your username" required />
              </div>
              <div className="input-box">
                <span className="details">Email</span>
                <input type="email" placeholder="Enter your email" required />
              </div>
              <div className="input-box">
                <span className="details">Phone Number</span>
                <input type="text" placeholder="Enter your number" required />
              </div>
              <div className="input-box">
                <span className="details">Password</span>
                <input type="password" placeholder="Enter your password" required />
              </div>
              <div className="input-box">
                <span className="details">Confirm Password</span>
                <input type="password" placeholder="Confirm your password" required />
              </div>
            </div>
            <div className="validBox">
              <label className="checkbox-container">
                <input type="checkbox" required />
                <span className="details">Click here to accept terms of use</span>
                </label>
              </div>
            <div className="gender-details">
              <span className="gender-title">Gender</span>
              <div className="category">
                <label htmlFor="dot-1">
                  <input type="radio" name="gender" id="dot-1" />
                  <span className="gender">Male</span>
                </label>
                <label htmlFor="dot-2">
                  <input type="radio" name="gender" id="dot-2" />
                  <span className="gender">Female</span>
                </label>
                <label htmlFor="dot-3">
                  <input type="radio" name="gender" id="dot-3" />
                  <span className="gender">Prefer not to say</span>
                </label>
              </div>
            </div>
            <div className="subButton">
              <input type="submit" value="Register" />
            </div>
            <div className="logButton">
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
