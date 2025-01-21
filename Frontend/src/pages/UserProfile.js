import React from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import '../assets/styles/MyProfile.css';
import { useUser } from '../context/UserContext'; // Access UserContext for global user data

/**
 * MyProfile Component:
 * Displays the logged-in user's account details.
 * @param {Function} onLogout - Function to handle user logout
 */
function MyProfile({ onLogout }) {
  const { userData } = useUser(); // Access user data from context

  return (
    <div id="my-profile-container">
      {/* Top navigation bar */}
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />

      {/* Main content area */}
      <div id="my-profile-content" className="d-flex">
        {/* Sidebar navigation */}
        <Sidebar />

        {/* Profile details */}
        <main id="my-profile-main" className="col-md-9 col-lg-10 p-4">
          <h1 className="mb-4">My Profile</h1>

          {/* User Details Table */}
          <table id="user-details-table" className="table table-striped">
            <tbody>
              <tr>
                <th>Full Name</th>
                {/* Display user full name; intentionally vulnerable to XSS */}
                <td dangerouslySetInnerHTML={{ __html: userData?.full_name || 'N/A' }}></td>
              </tr>
              <tr>
                <th>Username</th>
                {/* Display username; intentionally vulnerable to XSS */}
                <td dangerouslySetInnerHTML={{ __html: userData?.username || 'N/A' }}></td>
              </tr>
              <tr>
                <th>Phone Number</th>
                {/* Display phone number; intentionally vulnerable to XSS */}
                <td dangerouslySetInnerHTML={{ __html: userData?.phone_number || 'N/A' }}></td>
              </tr>
              <tr>
                <th>Email</th>
                {/* Display email; intentionally vulnerable to XSS */}
                <td dangerouslySetInnerHTML={{ __html: userData?.email || 'N/A' }}></td>
              </tr>
              <tr>
                <th>Gender</th>
                {/* Display gender; intentionally vulnerable to XSS */}
                <td dangerouslySetInnerHTML={{ __html: userData?.gender || 'N/A' }}></td>
              </tr>
            </tbody>
          </table>
        </main>
      </div>
    </div>
  );
}

export default MyProfile;
