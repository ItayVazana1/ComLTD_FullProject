import React from 'react';
import '../assets/styles/navbar.css'; // Import custom CSS for Navbar

/**
 * Navbar Component:
 * Represents the top navigation bar of the application.
 * 
 * Props:
 * - username (string): The name of the logged-in user, displayed next to the user icon.
 * - onLogout (function): Callback function executed when the logout button is clicked.
 */
function Navbar({ username, onLogout }) {
  return (
    <header
      id="navbar"
      className="navbar d-flex justify-content-between align-items-center p-3"
    >
      {/* Navbar Right Section */}
      <div className="navbar-right d-flex align-items-center">
        {/* User Information Section */}
        <div
          id="user-info"
          className="user-info d-flex align-items-center me-3"
        >
          {/* User Icon */}
          <i
            className="fa fa-user-circle" // Font Awesome icon
            aria-hidden="true" // Accessibility attribute
            id="user-icon"
          ></i>
          {/* Display Username */}
          <span id="username-display" className="ms-2">
            {username}
          </span>
        </div>
        {/* Logout Button */}
        <button
          id="logout-button"
          className="btn btn-primary logout-btn"
          onClick={onLogout} // Trigger the onLogout function
        >
          Logout
        </button>
      </div>
    </header>
  );
}

export default Navbar;
