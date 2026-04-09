import React from 'react';

const RequestCard = ({ request, onAccept }) => {
  return (
    <div className="card">
      <div className="card-header">
        <h4>Request for: {request.food?.type || 'Unknown'}</h4>
        <span className="badge badge-info">{request.status.toUpperCase()}</span>
      </div>
      <div className="card-content">
        <p><strong>Quantity:</strong> {request.food?.quantity}</p>
        <p><strong>NGO:</strong> {request.ngo?.name || request.ngoId}</p>
        <p><strong>Requested:</strong> {new Date(request.requestedAt).toLocaleString()}</p>
      </div>
      {onAccept && request.status === 'pending' && (
        <button className="btn-primary" onClick={() => onAccept(request)}>
          Accept Request
        </button>
      )}
    </div>
  );
};

export default RequestCard;
