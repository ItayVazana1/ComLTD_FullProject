import React from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import TypingEffect from '../components/TypingEffect';
import '../assets/styles/colors.css';
import '../assets/styles/main.css';

function Home({ onLogout }) { // קבלת onLogout כפרופס
  const user = "Itay"; // Username
  console.log("onLogout prop in Home:", onLogout); // בדיקת Debug

  return (
    <div className="home-container">
      <Navbar onLogout={onLogout} /> {/* העברת הפונקציה ל-Navbar */}
      <div className="content">
        <Sidebar />
        <main className="main-content col-md-9 col-lg-10 p-4" style={{ fontSize: '75px' }}>
          <TypingEffect userName={user} typingSpeed={80} delayBetweenLines={1000} />
        </main>
      </div>
    </div>
  );
}

export default Home;
