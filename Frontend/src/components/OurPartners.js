import React from 'react';
import '../assets/styles/Global.css';
import '../assets/styles/About.css';

/**
 * OurPartners Component:
 * Displays a list of partner logos in a horizontal layout.
 * - Accepts an array of partners as a prop.
 * - Each partner includes a name and an image.
 */
function OurPartners({ partners }) {
  return (
    <section id="our-partners-section" className="our-partners">
      {/* Section Title */}
      <h5 id="our-partners-title">Our Partners:</h5>

      {/* Partners Logo Container */}
      <div
        id="partners-container"
        className="rectangle-container d-flex gap-3 justify-content-between align-items-center"
      >
        {partners.map((partner, index) => (
          <img
            key={index}
            id={`partner-logo-${index}`} // Unique ID for each partner logo
            src={partner.image}
            alt={partner.name}
            className="img-fluid"
            style={{ maxHeight: '80px', objectFit: 'cover' }}
          />
        ))}
      </div>
    </section>
  );
}

export default OurPartners;
