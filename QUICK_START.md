# FoodBridge Backend - Quick Start Guide

## 📦 Installation Complete!

Your FoodBridge backend is ready to use. Follow these steps to get it running.

## 1️⃣ Prerequisites

Make sure you have:
- **Node.js** (v14 or higher) - [Download](https://nodejs.org/)
- **MongoDB** (v4.4 or higher) - [Download](https://www.mongodb.com/try/download/community)
- **MongoDB Compass** (optional) - [Download](https://www.mongodb.com/products/compass)

## 2️⃣ Start MongoDB

**On Mac (using Homebrew):**
```bash
brew services start mongodb-community
```

**On Windows:**
- Download MongoDB Community Server
- During installation, choose to install as a service
- MongoDB will start automatically

**On Linux/Ubuntu:**
```bash
sudo systemctl start mongod
```

**Verify MongoDB is running:**
```bash
mongosh  # or mongo
> use foodbridge
> exit
```

## 3️⃣ Start the Backend Server

```bash
cd /Users/Aanchal/Desktop/Food_Bridge/backend

# Install dependencies (if not already done)
npm install

# Start development server
npm run dev

# OR production mode
npm start
```

Expected output:
```
🚀 Server running on http://localhost:5000
Environment: development
MongoDB Connected: localhost
```

## 4️⃣ Test the API

Open a new terminal and test:

```bash
# Health check
curl http://localhost:5000/api/health

# Should return:
# {"message":"Server is running"}
```

## 5️⃣ Connect MongoDB Compass (Optional but Recommended!)

1. **Open MongoDB Compass**
2. **Click "New Connection"**
3. **Connection string:** `mongodb://localhost:27017`
4. **Click "Connect"**
5. **Create test data:**
   - Right-click "Databases" → "Create Database"
   - Database: `foodbridge`
6. **As you use the API, watch data appear in Compass!**

## 6️⃣ Frontend Connection

Update your frontend `.env` or API base URL to point to the backend:

```javascript
// In your React/Frontend code
const API_BASE_URL = 'http://localhost:5000/api';
```

Or create a `.env` file in the frontend:
```
VITE_API_URL=http://localhost:5000/api
```

## 📚 API Endpoints Quick Reference

### Authentication
- `POST /api/auth/signup` - Register
- `POST /api/auth/login` - Login
- `GET /api/auth/profile` - Get my profile (needs token)

### Food (Restaurant)
- `POST /api/food/add` - Add food (needs token, restaurant only)
- `GET /api/food/available` - See all available food
- `GET /api/food/search?foodType=pizza` - Search food

###  Requests (NGO)
- `POST /api/request/request` - Request food (needs token, NGO only)
- `GET /api/request/ngo/my-requests` - My requests (needs token)

## 🧪 Test with Postman/Thunder Client

1. **Download** [Postman](https://www.postman.com/downloads/) or [Thunder Client](https://www.thunderclient.com/)
2. **Import requests from API_DOCUMENTATION.md**
3. **Set Authorization header for protected routes:**
   ```
   Authorization: Bearer <your_jwt_token>
   ```

## 📝 Example API Request (using curl)

```bash
# 1. Register a restaurant
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pizza Palace",
    "email": "pizza@example.com",
    "password": "password123",
    "role": "restaurant",
    "location": "New Delhi",
    "phone": "9876543210"
  }'

# Response will include a token - save it!

# 2. Add food (replace TOKEN with actual token)
curl -X POST http://localhost:5000/api/food/add \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "foodType": "Margherita Pizza",
    "quantity": "20 servings",
    "expiryTime": "2024-04-05T22:00:00Z",
    "location": "Connaught Place, Delhi"
  }'

# 3. Get available foods
curl http://localhost:5000/api/food/available
```

## ⚙️ Database Setup

### Automatic Setup (Recommended)
When you make your first API request, MongoDB will automatically create:
- `foodbridge` database
- Collections: `users`, `foods`, `requests`

### Manual Setup (Optional)
```bash
# Connect to MongoDB
mongosh

# Create database and collections
use foodbridge

db.createCollection('users')
db.createCollection('foods')
db.createCollection('requests')

# Add indexes for better performance
db.foods.createIndex({ status: 1, expiryTime: 1 })
db.requests.createIndex({ ngoId: 1, status: 1 })
db.requests.createIndex({ restaurantId: 1, status: 1 })
```

## 🐛 Troubleshooting

### "MongoDB is not running"
```bash
# Check if MongoDB is running
ps aux | grep mongod

# Start MongoDB
brew services start mongodb-community  # Mac
sudo systemctl start mongod  # Linux
```

### "Port 5000 already in use"
```bash
# Find process on port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or change port in .env
PORT=5001
```

### "Cannot connect to MongoDB"
- Verify MongoDB is running
- Check `.env` MONGODB_URI is correct: `mongodb://localhost:27017/foodbridge`
- Make sure MongoDB service is started

### "JWT token errors"
- Token is valid for 7 days
- Include token in Authorization header: `Bearer <token>`
- Token format: `Authorization: Bearer eyJhbGciOi...`

## 📂 Project Structure

```
backend/
├── config/database.js       ← MongoDB connection
├── models/                  ← Database schemas
│   ├── User.js
│   ├── Food.js
│   └── Request.js
├── controllers/             ← Business logic
│   ├── authController.js
│   ├── foodController.js
│   └── requestController.js
├── routes/                  ← API endpoints
│   ├── authRoutes.js
│   ├── foodRoutes.js
│   └── requestRoutes.js
├── middleware/              ← Authentication & errors
│   ├── auth.js
│   └── errorHandler.js
├── server.js               ← Main server file
├── .env                    ← Environment variables
├── package.json            ← Dependencies
├── README.md              ← Full documentation
└── API_DOCUMENTATION.md   ← API reference
```

## 🔐 Security Notes

Before production:
1. Change `JWT_SECRET` in `.env` to a strong random string
2. Use HTTPS instead of HTTP
3. Set `NODE_ENV=production`
4. Add rate limiting
5. Implement CSRF protection

## 📞 Need Help?

- Check `README.md` for detailed documentation
- See `API_DOCUMENTATION.md` for all endpoints
- Review example curl commands in `QUICK_START.md`

---

**Ready to go!** 🚀

```bash
# Final commands to start everything:
npm install          # One time
npm run dev          # Development (auto-reload)
npm start           # Production
```

Enjoy building FoodBridge! 🎉
