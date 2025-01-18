import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import TypingEffect from '../components/TypingEffect';
import '../assets/styles/Contact.css';
import { sendContactMessage } from '../services/api';
import { useUser } from '../context/UserContext'; // Import UserContext

/**
 * Contact Component:
 * Includes a modern form with a typing effect displayed on the right.
 */
function Contact({ onLogout }) {
  const { userData } = useUser(); // Access user data from context

  const [formData, setFormData] = useState({
    message: '',
  });
  const [showTypingEffect, setShowTypingEffect] = useState(false); // State for conditional rendering

  // Simulate a delay before showing the typing effect
  useEffect(() => {
    const timer = setTimeout(() => setShowTypingEffect(true), 500); // Delay of 500ms
    return () => clearTimeout(timer); // Cleanup
  }, []);

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData({ ...formData, [id]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await sendContactMessage({
        user_id: userData?.id || 'Unknown', // Include user ID from UserContext
        name: userData?.full_name || 'Anonymous', // Use name from UserContext
        email: userData?.email || 'No Email Provided', // Use email from UserContext
        message: formData.message,
        send_copy: document.getElementById('copyCheckbox').checked, // Check if the user wants a copy
      });
      alert(response.message || 'Your message has been sent successfully!');
      setFormData({ message: '' });
    } catch (error) {
      alert('Failed to send your message. Please try again.');
    }
  };

  return (
    <div id="contact-container">
      {/* Navbar */}
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />

      {/* Main Content */}
      <div id="contact-content" className="d-flex">
        <Sidebar />
        <main id="contact-main" className="d-flex justify-content-between align-items-center">
          {/* Typing Effect */}
          <div id="typing-effect-container-contact">
            {showTypingEffect && ( // Conditional rendering
              <TypingEffect
                sentences={[
                  "<h4>We'd Love to Hear From You 😊</h4>",
                  'Got a question, suggestion, or need help?',
                  "Drop us a message, and we'll get back to you as soon as possible.",
                ]}
                typingSpeed={80}
                delayBetweenLines={1000}
              />
            )}
          </div>

          {/* Contact Form */}
          <form id="contact-form" onSubmit={handleSubmit}>
            <div className="mb-3 text-light">
              <label className="form-label"><b>{userData?.full_name || 'Anonymous'}</b></label>
            </div>
            <div className="mb-3 text-light">
              <label className="form-label"><b>{userData?.email || 'No Email Provided'}</b></label>
            </div>
            <textarea
              id="message"
              placeholder="Write your message here..."
              value={formData.message}
              onChange={handleChange}
              required
            ></textarea>
            <div className="form-check">
              <input
                className="form-check-input"
                type="checkbox"
                id="copyCheckbox"
              />
              <label className="form-check-label" htmlFor="copyCheckbox">
                Send me a copy of this message
              </label>
            </div>
            <button type="submit">Send</button>
          </form>
        </main>
      </div>
    </div>
  );
}

export default Contact;
