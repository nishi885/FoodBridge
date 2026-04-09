"""
Simple HTTP API for Demand Prediction Model
Can be integrated with Flask, FastAPI, or any backend framework
"""

from datetime import datetime
import traceback

from flask import Flask, jsonify, request

from predict import DemandPredictor

app = Flask(__name__)

try:
    predictor = DemandPredictor()
    MODEL_LOADED = True
except Exception as exc:
    print(f"Warning: Could not load model: {exc}")
    predictor = None
    MODEL_LOADED = False


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "model_loaded": MODEL_LOADED,
        }
    )


@app.route("/info", methods=["GET"])
def info():
    """Get model information."""
    if not MODEL_LOADED:
        return jsonify({"error": "Model not loaded"}), 500

    return jsonify(
        {
            "model_type": predictor.model_type,
            "features": predictor.feature_names,
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/predict", methods=["POST"])
def predict():
    """Make a single prediction."""
    if not MODEL_LOADED:
        return jsonify({"error": "Model not loaded. Run training first.", "success": False}), 500

    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Request body must be valid JSON", "success": False}), 400

        required_fields = ["location", "day_of_week", "temperature", "weather_condition"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}", "success": False}), 400

        result = predictor.predict(
            location=data["location"],
            day_of_week=data["day_of_week"],
            temperature=data["temperature"],
            weather_condition=data["weather_condition"],
            is_event=data.get("is_event", 0),
            holiday=data.get("holiday", 0),
        )

        return jsonify(
            {
                "success": True,
                "prediction": result,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except ValueError as exc:
        return jsonify({"error": f"Invalid input: {exc}", "success": False}), 400
    except Exception as exc:
        return jsonify(
            {
                "error": f"Prediction error: {exc}",
                "success": False,
                "traceback": traceback.format_exc(),
            }
        ), 500


@app.route("/predict-batch", methods=["POST"])
def predict_batch():
    """Make multiple predictions at once."""
    if not MODEL_LOADED:
        return jsonify({"error": "Model not loaded. Run training first.", "success": False}), 500

    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Request body must be valid JSON", "success": False}), 400

        scenarios = data.get("scenarios", [])
        if not isinstance(scenarios, list) or not scenarios:
            return jsonify({"error": "No scenarios provided", "success": False}), 400

        predictions = predictor.predict_batch(scenarios)
        return jsonify(
            {
                "success": True,
                "predictions": predictions,
                "count": len(predictions),
                "total_meals": sum(p["predicted_meals"] for p in predictions),
                "timestamp": datetime.now().isoformat(),
            }
        )

    except ValueError as exc:
        return jsonify({"error": f"Invalid input: {exc}", "success": False}), 400
    except Exception as exc:
        return jsonify(
            {
                "error": f"Batch prediction error: {exc}",
                "success": False,
                "traceback": traceback.format_exc(),
            }
        ), 500


@app.route("/stats", methods=["GET"])
def stats():
    """Get model statistics."""
    if not MODEL_LOADED:
        return jsonify({"error": "Model not loaded"}), 500

    valid_values = {
        field: sorted(list(encoder.classes_))
        for field, encoder in predictor.encoders.items()
    }
    return jsonify(
        {
            "model_type": predictor.model_type,
            "n_features": len(predictor.feature_names),
            "features": predictor.feature_names,
            "valid_locations": valid_values.get("location", []),
            "valid_days": valid_values.get("day_of_week", []),
            "valid_weather": valid_values.get("weather_condition", []),
            "temperature_range": [5, 35],
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify(
        {
            "error": "Endpoint not found",
            "available_endpoints": [
                "/health - Health check",
                "/info - Model information",
                "/stats - Model statistics",
                "/predict - Make single prediction (POST)",
                "/predict-batch - Make batch predictions (POST)",
            ],
        }
    ), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error", "message": str(error)}), 500


if __name__ == "__main__":
    print("FoodBridge API Server")
    print("=" * 50)

    if MODEL_LOADED:
        print(f"Model loaded: {predictor.model_type}")
        print(f"Features: {len(predictor.feature_names)}")
    else:
        print("Model not loaded. Train the model first:")
        print("python src/train_model.py")

    print("\nStarting server on http://localhost:5000")
    print("=" * 50)

    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
