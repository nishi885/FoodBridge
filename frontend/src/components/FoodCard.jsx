import React from 'react';

const FoodCard = ({ item, onAction, actionLabel }) => {
  const expiryDate = new Date(item.expiry);
  const now = new Date();
  const hoursLeft = (expiryDate - now) / (1000 * 60 * 60);
  const isUrgent = hoursLeft > 0 && hoursLeft < 24;

  const getStatusColor = () => {
    if (item.status === 'fulfilled') return 'badge-unavailable';
    if (isUrgent) return 'badge-urgent';
    return 'badge-available';
  };

  const getStatusText = () => {
    if (item.status === 'fulfilled') return 'FULFILLED';
    if (isUrgent) return 'URGENT';
    return 'AVAILABLE';
  };

  return (
    <div className={`card ${item.status === 'fulfilled' ? 'card-fulfilled' : ''}`}>
      <div className="card-header">
        <h3>🍎 {item.type}</h3>
        <span className={`badge ${getStatusColor()}`}>
          {getStatusText()}
        </span>
      </div>
      <div className="card-content">
        <p><strong>📦 Quantity:</strong> {item.quantity}</p>
        <p><strong>📍 Location:</strong> {item.location}</p>
        <p><strong>⏰ Expires:</strong> {expiryDate.toLocaleString()}</p>
        {isUrgent && (
          <p style={{ color: 'var(--error-color)', fontWeight: 'bold', marginTop: '10px' }}>
            ⚠️ Expires in {Math.floor(hoursLeft)} hours!
          </p>
        )}
      </div>
      {onAction && item.status !== 'fulfilled' && (
        <button className="btn-primary" onClick={() => onAction(item)} style={{ marginTop: '15px' }}>
          {actionLabel}
        </button>
      )}
    </div>
  );
};
    </div>
  );
};

export default FoodCard;
