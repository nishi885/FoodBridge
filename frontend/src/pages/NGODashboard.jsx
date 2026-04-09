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
    <div className="page-wrapper">
      <div className="top-bar">
        <h1>NGO Dashboard</h1>
        <div>
          <span>Welcome, {user.name}</span>
          <button className="btn-secondary" onClick={onLogout}>Logout</button>
        </div>
      </div>

      <div className="grid-container">
        <section className="panel">
          <h2>Available Food Listings</h2>
          {foods.length === 0 ? <p>No food currently available.</p> : foods.map((item) => (
            <FoodCard key={item.id} item={item} onAction={handleRequest} actionLabel="Request" />
          ))}
        </section>

        <section className="panel">
          <h2>Your Request Status</h2>
          {requests.length === 0 ? <p>No requests placed yet.</p> : requests.map((req) => (
            <div key={req.id} className="card">
              <div className="card-header">
                <h4>{req.food?.type || 'Unknown'}</h4>
                <span className="badge badge-info">{req.status.toUpperCase()}</span>
              </div>
              <div className="card-content">
                <p><strong>Quantity:</strong> {req.food?.quantity}</p>
                <p><strong>Requested On:</strong> {new Date(req.requestedAt).toLocaleString()}</p>
              </div>
            </div>
          ))}
        </section>
      </div>

      {status && <p className="status">{status}</p>}
    </div>
  );
};

export default NGODashboard;
