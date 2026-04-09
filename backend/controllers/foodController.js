import Food from '../models/Food.js';
import Request from '../models/Request.js';
import User from '../models/User.js';
import { asyncHandler } from '../middleware/errorHandler.js';

export const addFood = asyncHandler(async (req, res) => {
  const { foodType, quantity, description, expiryTime, location, image } = req.body;

  // Validation
  if (!foodType || !quantity || !expiryTime || !location) {
    return res.status(400).json({
      error: 'Please provide foodType, quantity, expiryTime, and location',
    });
  }

  // Check if expiry time is in the future
  if (new Date(expiryTime) <= new Date()) {
    return res.status(400).json({
      error: 'Expiry time must be in the future',
    });
  }

  const food = new Food({
    restaurantId: req.user.id,
    foodType,
    quantity,
    description,
    expiryTime,
    location,
    image,
  });

  await food.save();

  // Populate restaurant details
  await food.populate('restaurantId', 'name email location phone');

  res.status(201).json({
    message: 'Food item added successfully',
    food,
  });
});

export const getAvailableFoods = asyncHandler(async (req, res) => {
  const foods = await Food.find({ status: 'available' })
    .populate('restaurantId', 'name email location phone')
    .sort({ expiryTime: 1 });

  res.status(200).json({
    count: foods.length,
    foods,
  });
});

export const getRestaurantFoods = asyncHandler(async (req, res) => {
  const foods = await Food.find({ restaurantId: req.user.id })
    .sort({ createdAt: -1 });

  res.status(200).json({
    count: foods.length,
    foods,
  });
});

export const getFoodById = asyncHandler(async (req, res) => {
  const food = await Food.findById(req.params.id).populate(
    'restaurantId',
    'name email location phone'
  );

  if (!food) {
    return res.status(404).json({ error: 'Food item not found' });
  }

  res.status(200).json({ food });
});

export const updateFoodStatus = asyncHandler(async (req, res) => {
  const { status } = req.body;

  const validStatuses = ['available', 'requested', 'fulfilled', 'expired'];
  if (!validStatuses.includes(status)) {
    return res.status(400).json({
      error: `Status must be one of: ${validStatuses.join(', ')}`,
    });
  }

  const food = await Food.findById(req.params.id);

  if (!food) {
    return res.status(404).json({ error: 'Food item not found' });
  }

  // Only restaurant owner can update their own food
  if (food.restaurantId.toString() !== req.user.id) {
    return res.status(403).json({
      error: 'You can only update your own food items',
    });
  }

  food.status = status;
  await food.save();

  res.status(200).json({
    message: 'Food status updated successfully',
    food,
  });
});

export const deleteFood = asyncHandler(async (req, res) => {
  const food = await Food.findById(req.params.id);

  if (!food) {
    return res.status(404).json({ error: 'Food item not found' });
  }

  // Only restaurant owner can delete their own food
  if (food.restaurantId.toString() !== req.user.id) {
    return res.status(403).json({
      error: 'You can only delete your own food items',
    });
  }

  await Food.findByIdAndDelete(req.params.id);

  res.status(200).json({
    message: 'Food item deleted successfully',
  });
});

export const searchFoods = asyncHandler(async (req, res) => {
  const { foodType, location } = req.query;

  let filter = { status: 'available' };

  if (foodType) {
    filter.foodType = { $regex: foodType, $options: 'i' };
  }

  if (location) {
    filter.location = { $regex: location, $options: 'i' };
  }

  const foods = await Food.find(filter)
    .populate('restaurantId', 'name email location phone')
    .sort({ expiryTime: 1 });

  res.status(200).json({
    count: foods.length,
    foods,
  });
});
