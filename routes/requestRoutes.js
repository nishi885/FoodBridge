import express from 'express';
import {
  requestFood,
  acceptRequest,
  rejectRequest,
  getNGORequests,
  getRestaurantRequests,
  getRequestById,
  updateRequestStatus,
  getAllRequests,
} from '../controllers/requestController.js';
import { authenticateToken, authorizeRole } from '../middleware/auth.js';

const router = express.Router();

// NGO routes
router.post(
  '/request',
  authenticateToken,
  authorizeRole(['ngo']),
  requestFood
);
router.get(
  '/ngo/my-requests',
  authenticateToken,
  authorizeRole(['ngo']),
  getNGORequests
);

// Restaurant routes
router.post(
  '/accept',
  authenticateToken,
  authorizeRole(['restaurant']),
  acceptRequest
);
router.post(
  '/reject',
  authenticateToken,
  authorizeRole(['restaurant']),
  rejectRequest
);
router.get(
  '/restaurant/requests',
  authenticateToken,
  authorizeRole(['restaurant']),
  getRestaurantRequests
);

// Protected routes accessible by both
router.get('/:id', authenticateToken, getRequestById);
router.put(
  '/:id/status',
  authenticateToken,
  updateRequestStatus
);

// Admin routes
router.get('/', authenticateToken, authorizeRole(['admin']), getAllRequests);

export default router;
