import React from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import OurStory from '../components/OurStory';
import OurPartners from '../components/OurPartners';
import p1 from '../assets/images/partner1.png'
import p2 from '../assets/images/partner2.png'
import p3 from '../assets/images/partner3.png'
import p4 from '../assets/images/partner4.png'
import p5 from '../assets/images/partner5.png'

const partnersData = [
  { name: 'Partner 1', image: p1 },
  { name: 'Partner 2', image: p2 },
  { name: 'Partner 3', image: p3 },
  { name: 'Partner 4', image: p4 },
  { name: 'Partner 5', image: p5 },
];

function About({ onLogout }) {
  return (
    <div className="about-container">
      <Navbar onLogout={onLogout} />
      <div className="content d-flex">
        <Sidebar />
        <main className="col-md-9 col-lg-10 p-4">
          <OurStory /><br></br>
          <OurPartners partners={partnersData} />
        </main>
      </div>
    </div>
  );
}

export default About;
