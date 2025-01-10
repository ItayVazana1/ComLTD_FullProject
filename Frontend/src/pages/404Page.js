import React from 'react';
import '../assets/styles/404Page.css'; // ייבוא ה-CSS לדף

function PageNotFound() {
  return (
    <div className="not-found-container">
      <h1 className="not-found-title">404</h1>
      <div className="not-found-text">
        <span>Oops!</span>
        <span>The page you're looking for doesn't exist.</span>
        <span>Please check the URL or go back to the homepage.</span>
      </div>
    </div>
  );
}

export default PageNotFound;
