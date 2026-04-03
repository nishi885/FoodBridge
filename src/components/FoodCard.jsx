import React from 'react';

// A simple card component for food listing, shows urgent badge when close to expiry.
const FoodCard = ({ item, onAction, actionLabel }) => {
  const expiryDate = new Date(item.expiry);
  const now = new Date();
  const hoursLeft = (expiryDate - now) / (1000 * 60 * 60);
  const isUrgent = hoursLeft > 0 && hoursLeft < 2;

  return (
    <div className={`card ${item.status === 'fulfilled' ? 'card-fulfilled' : ''}`}>
      <div className="card-header">
        <h3>{item.type}</h3>
        {isUrgent && <span className="badge badge-urgent">URGENT</span>}
        <span className={`badge ${item.status === 'available' ? 'badge-available' : 'badge-unavailable'}`}>
          {item.status.toUpperCase()}
        </span>
      </div>
      <div className="card-content">
        <p><strong>Quantity:</strong> {item.quantity}</p>
        <p><strong>Location:</strong> {item.location}</p>
        <p><strong>Expiry:</strong> {expiryDate.toLocaleString()}</p>
      </div>
      {onAction && (
        <button className="btn-secondary" onClick={() => onAction(item)}>
          {actionLabel}
        </button>
      )}
    </div>
  );
};

export default FoodCard;
