import React from 'react';
import '../assets/styles/404Page.css'; // Import CSS for styling the 404 page

/**
 * PageNotFound Component:
 * Renders a simple and user-friendly 404 page to inform users that the requested page does not exist.
 */
function PageNotFound() {
  return (
    <div className="not-found-container">
      {/* Page title */}
      <h1 className="not-found-title">404</h1>
      
      {/* Error message text */}
      <div className="not-found-text">
        <span>Oops!</span> {/* Attention-grabbing text */}
        <span>The page you're looking for doesn't exist.</span> {/* Explanation */}
        <span>Please check the URL or go back to the homepage.</span> {/* Suggestion */}
      </div>
    </div>
  );
}

export default PageNotFound;
