import React from 'react';

const RequestCard = ({ request, onAccept }) => {
  const getStatusColor = () => {
    switch (request.status) {
      case 'pending': return 'badge-urgent';
      case 'accepted': return 'badge-available';
      case 'fulfilled': return 'badge-unavailable';
      default: return 'badge-unavailable';
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <h3>🤝 Request for: {request.food?.type || 'Unknown Food'}</h3>
        <span className={`badge ${getStatusColor()}`}>
          {request.status.toUpperCase()}
        </span>
      </div>
      <div className="card-content">
        <p><strong>📦 Quantity:</strong> {request.food?.quantity}</p>
        <p><strong>🏢 NGO:</strong> {request.ngo?.name || request.ngoId}</p>
        <p><strong>📍 Location:</strong> {request.food?.location}</p>
        <p><strong>⏰ Requested:</strong> {new Date(request.requestedAt).toLocaleString()}</p>
      </div>
      {onAccept && request.status === 'pending' && (
        <button className="btn-primary" onClick={() => onAccept(request)} style={{ marginTop: '15px' }}>
          ✅ Accept Request
        </button>
      )}
    </div>
  );
};

export default RequestCard;
