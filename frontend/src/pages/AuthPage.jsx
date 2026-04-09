import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, signup } from '../services/api';

const AuthPage = ({ setUser }) => {
  const [mode, setMode] = useState('login');
  const [role, setRole] = useState('donor');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');

    try {
      let user;
      if (mode === 'signup') {
        user = await signup({ name, email, role });
      } else {
        user = await login({ email, role });
      }
      setUser(user);
      if (user.role === 'donor') navigate('/donor');
      else navigate('/ngo');
    } catch (err) {
      setError(err.message || 'Something went wrong');
    }
  };

  return (
    <div className="page-wrapper">
      <div className="panel">
        <h1>FoodBridge</h1>
        <p>Connect donors with NGOs and reduce food waste.</p>
        <div className="tab-row">
          <button className={mode === 'login' ? 'tab active' : 'tab'} onClick={() => setMode('login')}>
            Login
          </button>
          <button className={mode === 'signup' ? 'tab active' : 'tab'} onClick={() => setMode('signup')}>
            Signup
          </button>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {mode === 'signup' && (
            <label>
              Name
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                placeholder="Your full name"
              />
            </label>
          )}

          <label>
            Email
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="you@example.com"
            />
          </label>

          <label>
            Role
            <select value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="donor">Donor</option>
              <option value="ngo">NGO</option>
            </select>
          </label>

          {error && <p className="error">{error}</p>}

          <button className="btn-primary" type="submit">
            {mode === 'signup' ? 'Create Account' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default AuthPage;
