import React from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import '../assets/styles/MyProfile.css';
import { useUser } from '../context/UserContext'; // Access UserContext

/**
 * MyProfile Component:
 * Displays the logged-in user's account details.
 */
function MyProfile({ onLogout }) {
  const { userData } = useUser(); // Access user data from context

  return (
    <div id="my-profile-container">
      {/* Navbar */}
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />

      {/* Content */}
      <div id="my-profile-content" className="d-flex">
        <Sidebar />
        <main id="my-profile-main" className="col-md-9 col-lg-10 p-4">
          <h1 className="mb-4">My Profile</h1>

          {/* User Details Table */}
          <table id="user-details-table" className="table table-striped">
            <tbody>
              <tr>
                <th>Full Name</th>
                <td dangerouslySetInnerHTML={{ __html: userData?.full_name || 'N/A' }}></td>
              </tr>
              <tr>
                <th>Username</th>
                <td dangerouslySetInnerHTML={{ __html: userData?.username || 'N/A' }}></td>
              </tr>
              <tr>
                <th>Phone Number</th>
                <td dangerouslySetInnerHTML={{ __html: userData?.phone_number || 'N/A' }}></td>
              </tr>
              <tr>
                <th>Email</th>
                <td dangerouslySetInnerHTML={{ __html: userData?.email || 'N/A' }}></td>
              </tr>
              <tr>
                <th>Gender</th>
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
