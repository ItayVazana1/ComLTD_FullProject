import React from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import OurStory from '../components/OurStory'; // Component for displaying the company story
import OurPartners from '../components/OurPartners'; // Component for displaying partners
import { useUser } from '../context/UserContext'; // Access UserContext for user data
import p1 from '../assets/images/partner1.png'; // Partner 1 image
import p2 from '../assets/images/partner2.png'; // Partner 2 image
import p3 from '../assets/images/partner3.png'; // Partner 3 image
import p4 from '../assets/images/partner4.png'; // Partner 4 image
import p5 from '../assets/images/partner5.png'; // Partner 5 image
import '../assets/styles/Global.css'; // Global styles
import '../assets/styles/About.css'; // Styles specific to the About page

/**
 * About Component:
 * Renders the "About" page, including:
 * - A navbar for navigation and logout functionality.
 * - A sidebar for additional navigation options.
 * - The main content area featuring "Our Story" and "Our Partners" sections.
 * 
 * @param {Function} onLogout - Function to handle user logout
 */

const partnersData = [
  { name: 'Partner 1', image: p1 }, // Partner 1 details
  { name: 'Partner 2', image: p2 }, // Partner 2 details
  { name: 'Partner 3', image: p3 }, // Partner 3 details
  { name: 'Partner 4', image: p4 }, // Partner 4 details
  { name: 'Partner 5', image: p5 }, // Partner 5 details
];

function About({ onLogout }) {
  const { userData } = useUser(); // Access user data from UserContext

  return (
    <div id="about-container" className="about-container">
      {/* Navbar section with user details and logout support */}
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />

      {/* Main content container with sidebar and primary sections */}
      <div id="content-container-about" className="content d-flex">
        {/* Sidebar for navigation */}
        <Sidebar id="sidebar" />

        {/* Main area containing "Our Story" and "Our Partners" */}
        <main id="main-content-about" className="col-md-9 col-lg-10 p-4">
          {/* "Our Story" Section */}
          <OurStory id="our-story" />
          {/* "Our Partners" Section */}
          <OurPartners id="our-partners" partners={partnersData} />
        </main>
      </div>
    </div>
  );
}

export default About;
