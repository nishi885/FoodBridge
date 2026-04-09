# 🔌 Backend Integration Guide

This guide shows how to integrate the Food Demand Prediction Model with your backend API.

---

## 🎯 Integration Options

Choose one of the following based on your backend framework:

1. **Python-based (Flask/FastAPI)** - Recommended
2. **Node.js/Express** - Via HTTP calls
3. **Direct API calls** - Language-agnostic

---

## 📦 Option 1: Python Flask Integration

### Setup

```bash
# Install Flask
pip install flask
```

### Run API Server

```bash
python src/api_server.py
```

Server runs on `http://localhost:5000`

### Available Endpoints

#### 1. Health Check
```bash
GET /health

Response:
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00",
    "model_loaded": true
}
```

#### 2. Model Info
```bash
GET /info

Response:
{
    "model_type": "Random Forest",
    "features": ["location", "day_of_week", "temperature", ...],
    "timestamp": "2024-01-15T10:30:00"
}
```

#### 3. Single Prediction
```bash
POST /predict
Content-Type: application/json

Request:
{
    "location": "North Area",
    "day_of_week": "Friday",
    "temperature": 15,
    "weather_condition": "Sunny",
    "is_event": 1,
    "holiday": 0
}

Response:
{
    "success": true,
    "prediction": {
        "predicted_meals": 95,
        "confidence_range": [81, 109],
        "location": "North Area",
        "day": "Friday",
        "temperature": 15,
        "weather": "Sunny",
        "is_event": true,
        "is_holiday": false,
        "timestamp": "2024-01-15T10:30:00"
    },
    "timestamp": "2024-01-15T10:30:00"
}
```

#### 4. Batch Predictions
```bash
POST /predict-batch
Content-Type: application/json

Request:
{
    "scenarios": [
        {
            "location": "North Area",
            "day_of_week": "Friday",
            "temperature": 15,
            "weather_condition": "Sunny",
            "is_event": 1,
            "holiday": 0
        },
        {
            "location": "South Area",
            "day_of_week": "Saturday",
            "temperature": 20,
            "weather_condition": "Sunny",
            "is_event": 0,
            "holiday": 0
        }
    ]
}

Response:
{
    "success": true,
    "predictions": [
        {...},
        {...}
    ],
    "count": 2,
    "total_meals": 185,
    "timestamp": "2024-01-15T10:30:00"
}
```

#### 5. Model Statistics
```bash
GET /stats

Response:
{
    "model_type": "Random Forest",
    "n_features": 9,
    "features": ["location", "day_of_week", ...],
    "valid_locations": ["North Area", "South Area", "East Area", "West Area"],
    "valid_days": ["Monday", "Tuesday", ...],
    "valid_weather": ["Sunny", "Rainy", "Cloudy"],
    "temperature_range": [5, 35],
    "timestamp": "2024-01-15T10:30:00"
}
```

### Python Code Example

```python
import requests
import json

API_URL = "http://localhost:5000"

# Single prediction
def predict_demand(location, day, temp, weather, is_event=0, holiday=0):
    response = requests.post(
        f"{API_URL}/predict",
        json={
            "location": location,
            "day_of_week": day,
            "temperature": temp,
            "weather_condition": weather,
            "is_event": is_event,
            "holiday": holiday
        }
    )
    
    if response.status_code == 200:
        return response.json()['prediction']
    else:
        print(f"Error: {response.json()}")
        return None

# Example usage
result = predict_demand(
    location="North Area",
    day="Friday",
    temp=15,
    weather="Sunny",
    is_event=1
)
print(f"Predicted meals: {result['predicted_meals']}")
```

---

## 📦 Option 2: FastAPI Integration

### Setup

```bash
pip install fastapi uvicorn httpx
```

### Create FastAPI App

```python
# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="FoodBridge API")

class PredictionRequest(BaseModel):
    location: str
    day_of_week: str
    temperature: float
    weather_condition: str
    is_event: int = 0
    holiday: int = 0

@app.post("/api/v1/predict")
async def predict(request: PredictionRequest):
    """Get meal demand prediction"""
    response = requests.post(
        "http://localhost:5000/predict",
        json=request.dict()
    )
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, 
                          detail=response.json()['error'])
    
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Run FastAPI Server

```bash
python app.py
# or
uvicorn app:app --reload --port 8000
```

Access at `http://localhost:8000/docs` for interactive API docs.

