import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../assets/styles/Login.css'; // ייבוא CSS מותאם לדף ההתחברות

function Login({ onLogin }) {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(); // קריאה לפונקציית התחברות (מעודכנת)
    navigate('/'); // ניתוב לדף ה-Home
  };

  return (
    <div className="login-page">
      <div className="container">
        <div className="title">Login</div>
        <div className="content">
          <form onSubmit={handleSubmit}>
            <div className="user-details">
              <div className="input-box">
                <span className="details">Username</span>
                <input type="text" placeholder="Enter your username" required />
              </div>
              <div className="input-box">
                <span className="details">Password</span>
                <input type="password" placeholder="Enter your password" required />
              </div>
            </div>
            <div className="validBox">
              <label className="checkbox-container">
                <input type="checkbox" />
                <span className="details">Remember me</span>
              </label>
            </div>
            <div className="subButton">
              <input type="submit" value="Login" />
            </div>
            <div className="logButton">
              <input
                type="button"
                value="Forgot Password?"
                onClick={() => navigate('/forgot-password')}
              />
            </div>
            <div className="logButton">
              <input
                type="button"
                value="Don't have an account? Register here"
                onClick={() => navigate('/register')}
              />
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
