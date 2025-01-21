import React, { useState } from 'react';

/**
 * PlanCard Component:
 * Displays a card with hover effects that shows the title of the plan.
 * On click, a modal appears with more details about the plan.
 * 
 * Props:
 * - title (string): The title of the plan.
 * - description (string): A brief description of the plan.
 * - image (string): URL of the image to display in the card.
 * - details (Array): Array of objects containing additional details (label, value).
 * - borderColor (string): The color for the card border and modal button.
 */
function PlanCard({ title, description, image, details, borderColor }) {
  const [isModalOpen, setIsModalOpen] = useState(false); // State to toggle the modal visibility

  /**
   * Toggles the modal's visibility.
   */
  const toggleModal = () => {
    setIsModalOpen(!isModalOpen);
  };

  return (
    <>
      {/* Card: Displays the plan's image and title */}
      <div
        className="plan-card"
        style={{
          position: 'relative',
          width: '200px',
          height: '200px',
          margin: '10px',
          border: `3px solid ${borderColor}`, // Dynamic border color
          borderRadius: '10px',
          overflow: 'hidden',
          cursor: 'pointer', // Change cursor to indicate interactivity
        }}
        onClick={toggleModal} // Open modal on click
      >
        {/* Image: Background image of the plan card */}
        <img
          src={image}
          alt={title}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover', // Maintain aspect ratio
            transition: 'opacity 0.3s ease', // Smooth transition for hover effects
          }}
          className="plan-card-image"
        />

        {/* Overlay: Appears on hover, displaying the plan's title */}
        <div
          className="plan-card-overlay"
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.7)', // Semi-transparent black background
            color: '#fff', // White text
            display: 'flex', // Center content
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.5rem', // Large font for title
            fontWeight: 'bold',
            opacity: 0, // Hidden by default
            transition: 'opacity 0.3s ease', // Smooth fade-in effect
          }}
        >
          {title}
        </div>
      </div>

      {/* Modal: Displays plan details when the card is clicked */}
      {isModalOpen && (
        <div
          className="plan-modal"
          style={{
            position: 'fixed',
            top: '50%', // Center vertically
            left: '50%', // Center horizontally
            transform: 'translate(-50%, -50%)', // Adjust for centering
            width: '400px', // Fixed modal width
            backgroundColor: '#fff', // White background
            padding: '20px', // Inner padding
            borderRadius: '10px', // Rounded corners
            boxShadow: '0px 5px 15px rgba(0,0,0,0.3)', // Subtle shadow
            zIndex: 1000, // Ensure modal is on top of other elements
          }}
        >
          {/* Modal Title */}
          <h3 style={{ color: borderColor }}>{title}</h3>

          {/* Modal Description */}
          <p
            style={{
              fontSize: '1rem', // Standard font size
              color: '#666', // Gray text for description
              marginBottom: '15px',
            }}
          >
            {description}
          </p>

          {/* Modal Details List */}
          <ul>
            {details.map((detail, index) => (
              <li key={index}>
                <strong>{detail.label}:</strong> {detail.value}
              </li>
            ))}
          </ul>

          {/* Close Button */}
          <button
            onClick={toggleModal} // Close modal on click
            style={{
              backgroundColor: borderColor, // Match button color to border
              color: '#fff', // White text
              padding: '10px 20px', // Button padding
              border: 'none', // No border
              borderRadius: '5px', // Rounded corners
              cursor: 'pointer', // Indicate interactivity
              marginTop: '20px',
            }}
          >
            Close
          </button>
        </div>
      )}
    </>
  );
}

export default PlanCard;