---

## 📦 Option 3: Node.js/Express Integration

### Setup

```bash
npm install express axios
```

### Create Express Server

```javascript
// server.js
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

const MODEL_API = 'http://localhost:5000';

// Single prediction
app.post('/api/predict', async (req, res) => {
    try {
        const response = await axios.post(
            `${MODEL_API}/predict`,
            req.body
        );
        res.json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).json({
            success: false,
            error: error.message
        });
    }
});

// Batch predictions
app.post('/api/predict-batch', async (req, res) => {
    try {
        const response = await axios.post(
            `${MODEL_API}/predict-batch`,
            req.body
        );
        res.json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).json({
            success: false,
            error: error.message
        });
    }
});

// Get model stats
app.get('/api/model-stats', async (req, res) => {
    try {
        const response = await axios.get(`${MODEL_API}/stats`);
        res.json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).json({
            success: false,
            error: error.message
        });
    }
});

app.listen(3000, () => {
    console.log('🍽️  FoodBridge API running on port 3000');
});
```

### Run Server

```bash
node server.js
```

---

## 🌐 Option 4: REST API Calls (Any Language)

### cURL Examples

```bash
# Health check
curl http://localhost:5000/health

# Get model info
curl http://localhost:5000/info

# Make prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "location": "North Area",
    "day_of_week": "Friday",
    "temperature": 15,
    "weather_condition": "Sunny",
    "is_event": 1,
    "holiday": 0
  }'

# Get stats
curl http://localhost:5000/stats
```

### JavaScript (Fetch API)

```javascript
// Make prediction
async function predictDemand(location, day, temp, weather) {
    const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            location: location,
            day_of_week: day,
            temperature: temp,
            weather_condition: weather,
            is_event: 0,
            holiday: 0
        })
    });
    
    const data = await response.json();
    return data.prediction;
}

// Usage
predictDemand('North Area', 'Friday', 15, 'Sunny')
    .then(pred => console.log(`Meals needed: ${pred.predicted_meals}`))
    .catch(err => console.error(err));
```

### Axios (JavaScript/Node.js)

```javascript
const axios = require('axios');

async function predictDemand(location, day, temp, weather) {
    try {
        const response = await axios.post('http://localhost:5000/predict', {
            location: location,
            day_of_week: day,
            temperature: temp,
            weather_condition: weather,
            is_event: 0,
            holiday: 0
        });
        
        return response.data.prediction;
    } catch (error) {
        console.error('Prediction error:', error);
    }
}
```

---

## 🗄️ Database Integration

Store predictions for analytics:

### Schema Example (SQL)

```sql
CREATE TABLE demand_predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    location VARCHAR(100),
    day_of_week VARCHAR(20),
    temperature FLOAT,
    weather_condition VARCHAR(20),
    is_event INT,
    holiday INT,
    predicted_meals INT,
    actual_meals INT,
    confidence_range_min INT,
    confidence_range_max INT,
    timestamp DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Track accuracy over time
CREATE TABLE prediction_accuracy (
    id INT PRIMARY KEY AUTO_INCREMENT,
    prediction_date DATE,
    location VARCHAR(100),
    avg_predicted INT,
    avg_actual INT,
    accuracy_percentage FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Python Backend Example

```python
from flask import Flask
from datetime import datetime
import SQLAlchemy as db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:pass@localhost/foodbridge'
db = db.SQLAlchemy(app)

class DemandPrediction(db.Model):
    __tablename__ = 'demand_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    day_of_week = db.Column(db.String(20))
    temperature = db.Column(db.Float)
    weather_condition = db.Column(db.String(20))
    is_event = db.Column(db.Integer)
    holiday = db.Column(db.Integer)
    predicted_meals = db.Column(db.Integer)
    actual_meals = db.Column(db.Integer, nullable=True)
    confidence_min = db.Column(db.Integer)
    confidence_max = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.post('/api/predict-and-store')
