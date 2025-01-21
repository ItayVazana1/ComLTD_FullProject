import React from 'react';

/**
 * ModalLoader Component:
 * Displays a full-screen loader with a spinning animation.
 * Used to indicate that a process is ongoing (e.g., data fetching).
 */
const ModalLoader = () => {
  return (
    <div
      style={{
        position: 'fixed', // Ensure the loader is fixed to the viewport
        top: 0, // Align to the top of the screen
        left: 0, // Align to the left of the screen
        width: '100%', // Full-screen width
        height: '100%', // Full-screen height
        backgroundColor: 'rgba(0, 0, 0, 0.5)', // Semi-transparent black background
        display: 'flex', // Flexbox for centering the spinner
        alignItems: 'center', // Center vertically
        justifyContent: 'center', // Center horizontally
        zIndex: 1000, // Ensure loader is above other content
      }}
    >
      {/* Spinner Element */}
      <div
        style={{
          width: '60px', // Diameter of the spinner
          height: '60px', // Diameter of the spinner
          border: '6px solid #f3f3f3', // Light gray border for the spinner
          borderTop: '6px solid #3498db', // Blue border for the spinning effect
          borderRadius: '50%', // Make the spinner circular
          animation: 'spin 1s linear infinite', // Continuous spinning animation
        }}
      />
      {/* Inline Keyframes for the Spinning Animation */}
      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); } // Start position
            100% { transform: rotate(360deg); } // Full rotation
          }
        `}
      </style>
    </div>
  );
};

export default ModalLoader;
