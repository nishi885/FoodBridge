import mongoose from 'mongoose';

const requestSchema = new mongoose.Schema(
  {
    ngoId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: [true, 'Please provide an NGO ID'],
    },
    foodId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Food',
      required: [true, 'Please provide a food ID'],
    },
    restaurantId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: [true, 'Please provide a restaurant ID'],
    },
    status: {
      type: String,
      enum: ['pending', 'accepted', 'rejected', 'completed'],
      default: 'pending',
    },
    requestedAt: {
      type: Date,
      default: Date.now,
    },
    acceptedAt: {
      type: Date,
      default: null,
    },
    notes: {
      type: String,
      default: '',
    },
    pickupLocation: {
      type: String,
      default: '',
    },
  },
  { timestamps: true }
);

// Index for finding requests by NGO or Restaurant
requestSchema.index({ ngoId: 1, status: 1 });
requestSchema.index({ restaurantId: 1, status: 1 });
requestSchema.index({ foodId: 1 });

export default mongoose.model('Request', requestSchema);
