import React, { useState } from 'react';

/**
 * PlanCard Component:
 * Displays a square card with hover effects to show the name.
 * Opens a modal with details and description when clicked.
 */
function PlanCard({ title, description, image, details, borderColor }) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const toggleModal = () => {
    setIsModalOpen(!isModalOpen);
  };

  return (
    <>
      {/* Card */}
      <div
        className="plan-card"
        style={{
          position: 'relative',
          width: '200px',
          height: '200px',
          margin: '10px',
          border: `3px solid ${borderColor}`,
          borderRadius: '10px',
          overflow: 'hidden',
          cursor: 'pointer',
        }}
        onClick={toggleModal}
      >
        {/* Image */}
        <img
          src={image}
          alt={title}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transition: 'opacity 0.3s ease',
          }}
          className="plan-card-image"
        />

        {/* Overlay */}
        <div
          className="plan-card-overlay"
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            color: '#fff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.5rem',
            fontWeight: 'bold',
            opacity: 0,
            transition: 'opacity 0.3s ease',
          }}
        >
          {title}
        </div>
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div
          className="plan-modal"
          style={{
            position: 'fixed',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: '400px',
            backgroundColor: '#fff',
            padding: '20px',
            borderRadius: '10px',
            boxShadow: '0px 5px 15px rgba(0,0,0,0.3)',
            zIndex: 1000,
          }}
        >
          <h3 style={{ color: borderColor }}>{title}</h3>
          <p
            style={{
              fontSize: '1rem',
              color: '#666',
              marginBottom: '15px',
            }}
          >
            {description}
          </p>
          <ul>
            {details.map((detail, index) => (
              <li key={index}>
                <strong>{detail.label}:</strong> {detail.value}
              </li>
            ))}
          </ul>
          <button
            onClick={toggleModal}
            style={{
              backgroundColor: borderColor,
              color: '#fff',
              padding: '10px 20px',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
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
