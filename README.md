<<<<<<< HEAD
# FoodBridge

FoodBridge is a comprehensive platform designed to connect food donors with NGOs and organizations in need, facilitating efficient food distribution and reducing food waste. The platform leverages AI-powered route optimization and demand prediction to ensure timely and effective food delivery.

## Project Overview

FoodBridge consists of three main components:

1. **Frontend**: A React-based web application for user interaction
2. **Backend**: A Node.js server handling API requests and data management
3. **AI Components**: Python-based services for route optimization and demand prediction

## Workflow

### User Authentication
- Users start by accessing the authentication page (`AuthPage.jsx`)
- New users can register, existing users can log in
- Upon successful authentication, users are redirected based on their role:
  - **Donors**: Redirected to `DonorDashboard.jsx`
  - **NGOs**: Redirected to `NGODashboard.jsx`

### Donor Workflow
1. Donors log in and access the Donor Dashboard
2. They can add food donations through the dashboard
3. Food listings are sent to the backend via API calls (`foodController.js`)
4. Donors can view their donation history and manage listings

### NGO Workflow
1. NGOs log in and access the NGO Dashboard
2. They can browse available food donations
3. NGOs can submit food requests for specific items
4. Requests are processed through the backend (`requestController.js`)
5. NGOs can track their requests and view fulfillment status

### Backend Processing
- The Node.js backend (`server.js`) handles all API requests
- Authentication is managed through `authController.js` and `authRoutes.js`
- Food donations and requests are stored in the database (`Food.js`, `Request.js`, `User.js` models)
- All routes are defined in respective route files (`authRoutes.js`, `foodRoutes.js`, `requestRoutes.js`)

### AI Integration
- **Route Optimization**: Uses graph algorithms and mapping services to find optimal delivery routes
- **Demand Prediction**: Machine learning models predict food demand patterns to help with planning
- AI services run as separate Python applications with their own APIs

## Technology Stack

### Frontend
- React (with Vite for development)
- JSX components for UI
- API service layer for backend communication

### Backend
- Node.js with Express.js
- MongoDB for data storage
- JWT for authentication
- Middleware for error handling and authentication

### AI Components
- Python with Flask for API servers
- Machine learning libraries (scikit-learn, pandas, etc.)
- Graph algorithms for route optimization

## Getting Started

1. **Clone the repository**
2. **Install dependencies**:
   - Frontend: `npm install` in the `FoodBridge/frontend` directory
   - Backend: `npm install` in the `FoodBridge/backend` directory
   - AI components: `pip install -r requirements.txt` in respective AI directories
3. **Set up environment variables** (database connection, API keys, etc.)
4. **Start the services**:
   - Backend: `npm start` in backend directory
   - Frontend: `npm run dev` in frontend directory
   - AI services: Run respective Python servers
5. **Access the application** at `http://localhost:3000` (or configured port)

## API Endpoints

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/food` - Get available food donations
- `POST /api/food` - Add new food donation
- `GET /api/requests` - Get food requests
- `POST /api/requests` - Submit food request

## Contributing

Please read the contributing guidelines before making changes. Ensure all tests pass and follow the established code style.

## License

This project is licensed under the MIT License.
=======
# FoodBridge
>>>>>>> 62b717ced6f9fae12f9082ad1704270265bdf161
