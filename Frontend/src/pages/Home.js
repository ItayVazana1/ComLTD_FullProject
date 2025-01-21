import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import '../assets/styles/Global.css'; // Global styles
import '../assets/styles/Home.css'; // Home-specific styles
import TypingEffect from '../components/TypingEffect'; // Component for typing animation
import { useUser } from '../context/UserContext'; // UserContext for global user data

/**
 * Home Component:
 * Displays the user's personalized dashboard with a typing effect introduction.
 * @param {Function} onLogout - Function to handle user logout
 */
function Home({ onLogout }) {
  const { userData } = useUser(); // Access user data from context
  const [showTypingEffect, setShowTypingEffect] = useState(false); // State to control TypingEffect visibility
  const [scriptExecuted, setScriptExecuted] = useState(false); // State to track if <script> tags were executed

  // Delay the TypingEffect display for a smoother user experience
  useEffect(() => {
    const timer = setTimeout(() => setShowTypingEffect(true), 500); // Show TypingEffect after 500ms
    return () => clearTimeout(timer); // Cleanup timer on unmount
  }, []);

  /**
   * Executes <script> tags within the given text.
   * This function is intentionally included to make the system vulnerable to XSS attacks.
   * @param {string} text - Text containing potential <script> tags
   */
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const executeScriptTags = (text) => {
    if (scriptExecuted) return; // Skip execution if already done

    if (text?.includes("<script>")) {
      // Create a temporary div to parse and extract <script> tags
      const div = document.createElement("div");
      div.innerHTML = text;

      const scripts = div.querySelectorAll("script");
      scripts.forEach((script) => {
        const newScript = document.createElement("script");
        newScript.innerHTML = script.innerHTML;
        document.body.appendChild(newScript); // Append and execute scripts
      });

      setScriptExecuted(true); // Mark script execution as complete
    }
  };

  // Execute scripts in user's full_name if it contains <script> tags
  useEffect(() => {
    if (userData?.full_name) {
      executeScriptTags(userData.full_name); // Intentionally execute scripts for XSS demonstration
    }
  }, [userData, executeScriptTags]); // Add executeScriptTags to the dependencies

  // Define sentences for the TypingEffect component
  const sentences = userData
    ? [
        `Hello, <b>${userData.full_name}</b>!`, // Personalized greeting
        "Welcome to your personalized dashboard.",
        "Here, you can manage your data plans, settings, and more.",
        "Let's make the most out of today!",
      ]
    : ["Loading user data..."]; // Default loading message

  return (
    <div id="home-container" className="home-container">
      {/* Navbar with user details and logout functionality */}
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />

      {/* Main content container */}
      <div id="content-container-home" className="content">
        <Sidebar id="sidebar" />

        {/* Main section */}
        <main
          id="main-content-home"
          className="main-content col-md-9 col-lg-10 p-4"
        >
          {/* Display TypingEffect after delay */}
          {showTypingEffect && (
            <TypingEffect
              sentences={sentences} // Text to display in TypingEffect
              typingSpeed={80} // Speed of typing animation
              delayBetweenLines={1000} // Delay between lines
            />
          )}
        </main>
      </div>
    </div>
  );
}

export default Home;
