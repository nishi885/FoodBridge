import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, signup } from '../services/api';

const AuthPage = ({ setUser }) => {
  const [mode, setMode] = useState('login');
  const [role, setRole] = useState('donor');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    location: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const token = localStorage.getItem('token');

    if (storedUser && token) {
      try {
        const user = JSON.parse(storedUser);
        setUser(user);
        if (user.role === 'donor') navigate('/donor');
        else navigate('/ngo');
      } catch (error) {
        localStorage.removeItem('user');
        localStorage.removeItem('token');
      }
    }
  }, [setUser, navigate]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      let user;
      if (mode === 'signup') {
        user = await signup({
          name: formData.name,
          email: formData.email,
          password: formData.password,
          role,
          location: formData.location,
        });
      } else {
        user = await login({
          email: formData.email,
          password: formData.password,
          role,
        });
      }
      setUser(user);
      if (user.role === 'donor') navigate('/donor');
      else navigate('/ngo');
    } catch (err) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setMode(mode === 'login' ? 'signup' : 'login');
    setError('');
    setFormData({
      name: '',
      email: '',
      password: '',
      location: '',
    });
  };

  return (
    <div className="page-wrapper">
      <div className="panel">
        <div className="auth-header">
          <h1>🍎 FoodBridge</h1>
          <p>Connect donors with NGOs and reduce food waste.</p>
        </div>
        <div className="tab-row">
          <button className={`tab ${mode === 'login' ? 'active' : ''}`} onClick={() => setMode('login')}>
            Login
          </button>
          <button className={`tab ${mode === 'signup' ? 'active' : ''}`} onClick={() => setMode('signup')}>
            Signup
          </button>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {mode === 'signup' && (
            <label>
              Name
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                required
                placeholder="Your full name"
                disabled={loading}
              />
            </label>
          )}

          <label>
            Email
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              required
              placeholder="you@example.com"
              disabled={loading}
            />
          </label>

          <label>
            Password
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              required
              placeholder="Enter your password"
              minLength="6"
              disabled={loading}
            />
          </label>

          {mode === 'signup' && (
            <label>
              Location
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleInputChange}
                required
                placeholder="Your city/location"
                disabled={loading}
              />
            </label>
          )}

          <label>
            Role
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              disabled={loading}
            >
              <option value="donor">🍎 Donor</option>
              <option value="ngo">🏢 NGO</option>
            </select>
          </label>

          {error && <p className="error">{error}</p>}

          <button className="btn-primary" type="submit" disabled={loading}>
            {loading ? 'Please wait...' : (mode === 'signup' ? 'Create Account' : 'Login')}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <button
            className="btn-secondary"
            onClick={toggleMode}
            disabled={loading}
            style={{ fontSize: '0.9rem' }}
          >
            {mode === 'login' ? "Don't have an account? Sign up" : 'Already have an account? Login'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
