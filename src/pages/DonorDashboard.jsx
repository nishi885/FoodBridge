import React, { useEffect, useState } from 'react';
import { getAllRequests, getDonorFoods, addFood, acceptRequest } from '../services/api';
import FoodCard from '../components/FoodCard';
import RequestCard from '../components/RequestCard';

const DonorDashboard = ({ user, onLogout }) => {
  const [foodList, setFoodList] = useState([]);
  const [ngoRequests, setNgoRequests] = useState([]);
  const [formState, setFormState] = useState({ type: '', quantity: '', expiry: '', location: '' });
  const [status, setStatus] = useState('');

  const loadData = async () => {
    setStatus('Loading...');
    try {
      const foods = await getDonorFoods(user.id);
      setFoodList(foods);
      const allReqs = await getAllRequests();
      // only requests for this donor foods
      setNgoRequests(allReqs.filter((r) => r.food?.donorId === user.id));
      setStatus('');
    } catch (e) {
      setStatus(e.message || 'Failed to load');
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAddFood = async (e) => {
    e.preventDefault();
    setStatus('Saving food...');

    try {
      await addFood({
        donorId: user.id,
        type: formState.type,
        quantity: formState.quantity,
        expiry: formState.expiry,
        location: formState.location,
      });
      setFormState({ type: '', quantity: '', expiry: '', location: '' });
      await loadData();
      setStatus('Food added successfully');
    } catch (err) {
      setStatus(err.message || 'Error adding food');
    }
  };

  const handleAccept = async (request) => {
    setStatus('Accepting request...');
    try {
      await acceptRequest({ donorId: user.id, requestId: request.id });
      await loadData();
      setStatus('Request accepted');
    } catch (err) {
      setStatus(err.message || 'Error accepting');
    }
  };

  return (
    <div className="page-wrapper">
      <div className="top-bar">
        <h1>Donor Dashboard</h1>
        <div>
          <span>Welcome, {user.name}</span>
          <button className="btn-secondary" onClick={onLogout}>Logout</button>
        </div>
      </div>

      <div className="grid-container">
        <section className="panel">
          <h2>Add Food</h2>
          <form onSubmit={handleAddFood} className="donor-form">
            <label>Type<input value={formState.type} onChange={(e) => setFormState({ ...formState, type: e.target.value })} required /></label>
            <label>Quantity<input value={formState.quantity} onChange={(e) => setFormState({ ...formState, quantity: e.target.value })} required /></label>
            <label>Expiry<input type="datetime-local" value={formState.expiry} onChange={(e) => setFormState({ ...formState, expiry: e.target.value })} required /></label>
            <label>Location<input value={formState.location} onChange={(e) => setFormState({ ...formState, location: e.target.value })} required /></label>
            <button className="btn-primary" type="submit">Add Food</button>
          </form>
        </section>

        <section className="panel">
          <h2>Your Food Listings</h2>
          {foodList.length === 0 ? <p>No food added yet.</p> : foodList.map((item) => <FoodCard key={item.id} item={item} />)}
        </section>

        <section className="panel">
          <h2>NGO Requests</h2>
          {ngoRequests.length === 0 ? <p>No requests for your foods yet.</p> : ngoRequests.map((req) => (
            <RequestCard key={req.id} request={req} onAccept={handleAccept} />
          ))}
        </section>
      </div>

      {status && <p className="status">{status}</p>}
    </div>
  );
};

export default DonorDashboard;
