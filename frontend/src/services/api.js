import axios from 'axios';

// Create axios instance with actual backend URL
const apiClient = axios.create({
  baseURL: 'http://localhost:3000/api',
  timeout: 5000,
});

// Add JWT token to requests if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const signup = async ({ name, email, password, role, location }) => {
  try {
    const backendRole = role === 'donor' ? 'restaurant' : role;

    const response = await apiClient.post('/auth/signup', {
      name,
      email,
      password,
      role: backendRole,
      location: location || 'Default Location',
    });

    const { token, user } = response.data;

    const frontendUser = { ...user, role };
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(frontendUser));

    return frontendUser;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Signup failed');
  }
};

export const login = async ({ email, password, role }) => {
  try {
    const response = await apiClient.post('/auth/login', {
      email,
      password,
    });

    const { token, user } = response.data;

    const frontendRole = user.role === 'restaurant' ? 'donor' : user.role;

    if (frontendRole !== role) {
      throw new Error('Invalid role for this account');
    }

    const frontendUser = { ...user, role: frontendRole };
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(frontendUser));

    return frontendUser;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Login failed');
  }
};

export const getDonorFoods = async (donorId) => {
  try {
    const response = await apiClient.get('/food/restaurant/my-foods');
    return response.data.foods || [];
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to load foods');
  }
};

export const addFood = async ({ donorId, type, quantity, expiry, location }) => {
  try {
    const response = await apiClient.post('/food/add', {
      type,
      quantity,
      expiry,
      location,
    });
    return response.data.food;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to add food');
  }
};

export const getAvailableFoods = async () => {
  try {
    const response = await apiClient.get('/food/available');
    return response.data.foods || [];
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to load foods');
  }
};

export const requestFood = async ({ ngoId, foodId }) => {
  try {
    const response = await apiClient.post('/request/request', {
      foodId,
    });
    return response.data.request;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to request food');
  }
};

export const getNgoRequests = async (ngoId) => {
  try {
    const response = await apiClient.get('/request/ngo/my-requests');
    return response.data.requests || [];
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to load requests');
  }
};

export const getAllRequests = async () => {
  try {
    const response = await apiClient.get('/request/restaurant/requests');
    return response.data.requests || [];
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to load requests');
  }
};

export const acceptRequest = async ({ donorId, requestId }) => {
  try {
    const response = await apiClient.post('/request/accept', {
      requestId,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to accept request');
  }
};
  return response.data;
};
