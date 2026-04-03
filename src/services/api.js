import axios from 'axios';

// Create axios instance (change baseURL to real API when available)
const apiClient = axios.create({
  baseURL: 'https://example.com/api',
  timeout: 5000,
});

// Mock data to simulate an API in memory.
let donors = [];
let ngos = [];
let foodItems = [];
let requests = [];

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export const signup = async ({ name, email, role }) => {
  await sleep(300);

  const existing = (role === 'donor' ? donors : ngos).find((u) => u.email === email);
  if (existing) {
    throw new Error('Email already registered');
  }

  const newUser = {
    id: Date.now() + Math.random(),
    name,
    email,
    role,
  };

  if (role === 'donor') donors.push(newUser);
  else ngos.push(newUser);

  return newUser;
};

export const login = async ({ email, role }) => {
  await sleep(300);

  const found = (role === 'donor' ? donors : ngos).find((u) => u.email === email);
  if (!found) {
    throw new Error('User not found');
  }
  return found;
};

export const getDonorFoods = async (donorId) => {
  await sleep(300);
  return foodItems.filter((item) => item.donorId === donorId);
};

export const addFood = async ({ donorId, type, quantity, expiry, location }) => {
  await sleep(300);
  const food = {
    id: Date.now() + Math.random(),
    donorId,
    type,
    quantity,
    expiry,
    location,
    createdAt: new Date().toISOString(),
    status: 'available',
  };
  foodItems.unshift(food);
  return food;
};

export const getAvailableFoods = async () => {
  await sleep(300);
  return foodItems.filter((item) => item.status === 'available');
};

export const requestFood = async ({ ngoId, foodId }) => {
  await sleep(300);
  const item = foodItems.find((f) => f.id === foodId);
  if (!item || item.status !== 'available') {
    throw new Error('Food not available');
  }

  item.status = 'requested';
  requests.push({
    id: Date.now() + Math.random(),
    ngoId,
    foodId,
    status: 'pending',
    requestedAt: new Date().toISOString(),
  });

  return item;
};

export const getNgoRequests = async (ngoId) => {
  await sleep(300);
  return requests
    .filter((r) => r.ngoId === ngoId)
    .map((r) => {
      const food = foodItems.find((f) => f.id === r.foodId);
      return {
        ...r,
        food,
      };
    });
};

export const getAllRequests = async () => {
  await sleep(300);
  return requests.map((r) => {
    const food = foodItems.find((f) => f.id === r.foodId);
    const donor = donors.find((d) => d.id === food?.donorId);
    const ngo = ngos.find((n) => n.id === r.ngoId);
    return { ...r, food, donor, ngo };
  });
};

export const acceptRequest = async ({ donorId, requestId }) => {
  await sleep(300);
  const req = requests.find((r) => r.id === requestId);
  if (!req) throw new Error('Request not found');

  const item = foodItems.find((f) => f.id === req.foodId);
  if (!item || item.donorId !== donorId) throw new Error('Not allowed');

  req.status = 'accepted';
  item.status = 'fulfilled';
  return req;
};

// Example of real API call usage if endpoint exists
export const realFetchFoods = async () => {
  const response = await apiClient.get('/foods');
  return response.data;
};
