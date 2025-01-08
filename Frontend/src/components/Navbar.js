import React from 'react';
import '../assets/styles/colors.css';
import '../assets/styles/main.css';
import '../assets/styles/navbar.css'; // ייבוא CSS מותאם

function Navbar({onLogout}) {
  return (
    <header className="navbar d-flex justify-content-between align-items-center p-3">
      {/* תיבת חיפוש */}
      <input
        type="text"
        className="form-control w-25"
        placeholder="You can search here.."
      />
      {/* כפתור Logout */}
      <button 
        className="btn btn-primary logout-btn" 
        onClick={onLogout}>
        Logout
      </button>
    </header>
  );
}

export default Navbar;
