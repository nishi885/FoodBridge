import Request from '../models/Request.js';
import Food from '../models/Food.js';
import User from '../models/User.js';
import { asyncHandler } from '../middleware/errorHandler.js';

export const requestFood = asyncHandler(async (req, res) => {
  const { foodId, notes, pickupLocation } = req.body;

  // Validation
  if (!foodId) {
    return res.status(400).json({
      error: 'Please provide a food ID',
    });
  }

  // Check if food exists and is available
  const food = await Food.findById(foodId);

  if (!food) {
    return res.status(404).json({ error: 'Food item not found' });
  }

  if (food.status !== 'available') {
    return res.status(400).json({
      error: 'This food item is no longer available',
    });
  }

  // Check if this NGO already has a pending request for this food
  const existingRequest = await Request.findOne({
    foodId,
    ngoId: req.user.id,
    status: 'pending',
  });

  if (existingRequest) {
    return res.status(400).json({
      error: 'You already have a pending request for this food item',
    });
  }

  // Create request
  const foodRequest = new Request({
    ngoId: req.user.id,
    foodId,
    restaurantId: food.restaurantId,
    notes,
    pickupLocation,
  });

  await foodRequest.save();

  // Update food status to requested
  food.status = 'requested';
  await food.save();

  // Populate references
  await foodRequest.populate([
    { path: 'ngoId', select: 'name email location phone' },
    { path: 'foodId', select: 'foodType quantity expiryTime' },
    { path: 'restaurantId', select: 'name email location phone' },
  ]);

  res.status(201).json({
    message: 'Food request created successfully',
    request: foodRequest,
  });
});

export const acceptRequest = asyncHandler(async (req, res) => {
  const { requestId } = req.body;

  // Validation
  if (!requestId) {
    return res.status(400).json({
      error: 'Please provide a request ID',
    });
  }

  const foodRequest = await Request.findById(requestId);

  if (!foodRequest) {
    return res.status(404).json({ error: 'Request not found' });
  }

  // Check if restaurant owns this food
  if (foodRequest.restaurantId.toString() !== req.user.id) {
    return res.status(403).json({
      error: 'You can only accept requests for your own food items',
    });
  }

  // Check if request is still pending
  if (foodRequest.status !== 'pending') {
    return res.status(400).json({
      error: 'This request has already been processed',
    });
  }

  // Update request status
  foodRequest.status = 'accepted';
  foodRequest.acceptedAt = new Date();
  await foodRequest.save();

  // Update food status to fulfilled
  const food = await Food.findById(foodRequest.foodId);
  food.status = 'fulfilled';
  await food.save();

  // Reject other pending requests for this food item
  await Request.updateMany(
    {
      foodId: foodRequest.foodId,
      _id: { $ne: requestId },
      status: 'pending',
    },
    { status: 'rejected' }
  );

  await foodRequest.populate([
    { path: 'ngoId', select: 'name email location phone' },
    { path: 'foodId', select: 'foodType quantity expiryTime' },
    { path: 'restaurantId', select: 'name email location phone' },
  ]);

  res.status(200).json({
    message: 'Request accepted successfully',
    request: foodRequest,
  });
});

export const rejectRequest = asyncHandler(async (req, res) => {
  const { requestId } = req.body;

  const foodRequest = await Request.findById(requestId);

  if (!foodRequest) {
    return res.status(404).json({ error: 'Request not found' });
  }

  // Check if restaurant owns this food
  if (foodRequest.restaurantId.toString() !== req.user.id) {
    return res.status(403).json({
      error: 'You can only reject requests for your own food items',
    });
  }

  if (foodRequest.status !== 'pending') {
    return res.status(400).json({
      error: 'Request cannot be rejected in its current status',
    });
  }

  foodRequest.status = 'rejected';
  await foodRequest.save();

  res.status(200).json({
    message: 'Request rejected successfully',
    request: foodRequest,
  });
});

export const getNGORequests = asyncHandler(async (req, res) => {
  const requests = await Request.find({ ngoId: req.user.id })
    .populate('foodId', 'foodType quantity expiryTime location')
    .populate('restaurantId', 'name email location phone')
    .sort({ requestedAt: -1 });

  res.status(200).json({
    count: requests.length,
    requests,
  });
});

export const getRestaurantRequests = asyncHandler(async (req, res) => {
  const requests = await Request.find({ restaurantId: req.user.id })
    .populate('ngoId', 'name email location phone')
    .populate('foodId', 'foodType quantity expiryTime')
    .sort({ requestedAt: -1 });

  res.status(200).json({
    count: requests.length,
    requests,
  });
});

export const getRequestById = asyncHandler(async (req, res) => {
  const request = await Request.findById(req.params.id).populate([
    { path: 'ngoId', select: 'name email location phone' },
    { path: 'foodId', select: 'foodType quantity expiryTime location' },
    { path: 'restaurantId', select: 'name email location phone' },
  ]);

  if (!request) {
    return res.status(404).json({ error: 'Request not found' });
  }

  res.status(200).json({ request });
});

export const updateRequestStatus = asyncHandler(async (req, res) => {
  const { status } = req.body;

  const validStatuses = ['pending', 'accepted', 'rejected', 'completed'];
  if (!validStatuses.includes(status)) {
    return res.status(400).json({
      error: `Status must be one of: ${validStatuses.join(', ')}`,
    });
  }

  const foodRequest = await Request.findById(req.params.id);

  if (!foodRequest) {
    return res.status(404).json({ error: 'Request not found' });
  }

  // Check authorization
  if (
    foodRequest.restaurantId.toString() !== req.user.id &&
    foodRequest.ngoId.toString() !== req.user.id
  ) {
    return res.status(403).json({
      error: 'You do not have permission to update this request',
    });
  }

  foodRequest.status = status;
  await foodRequest.save();

  res.status(200).json({
    message: 'Request status updated successfully',
    request: foodRequest,
  });
});

export const getAllRequests = asyncHandler(async (req, res) => {
  const requests = await Request.find()
    .populate('ngoId', 'name email location')
    .populate('foodId', 'foodType quantity')
    .populate('restaurantId', 'name email location')
    .sort({ requestedAt: -1 });

  res.status(200).json({
    count: requests.length,
    requests,
  });
});
