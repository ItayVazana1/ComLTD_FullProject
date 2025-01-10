import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import TypingEffect from '../components/TypingEffect';
import '../assets/styles/Global.css';
import '../assets/styles/Home.css';

/**
 * Home Component:
 * Displays a dashboard with a typing effect.
 */
function Home({ username, onLogout }) { // Accept `username` as a prop
  // State to control the conditional rendering of TypingEffect
  const [showTypingEffect, setShowTypingEffect] = useState(false);

  // Simulate a delay for conditional rendering
  useEffect(() => {
    const timer = setTimeout(() => setShowTypingEffect(true), 500); // Delay by 500ms
    return () => clearTimeout(timer); // Cleanup
  }, []);

  // Sentences for the typing effect
  const sentences = [
    `Hello, <b>${username}</b>!`,
    "Welcome to your personalized dashboard.",
    "Here, you can manage your data plans, settings, and more.",
    "Let's make the most out of today!",
  ];

  return (
    <div id="home-container" className="home-container">
      {/* Navbar with logout functionality */}
      <Navbar username={username} onLogout={onLogout} />

      {/* Main content container */}
      <div id="content-container-home" className="content">
        <Sidebar id="sidebar" />

        {/* Main section */}
        <main
          id="main-content-home"
          className="main-content col-md-9 col-lg-10 p-4"
        >
          {/* Conditional rendering of TypingEffect */}
          {showTypingEffect && (
            <TypingEffect
              sentences={sentences} // Pass sentences array
              typingSpeed={80}
              delayBetweenLines={1000}
            />
          )}
        </main>
      </div>
    </div>
  );
}

export default Home;
