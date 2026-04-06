"""
Prediction Utility for Food Demand Model
Use trained model to make predictions for new locations and conditions
"""

import joblib
import pandas as pd
import numpy as np
import os
from datetime import datetime


class DemandPredictor:
    """
    Make predictions using trained demand prediction model
    """
    
    def __init__(self, model_path='models'):
        """
        Load the trained model and encoders
        
        Args:
            model_path: Path to the models directory
        """
        self.model_path = model_path
        self.model = None
        self.encoders = None
        self.feature_names = None
        
        self._load_artifacts()
        
    def _load_artifacts(self):
        """Load model and encoders"""
        try:
            # Try to load Random Forest first
            model_file = os.path.join(self.model_path, 'random_forest_model.pkl')
            if os.path.exists(model_file):
                self.model = joblib.load(model_file)
                self.model_type = 'Random Forest'
            else:
                # Fall back to Linear Regression
                model_file = os.path.join(self.model_path, 'linear_regression_model.pkl')
                if os.path.exists(model_file):
                    self.model = joblib.load(model_file)
                    self.model_type = 'Linear Regression'
                else:
                    raise FileNotFoundError("No trained model found")
            
            # Load encoders
            encoders_file = os.path.join(self.model_path, 'feature_encoders.pkl')
            self.encoders = joblib.load(encoders_file)
            
            # Load feature names
            features_file = os.path.join(self.model_path, 'feature_names.pkl')
            self.feature_names = joblib.load(features_file)
            
            print("✅ Model loaded successfully!")
            print(f"   Model: {self.model_type}")
            print(f"   Features: {len(self.feature_names)}")
            
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            print(f"   Make sure you've trained the model first using train_model.py")
            raise
    
    def predict(self, location, day_of_week, temperature, weather_condition, 
                is_event=0, holiday=0):
        """
        Make a prediction for a specific scenario
        
        Args:
            location (str): Area location (North/South/East/West Area)
            day_of_week (str): Day of week (Monday-Sunday)
            temperature (float): Temperature in Celsius
            weather_condition (str): Weather (Sunny/Rainy/Cloudy)
            is_event (int): 1 if event/festival, 0 otherwise
            holiday (int): 1 if holiday, 0 otherwise
            
        Returns:
            dict: Prediction with confidence and explanation
        """
        try:
            # Create input dataframe
            input_data = pd.DataFrame({
                'location': [location],
                'day_of_week': [day_of_week],
                'temperature': [temperature],
                'weather_condition': [weather_condition],
                'is_event': [is_event],
                'holiday': [holiday]
            })
            
            # Encode categorical features
            for col in ['location', 'day_of_week', 'weather_condition']:
                input_data[col] = self.encoders[col].transform(input_data[col])
            
            # Add engineered features
            is_weekend = 1 if day_of_week in ['Saturday', 'Sunday'] else 0
            is_cold = 1 if temperature < 12 else 0
            is_hot = 1 if temperature > 18 else 0
            
            input_data['is_weekend'] = is_weekend
            input_data['is_cold'] = is_cold
            input_data['is_hot'] = is_hot
            
            # Ensure features are in the same order as training
            input_data = input_data[self.feature_names]
            
            # Make prediction
            prediction = self.model.predict(input_data)[0]
            prediction = max(0, prediction)  # Ensure non-negative
            
            return {
                'predicted_meals': int(round(prediction)),
                'confidence_range': (int(round(prediction * 0.85)), int(round(prediction * 1.15))),
                'location': location,
                'day': day_of_week,
                'temperature': temperature,
                'weather': weather_condition,
                'is_event': bool(is_event),
                'is_holiday': bool(holiday),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error making prediction: {str(e)}")
            raise
    
    def predict_batch(self, scenarios):
        """
        Make predictions for multiple scenarios
        
        Args:
            scenarios (list): List of dicts with prediction parameters
            
        Returns:
            list: List of predictions
        """
        predictions = []
        for scenario in scenarios:
            pred = self.predict(**scenario)
            predictions.append(pred)
        return predictions
    
    def predict_from_dataframe(self, df):
        """
        Make predictions from a DataFrame
        
        Args:
            df (pd.DataFrame): DataFrame with columns: location, day_of_week, temperature, 
                             weather_condition, is_event, holiday
                             
        Returns:
            pd.DataFrame: Original data with 'predicted_meals' column added
        """
        df_copy = df.copy()
        predictions = []
        
        for idx, row in df.iterrows():
            pred = self.predict(
                location=row['location'],
                day_of_week=row['day_of_week'],
                temperature=row['temperature'],
                weather_condition=row['weather_condition'],
                is_event=row.get('is_event', 0),
                holiday=row.get('holiday', 0)
            )
            predictions.append(pred['predicted_meals'])
        
        df_copy['predicted_meals'] = predictions
        return df_copy


# Example usage
if __name__ == "__main__":
    print("🍽️  FoodBridge - Demand Prediction")
    print("="*50)
    
    try:
        # Initialize predictor
        predictor = DemandPredictor()
        
        # Example 1: Single prediction
        print("\n📍 Example 1: Single Location Prediction")
        print("-" * 50)
        result = predictor.predict(
            location='North Area',
            day_of_week='Friday',
            temperature=15,
            weather_condition='Sunny',
            is_event=1,
            holiday=0
        )
        
        print(f"Location: {result['location']}")
        print(f"Day: {result['day']}")
        print(f"Temperature: {result['temperature']}°C")
        print(f"Weather: {result['weather']}")
        print(f"Event: {'Yes' if result['is_event'] else 'No'}")
        print(f"\n🎯 Predicted Meals: {result['predicted_meals']}")
        print(f"📊 Confidence Range: {result['confidence_range'][0]}-{result['confidence_range'][1]} meals")
        
        # Example 2: Multiple predictions
        print("\n\n📍 Example 2: Multiple Area Predictions (Sunday)")
        print("-" * 50)
        scenarios = [
            {
                'location': 'North Area',
                'day_of_week': 'Sunday',
                'temperature': 20,
                'weather_condition': 'Sunny',
                'is_event': 0,
                'holiday': 0
            },
            {
                'location': 'South Area',
                'day_of_week': 'Sunday',
                'temperature': 22,
                'weather_condition': 'Sunny',
                'is_event': 1,
                'holiday': 0
            },
            {
                'location': 'East Area',
                'day_of_week': 'Sunday',
                'temperature': 18,
                'weather_condition': 'Cloudy',
                'is_event': 0,
                'holiday': 0
            },
            {
                'location': 'West Area',
                'day_of_week': 'Sunday',
                'temperature': 19,
                'weather_condition': 'Sunny',
                'is_event': 1,
                'holiday': 1
            }
        ]
        
        predictions = predictor.predict_batch(scenarios)
        
        for pred in predictions:
            print(f"\n{pred['location']:12} | Day: {pred['day']:10} | Weather: {pred['weather']:8} | "
                  f"Event: {'Yes' if pred['is_event'] else 'No ':3} | "
                  f"🎯 {pred['predicted_meals']} meals")
        
        # Example 3: Summary statistics
        print("\n\n📊 Prediction Summary")
        print("-" * 50)
        all_predictions = [p['predicted_meals'] for p in predictions]
        print(f"Total meals needed (all areas): {sum(all_predictions)} meals")
        print(f"Average per area: {np.mean(all_predictions):.1f} meals")
        print(f"Range: {min(all_predictions)}-{max(all_predictions)} meals")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Make sure you've trained the model first!")
        print("   Run: python src/train_model.py")
