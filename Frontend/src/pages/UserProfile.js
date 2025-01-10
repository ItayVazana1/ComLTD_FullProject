import React from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import '../assets/styles/MyProfile.css';

/**
 * MyProfile Component:
 * Displays the logged-in user's account details.
 */
function MyProfile({ username, onLogout }) {
  // Mock data for the current user (replace with actual API or state in the future)
  const userData = {
    fullName: 'First Last',
    username: username,
    phone: '+972-50-965-3133',
    email: username + '@example.com',
    gender: 'Male',
    memberSince: Date.now(),
  };

  return (
    <div id="my-profile-container">
      {/* Navbar */}
      <Navbar username={username} onLogout={onLogout} />

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
                <td>{userData.fullName}</td>
              </tr>
              <tr>
                <th>Username</th>
                <td>{userData.username}</td>
              </tr>
              <tr>
                <th>Phone Number</th>
                <td>{userData.phone}</td>
              </tr>
              <tr>
                <th>Email</th>
                <td>{userData.email}</td>
              </tr>
              <tr>
                <th>Gender</th>
                <td>{userData.gender}</td>
              </tr>
              <tr>
                <th>Member Since</th>
                <td>{new Date(userData.memberSince).toLocaleDateString()}</td>
              </tr>
            </tbody>
          </table>
        </main>
      </div>
    </div>
  );
}

export default MyProfile;