def predict_and_store():
    # Get prediction
    prediction = predictor.predict(...)
    
    # Store in database
    record = DemandPrediction(
        location=prediction['location'],
        day_of_week=prediction['day'],
        temperature=prediction['temperature'],
        weather_condition=prediction['weather'],
        is_event=prediction['is_event'],
        holiday=prediction['is_holiday'],
        predicted_meals=prediction['predicted_meals'],
        confidence_min=prediction['confidence_range'][0],
        confidence_max=prediction['confidence_range'][1]
    )
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify(prediction)
```

---

## 🔄 Real-time Weather Integration

Integrate with weather API for automatic temperature/weather data:

### Using Open-Meteo (Free API)

```python
import requests
from datetime import datetime

def get_weather(latitude, longitude):
    """Get current weather for a location"""
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,weather_code",
            "timezone": "auto"
        }
    )
    
    data = response.json()['current']
    temperature = data['temperature_2m']
    
    # Map weather code to condition
    weather_code = data['weather_code']
    weather_map = {
        0: "Sunny",
        1: "Cloudy",
        2: "Cloudy",
        45: "Cloudy",
        48: "Cloudy",
        51: "Rainy",
        61: "Rainy",
        80: "Rainy"
    }
    
    weather = weather_map.get(weather_code, "Sunny")
    
    return temperature, weather

# Integrated prediction with auto weather
def predict_with_weather(location, latitude, longitude, day_of_week, is_event=0, holiday=0):
    temperature, weather = get_weather(latitude, longitude)
    
    prediction = predictor.predict(
        location=location,
        day_of_week=day_of_week,
        temperature=temperature,
        weather_condition=weather,
        is_event=is_event,
        holiday=holiday
    )
    
    return prediction
```

---

## 📊 Monitoring & Analytics

Track model performance over time:

```python
@app.post('/api/feedback')
def record_feedback():
    """Record actual demand to track accuracy"""
    data = request.json
    
    # Update record with actual meals
    prediction = DemandPrediction.query.get(data['prediction_id'])
    prediction.actual_meals = data['actual_meals']
    
    # Calculate accuracy
    error = abs(prediction.predicted_meals - data['actual_meals'])
    accuracy = max(0, 100 - (error / data['actual_meals'] * 100))
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'error': error,
        'accuracy': accuracy
    })
```

---

## 🚀 Production Deployment

### Considerations

1. **Model Loading**: Cache model in memory
2. **Performance**: Use async/concurrent requests
3. **Error Handling**: Graceful fallbacks
4. **Monitoring**: Log predictions and accuracy
5. **Scaling**: Run multiple API instances
6. **Security**: Add authentication/rate limiting

### Docker Deployment

```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ src/
COPY models/ models/
COPY data/ data/

EXPOSE 5000

CMD ["python", "src/api_server.py"]
```

Build and run:

```bash
docker build -t foodbridge-api .
docker run -p 5000:5000 foodbridge-api
```

---

## ✅ Integration Checklist

- [ ] Train model: `python src/train_model.py`
- [ ] Test predictions: `python src/predict.py`
- [ ] Review model performance
- [ ] Start API server: `python src/api_server.py`
- [ ] Test API endpoints
- [ ] Integrate with backend
- [ ] Add database storage
- [ ] Add weather API integration
- [ ] Implement feedback mechanism
- [ ] Set up monitoring
- [ ] Deploy to production

---

## 💡 Sample Use Cases

### 1. Daily Planning
```
Each morning, get predictions for next 7 days
Aggregate meals needed across all areas
Plan procurement and distribution
```

### 2. Event Management
```
When event scheduled, set is_event=1
Get updated predictions
Ensure adequate supply
```

### 3. Real-time Adjustments
```
Monitor actual demand vs predicted
Adjust next predictions based on deviation
Learn patterns over time
```

### 4. Resource Optimization
```
Predict for all 4 areas at once
Optimize logistics routes
Reduce transportation costs
```

---

## 📞 Troubleshooting

### API Connection Issues
- Ensure Flask server is running: `python src/api_server.py`
- Check port 5000 is not blocked
- Verify response with: `curl http://localhost:5000/health`

### Prediction Errors
- Validate input field names (case-sensitive)
- Check location is in: North/South/East/West Area
- Verify day_of_week is correct spelling
- Ensure temperature is numeric

### Model Not Loaded
- Train model first: `python src/train_model.py`
- Check models/ directory has `.pkl` files
- Restart API server

---

**Ready to integrate? Start with Option 1 (Flask) for fastest setup!** 🚀
