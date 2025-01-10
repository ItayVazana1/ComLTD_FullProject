import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import PlanCard from '../components/PlanCard';
import TypingEffect from '../components/TypingEffect';
import '../assets/styles/DataPlans.css';
import p1 from '../assets/images/plan_1.png';
import p2 from '../assets/images/plan_2.png';
import p3 from '../assets/images/plan_3.png';
import p4 from '../assets/images/plan_4.png';

/**
 * DataPlans Component:
 * Displays a grid of PlanCard components with a typing effect.
 */
const plansData = [
  {
    title: 'Essential Plan',
    description: 'Perfect for casual users who need just the basics.',
    image: p1,
    details: [
      { label: 'Data Limit', value: '5GB' },
      { label: 'Price', value: '$10/month' },
      { label: 'Speed', value: 'Up to 20Mbps' },
      { label: 'Free Add-ons', value: 'None' },
      { label: 'Roaming', value: 'Not Included' },
      { label: 'Support', value: 'Email Support Only' },
    ],
    borderColor: '#ff206e',
  },
  {
    title: 'Streamer Lite',
    description: 'Ideal for streaming enthusiasts with moderate usage needs.',
    image: p2,
    details: [
      { label: 'Data Limit', value: '20GB' },
      { label: 'Price', value: '$25/month' },
      { label: 'Speed', value: 'Up to 50Mbps' },
      { label: 'Free Add-ons', value: '1 month free on Netflix Basic Plan' },
      { label: 'Roaming', value: 'Domestic Roaming Only' },
      { label: 'Support', value: '24/7 Live Chat Support' },
    ],
    borderColor: '#3e92cc',
  },
  {
    title: 'Unlimited Pro',
    description:
      'Unlimited data for professionals who need constant connectivity.',
    image: p3,
    details: [
      { label: 'Data Limit', value: 'Unlimited (Fair Use Policy: 100GB)' },
      { label: 'Price', value: '$40/month' },
      { label: 'Speed', value: 'Up to 100Mbps' },
      { label: 'Free Add-ons', value: 'Free VPN for 6 months' },
      { label: 'Roaming', value: 'International Roaming (5GB)' },
      { label: 'Support', value: 'Priority Phone Support' },
    ],
    borderColor: '#339989',
  },
  {
    title: 'Global Connect',
    description:
      'For frequent travelers and those who need connectivity worldwide.',
    image: p4,
    details: [
      { label: 'Data Limit', value: '300GB' },
      { label: 'Price', value: '$70/month' },
      { label: 'Speed', value: 'High-speed 5G' },
      { label: 'Free Add-ons', value: '10GB extra in roaming zones' },
      { label: 'Roaming', value: 'Global Roaming (50GB)' },
      { label: 'Support', value: 'Dedicated Account Manager' },
    ],
    borderColor: '#f9c22e',
  },
];

function DataPlans({ username, onLogout }) {
  const [showTypingEffect, setShowTypingEffect] = useState(false); // State for conditional rendering

  useEffect(() => {
    const timer = setTimeout(() => setShowTypingEffect(true), 500); // Delay of 500ms
    return () => clearTimeout(timer); // Cleanup
  }, []);

  return (
    <div id="data-plans-container" className="data-plans-container">
      <Navbar username={username} onLogout={onLogout} />
      <div id="content-container" className="content d-flex">
        <Sidebar id="sidebar" />
        <main id="main-content" className="col-md-9 col-lg-10 p-4">
          {/* Typing Effect Section */}
          <div id="typing-effect-container" className="text-center mb-5">
            {showTypingEffect && ( // Conditional rendering
              <TypingEffect
                sentences={['Explore Our Exclusive Plans!', 'Choose the best for you.']}
                typingSpeed={80}
                delayBetweenLines={1000}
              />
            )}
          </div>

          {/* Data Plans Grid */}
          <div
            id="plans-grid"
            className="d-flex flex-wrap justify-content-center"
          >
            {plansData.map((plan, index) => (
              <PlanCard key={index} {...plan} />
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}

export default DataPlans;
