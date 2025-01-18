import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import '../assets/styles/Global.css';
import '../assets/styles/Home.css';
import TypingEffect from '../components/TypingEffect'; // Import TypingEffect
import { useUser } from '../context/UserContext'; // Import UserContext

function Home({ onLogout }) {
  const { userData } = useUser(); // Access user data from UserContext
  const [showTypingEffect, setShowTypingEffect] = useState(false);

  useEffect(() => {
    // Delay the display of TypingEffect
    const timer = setTimeout(() => setShowTypingEffect(true), 500);
    return () => clearTimeout(timer);
  }, []);

  // Define sentences for TypingEffect
  const sentences = userData
    ? [
        `Hello, <b>${userData.full_name}</b>!`,
        "Welcome to your personalized dashboard.",
        "Here, you can manage your data plans, settings, and more.",
        "Let's make the most out of today!",
      ]
    : ["Loading user data..."];

  return (
    <div id="home-container" className="home-container">
      {/* Navbar with user data */}
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />

      {/* Main content container */}
      <div id="content-container-home" className="content">
        <Sidebar id="sidebar" />

        {/* Main section */}
        <main
          id="main-content-home"
          className="main-content col-md-9 col-lg-10 p-4"
        >
          {/* TypingEffect */}
          {showTypingEffect && (
            <TypingEffect
              sentences={sentences}
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
