import React from 'react';
import '../assets/styles/Global.css'; // Global styles
import '../assets/styles/About.css'; // Styles specific to the About page

/**
 * OurPartners Component:
 * Renders a section displaying partner logos in a horizontal layout.
 * 
 * Props:
 * - partners (Array): An array of partner objects, each containing:
 *   - name (string): The name of the partner.
 *   - image (string): The URL of the partner's logo.
 */
function OurPartners({ partners }) {
  return (
    <section id="our-partners-section" className="our-partners">
      {/* Section Title */}
      <h5 id="our-partners-title">Our Partners:</h5>

      {/* Container for Partner Logos */}
      <div
        id="partners-container"
        className="rectangle-container d-flex gap-3 justify-content-between align-items-center"
      >
        {/* Iterate over the partners array to display each logo */}
        {partners.map((partner, index) => (
          <img
            key={index} // Unique key for React rendering
            id={`partner-logo-${index}`} // Unique ID for each partner logo
            src={partner.image} // Logo image URL
            alt={partner.name} // Alternative text for accessibility
            className="img-fluid" // Responsive image class
            style={{
              maxHeight: '80px', // Restrict height to maintain uniformity
              objectFit: 'cover', // Ensure the image scales proportionally
            }}
          />
        ))}
      </div>
    </section>
  );
}

export default OurPartners;
