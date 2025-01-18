import React from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import OurStory from '../components/OurStory';
import OurPartners from '../components/OurPartners';
import { useUser } from '../context/UserContext'; // Import UserContext
import p1 from '../assets/images/partner1.png';
import p2 from '../assets/images/partner2.png';
import p3 from '../assets/images/partner3.png';
import p4 from '../assets/images/partner4.png';
import p5 from '../assets/images/partner5.png';
import '../assets/styles/Global.css';
import '../assets/styles/About.css';

/**
 * About Component:
 * This component renders the "About" page, including:
 * - A navbar for navigation and logout functionality.
 * - A sidebar for additional navigation options.
 * - The main content area featuring "Our Story" and "Our Partners" sections.
 */
const partnersData = [
  { name: 'Partner 1', image: p1 },
  { name: 'Partner 2', image: p2 },
  { name: 'Partner 3', image: p3 },
  { name: 'Partner 4', image: p4 },
  { name: 'Partner 5', image: p5 },
];

function About({ onLogout }) {
  const { userData } = useUser(); // Access user data from UserContext

  return (
    <div id="about-container" className="about-container">
      {/* Navbar section with logout support */}
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />

      {/* Main content container with sidebar and primary sections */}
      <div id="content-container-about" className="content d-flex">
        <Sidebar id="sidebar" />

        {/* Main area containing "Our Story" and "Our Partners" */}
        <main id="main-content-about" className="col-md-9 col-lg-10 p-4">
          <OurStory id="our-story" />
          <OurPartners id="our-partners" partners={partnersData} />
        </main>
      </div>
    </div>
  );
}

export default About;
