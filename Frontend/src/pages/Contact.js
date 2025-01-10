import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import TypingEffect from '../components/TypingEffect';
import '../assets/styles/Contact.css';

/**
 * Contact Component:
 * Includes a modern form with a typing effect displayed on the right.
 */
function Contact({ username, onLogout }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
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

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Your message has been sent successfully!');
    setFormData({ name: '', email: '', message: '' });
  };

  return (
    <div id="contact-container">
      {/* Navbar */}
      <Navbar username={username} onLogout={onLogout} />
      
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
            <input
              id="name"
              type="text"
              placeholder="Your Full Name"
              value={formData.name}
              onChange={handleChange}
              required
            />
            <input
              id="email"
              type="email"
              placeholder="Your Email Address"
              value={formData.email}
              onChange={handleChange}
              required
            />
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
