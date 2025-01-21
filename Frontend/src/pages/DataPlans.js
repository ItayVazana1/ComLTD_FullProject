import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import PlanCard from '../components/PlanCard'; // Component to display individual plans
import TypingEffect from '../components/TypingEffect'; // Component for typing animation
import '../assets/styles/DataPlans.css'; // CSS for styling the page
import { fetchDataPlans } from '../services/api'; // API function to fetch data plans
import { useUser } from '../context/UserContext'; // UserContext for accessing global user data

// Define colors and images for plans to dynamically style PlanCards
const colors = ['#ff206e', '#3e92cc', '#339989', '#f9c22e'];
const images = [
  require('../assets/images/plan_1.png'),
  require('../assets/images/plan_2.png'),
  require('../assets/images/plan_3.png'),
  require('../assets/images/plan_4.png'),
];

/**
 * DataPlans Component:
 * Displays available data plans in a grid format, with a typing effect introduction.
 * @param {Function} onLogout - Function to handle user logout
 */
function DataPlans({ onLogout }) {
  const { userData } = useUser(); // Access user data from context
  const [showTypingEffect, setShowTypingEffect] = useState(false); // State for showing TypingEffect
  const [plansData, setPlansData] = useState([]); // State to store data plans
  const [loading, setLoading] = useState(true); // State to manage loading status

  useEffect(() => {
    const timer = setTimeout(() => setShowTypingEffect(true), 500); // Delay TypingEffect by 500ms

    /**
     * Fetch and update data plans from the server
     */
    const fetchPlans = async () => {
      try {
        const plans = await fetchDataPlans(); // Fetch plans using API function
        setPlansData(plans); // Update state with the fetched plans
      } catch (error) {
        console.error('Failed to fetch data plans:', error); // Log error if fetch fails
      } finally {
        setLoading(false); // Ensure loading spinner is hidden
      }
    };

    fetchPlans(); // Trigger fetching of data plans

    return () => clearTimeout(timer); // Cleanup timer on component unmount
  }, []);

  return (
    <div id="data-plans-container" className="data-plans-container">
      {/* Navbar with user details and logout functionality */}
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />

      <div id="content-container" className="content d-flex">
        {/* Sidebar Navigation */}
        <Sidebar id="sidebar" />

        <main id="main-content" className="col-md-9 col-lg-10 p-4">
          {/* Typing Effect Section */}
          <div id="typing-effect-container" className="text-center mb-5">
            {showTypingEffect && ( // Show TypingEffect after the delay
              <TypingEffect
                sentences={['Explore Our Exclusive Plans!', 'Choose the best for you.']} // Text to display
                typingSpeed={80} // Speed of typing animation
                delayBetweenLines={1000} // Delay between lines
              />
            )}
          </div>

          {/* Data Plans Grid */}
          <div id="plans-grid" className="d-flex flex-wrap justify-content-center">
            {loading ? (
              <p>Loading plans...</p> // Show loading message while fetching
            ) : (
              plansData.map((plan, index) => (
                <PlanCard
                  key={index} // Unique key for each plan
                  title={plan.package_name} // Display the plan name
                  description={plan.description} // Display the plan description
                  image={images[index % images.length]} // Assign an image cyclically
                  details={[
                    { label: 'Price', value: `$${plan.monthly_price}/month` }, // Plan price details
                  ]}
                  borderColor={colors[index % colors.length]} // Assign a border color cyclically
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
