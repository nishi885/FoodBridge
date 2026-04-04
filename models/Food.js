import mongoose from 'mongoose';

const foodSchema = new mongoose.Schema(
  {
    restaurantId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: [true, 'Please provide a restaurant ID'],
    },
    foodType: {
      type: String,
      required: [true, 'Please provide a food type'],
      trim: true,
    },
    quantity: {
      type: String,
      required: [true, 'Please provide quantity'],
      trim: true,
    },
    description: {
      type: String,
      default: '',
    },
    expiryTime: {
      type: Date,
      required: [true, 'Please provide expiry time'],
    },
    location: {
      type: String,
      required: [true, 'Please provide location'],
    },
    status: {
      type: String,
      enum: ['available', 'requested', 'fulfilled', 'expired'],
      default: 'available',
    },
    image: {
      type: String,
      default: '',
    },
    createdAt: {
      type: Date,
      default: Date.now,
    },
  },
  { timestamps: true }
);

// Index for finding available foods and sorting by expiry
foodSchema.index({ status: 1, expiryTime: 1 });

export default mongoose.model('Food', foodSchema);
