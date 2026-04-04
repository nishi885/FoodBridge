import User from '../models/User.js';
import jwt from 'jsonwebtoken';
import { asyncHandler } from '../middleware/errorHandler.js';

const generateToken = (userId, email, role) => {
  return jwt.sign(
    { id: userId, email, role },
    process.env.JWT_SECRET,
    { expiresIn: '7d' }
  );
};

export const signup = asyncHandler(async (req, res) => {
  const { name, email, password, role, location, phone, description } = req.body;

  // Validation
  if (!name || !email || !password || !location) {
    return res.status(400).json({
      error: 'Please provide name, email, password, and location',
    });
  }

  // Check if user already exists
  const existingUser = await User.findOne({ email });
  if (existingUser) {
    return res.status(400).json({ error: 'Email already registered' });
  }

  // Create new user
  const user = new User({
    name,
    email,
    password,
    role: role || 'restaurant',
    location,
    phone,
    description,
  });

  await user.save();

  // Generate token
  const token = generateToken(user._id, user.email, user.role);

  // Return user without password
  const userResponse = user.toObject();
  delete userResponse.password;

  res.status(201).json({
    message: 'User registered successfully',
    token,
    user: userResponse,
  });
});

export const login = asyncHandler(async (req, res) => {
  const { email, password } = req.body;

  // Validation
  if (!email || !password) {
    return res.status(400).json({
      error: 'Please provide email and password',
    });
  }

  // Find user and include password field
  const user = await User.findOne({ email }).select('+password');

  if (!user) {
    return res.status(401).json({ error: 'Invalid email or password' });
  }

  // Check password
  const isPasswordValid = await user.matchPassword(password);

  if (!isPasswordValid) {
    return res.status(401).json({ error: 'Invalid email or password' });
  }

  // Generate token
  const token = generateToken(user._id, user.email, user.role);

  // Return user without password
  const userResponse = user.toObject();
  delete userResponse.password;

  res.status(200).json({
    message: 'Login successful',
    token,
    user: userResponse,
  });
});

export const getProfile = asyncHandler(async (req, res) => {
  const user = await User.findById(req.user.id);

  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  res.status(200).json({ user });
});

export const updateProfile = asyncHandler(async (req, res) => {
  const { name, phone, description, location } = req.body;

  const user = await User.findByIdAndUpdate(
    req.user.id,
    { name, phone, description, location },
    { new: true, runValidators: true }
  );

  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  res.status(200).json({
    message: 'Profile updated successfully',
    user,
  });
});
