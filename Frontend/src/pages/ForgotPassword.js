import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../assets/styles/ForgotPassword.css'; // ייבוא CSS מותאם לדף שכחתי סיסמה

function ForgotPassword() {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Password reset link has been sent to your email.'); // הודעה למשתמש
    navigate('/login'); // ניתוב חזרה לדף התחברות
  };

  return (
    <div className="forgot-password-page">
      <div className="container">
        <div className="title">Forgot Password</div>
        <div className="content">
          <form onSubmit={handleSubmit}>
            <div className="user-details">
              <div className="input-box">
                <span className="details">Email</span>
                <input type="email" placeholder="Enter your email" required />
              </div>
            </div>
            <div className="subButton">
              <input type="submit" value="Send Reset Link" />
            </div>
            <div className="logButton">
              <input
                type="button"
                value="Back to login"
                onClick={() => navigate('/login')}
              />
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default ForgotPassword;
