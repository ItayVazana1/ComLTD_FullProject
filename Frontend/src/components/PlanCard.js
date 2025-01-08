/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react';

function PlanCard({ title, description, image, details, borderColor }) {
    
  return (
    <div className="card" style={{ border: `4px solid ${borderColor}`, borderRadius: '10px' }}>
      <img src={image} className="card-img-top" alt={`${title} Plan`} />
      <div className="card-body">
        <h5 className="card-title">{title}</h5>
        <p className="card-text">{description}</p>
      </div>
      <ul className="list-group list-group-flush">
        {details.map((detail, index) => (
          <li className="list-group-item" key={index}>
            <strong>{detail.label}:</strong> {detail.value}
          </li>
        ))}
      </ul>
      <div className="card-body">
        <a href="#" className="card-link">Learn More</a>
      </div>
    </div>
  );
}

export default PlanCard;
