"""
Simple HTTP API for Demand Prediction Model
Can be integrated with Flask, FastAPI, or any backend framework

Usage:
    python src/api_server.py

Then make requests to:
    POST http://localhost:5000/predict
    
Example request:
{
    "location": "North Area",
    "day_of_week": "Friday",
    "temperature": 15,
    "weather_condition": "Sunny",
    "is_event": 1,
    "holiday": 0
}
"""

from flask import Flask, request, jsonify
import json
from predict import DemandPredictor
from datetime import datetime
import traceback

# Initialize Flask app
app = Flask(__name__)

# Initialize predictor globally
try:
    predictor = DemandPredictor()
    MODEL_LOADED = True
except Exception as e:
    print(f"Warning: Could not load model: {str(e)}")
    predictor = None
    MODEL_LOADED = False


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': MODEL_LOADED
    })


@app.route('/info', methods=['GET'])
def info():
    """Get model information"""
    if not MODEL_LOADED:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'model_type': predictor.model_type,
        'features': predictor.feature_names,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Make a single prediction
    
    Request body:
    {
        "location": "North Area",
        "day_of_week": "Friday",
        "temperature": 15,
        "weather_condition": "Sunny",
        "is_event": 1,
        "holiday": 0
    }
    """
    if not MODEL_LOADED:
        return jsonify({
            'error': 'Model not loaded. Run training first.',
            'success': False
        }), 500
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['location', 'day_of_week', 'temperature', 'weather_condition']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'success': False
                }), 400
        
        # Extract parameters
        location = data['location']
        day_of_week = data['day_of_week']
        temperature = float(data['temperature'])
        weather_condition = data['weather_condition']
        is_event = int(data.get('is_event', 0))
        holiday = int(data.get('holiday', 0))
        
        # Make prediction
        result = predictor.predict(
            location=location,
            day_of_week=day_of_week,
            temperature=temperature,
            weather_condition=weather_condition,
            is_event=is_event,
            holiday=holiday
        )
        
        return jsonify({
            'success': True,
            'prediction': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except ValueError as e:
        return jsonify({
            'error': f'Invalid input: {str(e)}',
            'success': False
        }), 400
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}',
            'success': False,
            'traceback': traceback.format_exc()
        }), 500


@app.route('/predict-batch', methods=['POST'])
def predict_batch():
    """
    Make multiple predictions at once
    
    Request body:
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
            ...
        ]
    }
    """
    if not MODEL_LOADED:
        return jsonify({
            'error': 'Model not loaded. Run training first.',
            'success': False
        }), 500
    
    try:
        data = request.get_json()
        scenarios = data.get('scenarios', [])
        
        if not scenarios:
            return jsonify({
                'error': 'No scenarios provided',
                'success': False
            }), 400
        
        predictions = predictor.predict_batch(scenarios)
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'count': len(predictions),
            'total_meals': sum(p['predicted_meals'] for p in predictions),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Batch prediction error: {str(e)}',
            'success': False,
            'traceback': traceback.format_exc()
        }), 500


@app.route('/stats', methods=['GET'])
def stats():
    """Get model statistics"""
    if not MODEL_LOADED:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'model_type': predictor.model_type,
        'n_features': len(predictor.feature_names),
        'features': predictor.feature_names,
        'valid_locations': ['North Area', 'South Area', 'East Area', 'West Area'],
        'valid_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'valid_weather': ['Sunny', 'Rainy', 'Cloudy'],
        'temperature_range': (5, 35),  # Celsius
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            '/health - Health check',
            '/info - Model information',
            '/stats - Model statistics',
            '/predict - Make single prediction (POST)',
            '/predict-batch - Make batch predictions (POST)'
        ]
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': str(error)
    }), 500


if __name__ == '__main__':
    print(f"🍽️  FoodBridge API Server")
    print(f"{'='*50}")
    
    if MODEL_LOADED:
        print(f"✅ Model loaded: {predictor.model_type}")
        print(f"📊 Features: {len(predictor.feature_names)}")
    else:
        print(f"❌ Model not loaded! Train the model first:")
        print(f"   python src/train_model.py")
    
    print(f"\n🚀 Starting server on http://localhost:5000")
    print(f"{'='*50}")
    
    # Run Flask app
    # Note: Set debug=False for production
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
