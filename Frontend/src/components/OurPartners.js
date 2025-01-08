import React from 'react';

function OurPartners({ partners }) {
  return (
    <section className="our-partners">
      <h5>Our Partners:</h5>
      <div className="rectangle-container d-flex gap-3 justify-content-between align-items-center">
        {partners.map((partner, index) => (
          <img
            key={index}
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
