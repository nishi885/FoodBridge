"""
Prediction Utility for Food Demand Model
Use trained model to make predictions for new locations and conditions
"""

import os
from datetime import datetime

import joblib
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MODEL_DIR = os.path.join(BASE_DIR, "models")


class DemandPredictor:
    """
    Make predictions using trained demand prediction model
    """

    def __init__(self, model_path=DEFAULT_MODEL_DIR):
        """
        Load the trained model and encoders

        Args:
            model_path: Path to the models directory
        """
        self.model_path = os.path.abspath(model_path)
        self.model = None
        self.model_type = None
        self.model_metadata = {}
        self.encoders = None
        self.feature_names = None

        self._load_artifacts()

    def _load_artifacts(self):
        """Load model and encoders."""
        try:
            metadata_file = os.path.join(self.model_path, "model_metadata.pkl")
            if os.path.exists(metadata_file):
                self.model_metadata = joblib.load(metadata_file)

            preferred_model = self.model_metadata.get("model_file")
            candidate_files = [preferred_model] if preferred_model else []
            candidate_files.extend(["random_forest_model.pkl", "linear_regression_model.pkl"])

            model_file = None
            for candidate in candidate_files:
                if not candidate:
                    continue
                path = os.path.join(self.model_path, candidate)
                if os.path.exists(path):
                    model_file = path
                    break

            if not model_file:
                raise FileNotFoundError("No trained model found")

            self.model = joblib.load(model_file)
            self.model_type = self.model_metadata.get(
                "model_name",
                "Random Forest" if "random_forest" in os.path.basename(model_file) else "Linear Regression",
            )

            encoders_file = os.path.join(self.model_path, "feature_encoders.pkl")
            self.encoders = joblib.load(encoders_file)

            features_file = os.path.join(self.model_path, "feature_names.pkl")
            self.feature_names = joblib.load(features_file)

            print("Model loaded successfully")
            print(f"  Model: {self.model_type}")
            print(f"  Features: {len(self.feature_names)}")

        except Exception as exc:
            print(f"Error loading model: {exc}")
            print("Make sure you've trained the model first using train_model.py")
            raise

    def _validate_categorical_value(self, field_name, value):
        encoder = self.encoders[field_name]
        valid_values = set(encoder.classes_)
        if value not in valid_values:
            allowed = ", ".join(sorted(valid_values))
            raise ValueError(f"Invalid {field_name}: {value}. Allowed values: {allowed}")

    def predict(self, location, day_of_week, temperature, weather_condition, is_event=0, holiday=0):
        """
        Make a prediction for a specific scenario.
        """
        try:
            temperature = float(temperature)
            is_event = int(is_event)
            holiday = int(holiday)

            self._validate_categorical_value("location", location)
            self._validate_categorical_value("day_of_week", day_of_week)
            self._validate_categorical_value("weather_condition", weather_condition)

            input_data = pd.DataFrame(
                {
                    "location": [location],
                    "day_of_week": [day_of_week],
                    "temperature": [temperature],
                    "weather_condition": [weather_condition],
                    "is_event": [is_event],
                    "holiday": [holiday],
                }
            )

            for col in ["location", "day_of_week", "weather_condition"]:
                input_data[col] = self.encoders[col].transform(input_data[col])

            input_data["is_weekend"] = 1 if day_of_week in ["Saturday", "Sunday"] else 0
            input_data["is_cold"] = 1 if temperature < 12 else 0
            input_data["is_hot"] = 1 if temperature > 18 else 0
            input_data = input_data[self.feature_names]

            prediction = max(0, float(self.model.predict(input_data)[0]))

            return {
                "predicted_meals": int(round(prediction)),
                "confidence_range": (
                    int(round(prediction * 0.85)),
                    int(round(prediction * 1.15)),
                ),
                "model_type": self.model_type,
                "location": location,
                "day": day_of_week,
                "temperature": temperature,
                "weather": weather_condition,
                "is_event": bool(is_event),
                "is_holiday": bool(holiday),
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as exc:
            print(f"Error making prediction: {exc}")
            raise

    def predict_batch(self, scenarios):
        """Make predictions for multiple scenarios."""
        predictions = []
        for scenario in scenarios:
            predictions.append(self.predict(**scenario))
        return predictions

    def predict_from_dataframe(self, df):
        """Make predictions from a DataFrame."""
        df_copy = df.copy()
        predictions = []

        for _, row in df.iterrows():
            pred = self.predict(
                location=row["location"],
                day_of_week=row["day_of_week"],
                temperature=row["temperature"],
                weather_condition=row["weather_condition"],
                is_event=row.get("is_event", 0),
                holiday=row.get("holiday", 0),
            )
            predictions.append(pred["predicted_meals"])

        df_copy["predicted_meals"] = predictions
        return df_copy


if __name__ == "__main__":
    print("FoodBridge - Demand Prediction")
    print("=" * 50)

    try:
        predictor = DemandPredictor()

        print("\nExample 1: Single Location Prediction")
        print("-" * 50)
        result = predictor.predict(
            location="North Area",
            day_of_week="Friday",
            temperature=15,
            weather_condition="Sunny",
            is_event=1,
            holiday=0,
        )

        print(f"Location: {result['location']}")
        print(f"Day: {result['day']}")
        print(f"Temperature: {result['temperature']} C")
        print(f"Weather: {result['weather']}")
        print(f"Event: {'Yes' if result['is_event'] else 'No'}")
        print(f"\nPredicted Meals: {result['predicted_meals']}")
        print(
            f"Confidence Range: {result['confidence_range'][0]}-"
            f"{result['confidence_range'][1]} meals"
        )

        print("\n\nExample 2: Multiple Area Predictions (Sunday)")
        print("-" * 50)
        scenarios = [
            {
                "location": "North Area",
                "day_of_week": "Sunday",
                "temperature": 20,
                "weather_condition": "Sunny",
                "is_event": 0,
                "holiday": 0,
            },
            {
                "location": "South Area",
                "day_of_week": "Sunday",
                "temperature": 22,
                "weather_condition": "Sunny",
                "is_event": 1,
                "holiday": 0,
            },
            {
                "location": "East Area",
                "day_of_week": "Sunday",
                "temperature": 18,
                "weather_condition": "Cloudy",
                "is_event": 0,
                "holiday": 0,
            },
            {
                "location": "West Area",
                "day_of_week": "Sunday",
                "temperature": 19,
                "weather_condition": "Sunny",
                "is_event": 1,
                "holiday": 1,
            },
        ]

        predictions = predictor.predict_batch(scenarios)

        for pred in predictions:
            print(
                f"\n{pred['location']:12} | Day: {pred['day']:10} | Weather: {pred['weather']:8} | "
                f"Event: {'Yes' if pred['is_event'] else 'No ':3} | {pred['predicted_meals']} meals"
            )

        print("\n\nPrediction Summary")
        print("-" * 50)
        all_predictions = [p["predicted_meals"] for p in predictions]
        print(f"Total meals needed (all areas): {sum(all_predictions)} meals")
        print(f"Average per area: {np.mean(all_predictions):.1f} meals")
        print(f"Range: {min(all_predictions)}-{max(all_predictions)} meals")

    except Exception as exc:
        print(f"Error: {exc}")
        print("\nMake sure you've trained the model first")
        print("Run: python src/train_model.py")
