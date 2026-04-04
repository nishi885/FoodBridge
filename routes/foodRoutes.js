import express from 'express';
import {
  addFood,
  getAvailableFoods,
  getRestaurantFoods,
  getFoodById,
  updateFoodStatus,
  deleteFood,
  searchFoods,
} from '../controllers/foodController.js';
import { authenticateToken, authorizeRole } from '../middleware/auth.js';

const router = express.Router();

// Public routes
router.get('/available', getAvailableFoods);
router.get('/search', searchFoods);
router.get('/:id', getFoodById);

// Protected routes for restaurant
router.post
('/add', authenticateToken, authorizeRole(['restaurant']), addFood);
router.get('/restaurant/my-foods', authenticateToken, getRestaurantFoods);
router.put(
  '/:id/status',
  authenticateToken,
  authorizeRole(['restaurant']),
  updateFoodStatus
);
router.delete(
  '/:id',
  authenticateToken,
  authorizeRole(['restaurant']),
  deleteFood
);

export default router;
