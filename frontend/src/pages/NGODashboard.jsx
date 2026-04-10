import React, { useEffect, useState } from 'react';
import { getAvailableFoods, requestFood, getNgoRequests } from '../services/api';
import FoodCard from '../components/FoodCard';

const NGODashboard = ({ user, onLogout }) => {
  const [foods, setFoods] = useState([]);
  const [requests, setRequests] = useState([]);
  const [status, setStatus] = useState('');

  const loadData = async () => {
    setStatus('Loading...');
    try {
      setFoods(await getAvailableFoods());
      setRequests(await getNgoRequests(user.id));
      setStatus('');
    } catch (e) {
      setStatus(e.message || 'Failed to load');
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRequest = async (item) => {
    setStatus('Requesting food...');
    try {
      await requestFood({ ngoId: user.id, foodId: item.id });
      await loadData();
      setStatus('Food request sent');
    } catch (err) {
      setStatus(err.message || 'Failed request');
    }
  };

  return (
    <div>
      <div className="top-bar">
        <h1>🏢 NGO Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {user.name}</span>
          <button className="btn-secondary" onClick={onLogout}>Logout</button>
        </div>
      </div>

      <div className="grid-container">
        <section className="dashboard-section">
          <h2>🍎 Available Food Donations</h2>
          {foods.length === 0 ? (
            <p style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '40px' }}>
              No food donations available right now. Check back later! 🌱
            </p>
          ) : (
            foods.map((item) => (
              <FoodCard key={item.id} item={item} onAction={handleRequest} actionLabel="Request Food" />
            ))
          )}
        </section>

        <section className="dashboard-section">
          <h2>📋 Your Food Requests</h2>
          {requests.length === 0 ? (
            <p style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '40px' }}>
              No requests placed yet. Browse available donations above! 🤝
            </p>
          ) : (
            requests.map((req) => (
              <div key={req.id} className="card">
                <div className="card-header">
                  <h3>{req.food?.type || 'Unknown Food'}</h3>
                  <span className={`badge ${
                    req.status === 'pending' ? 'badge-urgent' :
                    req.status === 'accepted' ? 'badge-available' :
                    'badge-unavailable'
                  }`}>
                    {req.status.toUpperCase()}
                  </span>
                </div>
                <div className="card-content">
                  <p><strong>Quantity:</strong> {req.food?.quantity}</p>
                  <p><strong>Location:</strong> {req.food?.location}</p>
                  <p><strong>Requested On:</strong> {new Date(req.requestedAt).toLocaleString()}</p>
                </div>
              </div>
            ))
          )}
        </section>
      </div>

      {status && <p className="status">{status}</p>}
    </div>
  );
};

export default NGODashboard;
