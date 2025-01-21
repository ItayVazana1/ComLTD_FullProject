import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import TypingEffect from '../components/TypingEffect'; // Typing animation component
import '../assets/styles/Contact.css'; // Import CSS for styling
import { sendContactMessage } from '../services/api'; // API function to send a contact message
import { useUser } from '../context/UserContext'; // UserContext for accessing global user data

/**
 * Contact Component:
 * Displays a contact form alongside a typing effect to enhance the user experience.
 * @param {Function} onLogout - Function to handle user logout
 */
function Contact({ onLogout }) {
  const { userData } = useUser(); // Access user data from UserContext

  const [formData, setFormData] = useState({
    message: '', // State to store the message input
  });
  const [showTypingEffect, setShowTypingEffect] = useState(false); // State to control TypingEffect visibility

  /**
   * Delays the display of the TypingEffect for smoother user experience
   */
  useEffect(() => {
    const timer = setTimeout(() => setShowTypingEffect(true), 500); // Delay TypingEffect by 500ms
    return () => clearTimeout(timer); // Cleanup the timer on unmount
  }, []);

  /**
   * Handles input changes for the form fields
   * @param {Event} e - Input change event
   */
  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData({ ...formData, [id]: value }); // Update formData state with the new value
  };

  /**
   * Handles form submission to send the contact message
   * @param {Event} e - Form submission event
   */
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior

    try {
      // Call the API function with the contact form data
      const response = await sendContactMessage({
        user_id: userData?.id || 'Unknown', // Include user ID if available
        name: userData?.full_name || 'Anonymous', // Use name from UserContext
        email: userData?.email || 'No Email Provided', // Use email from UserContext
        message: formData.message, // User's message
        send_copy: document.getElementById('copyCheckbox').checked, // Whether to send a copy to the user
      });

      // Notify the user of success
      alert(response.message || 'Your message has been sent successfully!');
      setFormData({ message: '' }); // Reset the form after successful submission
    } catch (error) {
      // Notify the user of failure
      alert('Failed to send your message. Please try again.');
    }
  };

  return (
    <div id="contact-container">
      {/* Navbar with user details and logout functionality */}
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />

      {/* Main Content Area */}
      <div id="contact-content" className="d-flex">
        <Sidebar />
        <main id="contact-main" className="d-flex justify-content-between align-items-center">
          {/* Typing Effect Section */}
          <div id="typing-effect-container-contact">
            {showTypingEffect && ( // Show TypingEffect after delay
              <TypingEffect
                sentences={[
                  "<h4>We'd Love to Hear From You 😊</h4>", // Header message
                  'Got a question, suggestion, or need help?', // Follow-up message
                  "Drop us a message, and we'll get back to you as soon as possible.", // Final message
                ]}
                typingSpeed={80} // Speed of typing animation
                delayBetweenLines={1000} // Delay between lines
              />
            )}
          </div>

          {/* Contact Form Section */}
          <form id="contact-form" onSubmit={handleSubmit}>
            {/* Display User Name */}
            <div className="mb-3 text-light">
              <label className="form-label"><b>{userData?.full_name || 'Anonymous'}</b></label>
            </div>
            {/* Display User Email */}
            <div className="mb-3 text-light">
              <label className="form-label"><b>{userData?.email || 'No Email Provided'}</b></label>
            </div>
            {/* Message Textarea */}
            <textarea
              id="message"
              placeholder="Write your message here..."
              value={formData.message} // Controlled input for message
              onChange={handleChange} // Update message state
              required // Mark field as required
            ></textarea>
            {/* Copy Checkbox */}
            <div className="form-check">
              <input
                className="form-check-input"
                type="checkbox"
                id="copyCheckbox" // Checkbox to send a copy of the message
              />
              <label className="form-check-label" htmlFor="copyCheckbox">
                Send me a copy of this message
              </label>
            </div>
            {/* Submit Button */}
            <button type="submit">Send</button>
          </form>
        </main>
      </div>
    </div>
  );
}

export default Contact;
