import React from 'react';
import '../assets/styles/Navbar.css'; // Import custom CSS for Navbar

/**
 * Navbar Component:
 * Represents the top navigation bar of the application.
 * - Includes a search box for quick input.
 * - Displays the username with a user icon.
 * - Includes a logout button to exit the application.
 */
function Navbar({ username, onLogout }) {
  return (
    <header id="navbar" className="navbar d-flex justify-content-between align-items-center p-3">
      {/* Search box for user input */}
      <div className="navbar-right d-flex align-items-center">
        {/* User icon and username */}
        <div id="user-info" className="user-info d-flex align-items-center me-3">
          <i className="fa fa-user-circle" aria-hidden="true" id="user-icon"></i>
          <span id="username-display" className="ms-2">{username}</span>
        </div>
        {/* Logout button */}
        <button
          id="logout-button"
          className="btn btn-primary logout-btn"
          onClick={onLogout}
        >
          Logout
        </button>
      </div>
    </header>
  );
}

export default Navbar;
