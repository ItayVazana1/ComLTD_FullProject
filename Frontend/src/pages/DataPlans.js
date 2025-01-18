import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import PlanCard from '../components/PlanCard';
import TypingEffect from '../components/TypingEffect';
import '../assets/styles/DataPlans.css';
import { fetchDataPlans } from '../services/api'; // Import the API function
import { useUser } from '../context/UserContext'; // Import UserContext

// Define colors and images for plans
const colors = ['#ff206e', '#3e92cc', '#339989', '#f9c22e'];
const images = [
  require('../assets/images/plan_1.png'),
  require('../assets/images/plan_2.png'),
  require('../assets/images/plan_3.png'),
  require('../assets/images/plan_4.png'),
];

function DataPlans({ onLogout }) {
  const { userData } = useUser(); // Access user data from UserContext
  const [showTypingEffect, setShowTypingEffect] = useState(false); // State for conditional rendering
  const [plansData, setPlansData] = useState([]); // State to store plans data
  const [loading, setLoading] = useState(true); // State for loading status

  useEffect(() => {
    const timer = setTimeout(() => setShowTypingEffect(true), 500); // Delay of 500ms

    // Fetch plans data
    const fetchPlans = async () => {
      try {
        const plans = await fetchDataPlans(); // Fetch data plans
        setPlansData(plans); // Update state with plans data
      } catch (error) {
        console.error('Failed to fetch data plans:', error);
      } finally {
        setLoading(false); // Set loading to false
      }
    };

    fetchPlans();

    return () => clearTimeout(timer); // Cleanup
  }, []);

  return (
    <div id="data-plans-container" className="data-plans-container">
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />
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
          <div id="plans-grid" className="d-flex flex-wrap justify-content-center">
            {loading ? (
              <p>Loading plans...</p> // Show loading message
            ) : (
              plansData.map((plan, index) => (
                <PlanCard
                  key={index}
                  title={plan.package_name}
                  description={plan.description}
                  image={images[index % images.length]} // Assign image dynamically
                  details={[
                    { label: 'Price', value: `$${plan.monthly_price}/month` },
                  ]}
                  borderColor={colors[index % colors.length]} // Assign color dynamically
                />
              ))
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

export default DataPlans;
