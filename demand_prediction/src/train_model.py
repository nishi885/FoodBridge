"""
Food Demand Prediction Model
Predicts how many meals NGOs need based on location, weather, events, and day of week
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class DemandPredictionModel:
    """
    Demand Prediction Model for Food NGOs
    
    Features:
    - Location (North, South, East, West Area)
    - Day of Week (Monday-Sunday)
    - Temperature
    - Weather Condition (Sunny, Rainy, Cloudy)
    - Is Event/Festival (1/0)
    - Holiday (1/0)
    
    Target: meals_needed
    """
    
    def __init__(self):
        self.lr_model = None
        self.rf_model = None
        self.feature_encoders = {}
        self.best_model = None
        self.model_name = None
        self.train_data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None
        
    def load_data(self, filepath):
        """Load training data from CSV"""
        print(f"📂 Loading data from {filepath}...")
        self.train_data = pd.read_csv(filepath)
        print(f"✅ Data loaded: {self.train_data.shape[0]} records, {self.train_data.shape[1]} features")
        print(f"\nDataset info:\n{self.train_data.head()}")
        return self.train_data
        
    def preprocess_data(self):
        """Preprocess and engineer features"""
        print("\n🔧 Preprocessing data...")
        
        df = self.train_data.copy()
        
        # Encode categorical variables
        categorical_features = ['location', 'day_of_week', 'weather_condition']
        
        for feature in categorical_features:
            le = LabelEncoder()
            df[feature] = le.fit_transform(df[feature])
            self.feature_encoders[feature] = le
            print(f"  → Encoded {feature}: {dict(zip(le.classes_, le.transform(le.classes_)))}")
        
        # Feature engineering
        # Create is_weekend feature
        day_of_week_mapping = {
            'Monday': 0, 'Tuesday': 1, 'Wednesday': 2,
            'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6
        }
        df['is_weekend'] = self.train_data['day_of_week'].map(
            lambda x: 1 if x in ['Saturday', 'Sunday'] else 0
        )
        
        # Create temperature categories
        df['is_cold'] = (df['temperature'] < 12).astype(int)
        df['is_hot'] = (df['temperature'] > 18).astype(int)
        
        # Separate features and target
        feature_columns = [col for col in df.columns if col != 'meals_needed' and col != 'date']
        X = df[feature_columns]
        y = df['meals_needed']
        
        self.feature_names = feature_columns
        
        print(f"✅ Features created: {len(feature_columns)} features")
        print(f"   Features: {feature_columns}")
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"✅ Data split: {len(self.X_train)} train, {len(self.X_test)} test")
        return self.X_train, self.X_test, self.y_train, self.y_test
        
    def train_linear_regression(self):
        """Train Linear Regression model"""
        print("\n🚀 Training Linear Regression model...")
        
        self.lr_model = LinearRegression()
        self.lr_model.fit(self.X_train, self.y_train)
        
        # Predictions
        y_pred_train = self.lr_model.predict(self.X_train)
        y_pred_test = self.lr_model.predict(self.X_test)
        
        # Metrics
        lr_train_r2 = r2_score(self.y_train, y_pred_train)
        lr_test_r2 = r2_score(self.y_test, y_pred_test)
        lr_train_rmse = np.sqrt(mean_squared_error(self.y_train, y_pred_train))
        lr_test_rmse = np.sqrt(mean_squared_error(self.y_test, y_pred_test))
        lr_test_mae = mean_absolute_error(self.y_test, y_pred_test)
        
        print(f"✅ Linear Regression trained:")
        print(f"   Train R² Score: {lr_train_r2:.4f}")
        print(f"   Test R² Score: {lr_test_r2:.4f}")
        print(f"   Test RMSE: {lr_test_rmse:.2f} meals")
        print(f"   Test MAE: {lr_test_mae:.2f} meals")
        
        # Feature importance (coefficients)
        print(f"\n   Feature Coefficients:")
        for name, coef in sorted(zip(self.feature_names, self.lr_model.coef_), 
                                key=lambda x: abs(x[1]), reverse=True):
            print(f"     - {name}: {coef:.4f}")
        
        return {
            'model': self.lr_model,
            'train_r2': lr_train_r2,
            'test_r2': lr_test_r2,
            'test_rmse': lr_test_rmse,
            'test_mae': lr_test_mae,
            'y_pred': y_pred_test
        }
        
    def train_random_forest(self):
        """Train Random Forest model"""
        print("\n🚀 Training Random Forest model...")
        
        self.rf_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.rf_model.fit(self.X_train, self.y_train)
        
        # Predictions
        y_pred_train = self.rf_model.predict(self.X_train)
        y_pred_test = self.rf_model.predict(self.X_test)
        
        # Metrics
        rf_train_r2 = r2_score(self.y_train, y_pred_train)
        rf_test_r2 = r2_score(self.y_test, y_pred_test)
        rf_train_rmse = np.sqrt(mean_squared_error(self.y_train, y_pred_train))
        rf_test_rmse = np.sqrt(mean_squared_error(self.y_test, y_pred_test))
        rf_test_mae = mean_absolute_error(self.y_test, y_pred_test)
        
        print(f"✅ Random Forest trained:")
        print(f"   Train R² Score: {rf_train_r2:.4f}")
        print(f"   Test R² Score: {rf_test_r2:.4f}")
        print(f"   Test RMSE: {rf_test_rmse:.2f} meals")
        print(f"   Test MAE: {rf_test_mae:.2f} meals")
        
        # Feature importance
        print(f"\n   Top 5 Important Features:")
        importances = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        for idx, row in importances.head(5).iterrows():
            print(f"     - {row['feature']}: {row['importance']:.4f}")
        
        return {
            'model': self.rf_model,
            'train_r2': rf_train_r2,
            'test_r2': rf_test_r2,
            'test_rmse': rf_test_rmse,
            'test_mae': rf_test_mae,
            'y_pred': y_pred_test
        }
        
    def select_best_model(self, lr_metrics, rf_metrics):
        """Select best model based on test R² score"""
        print("\n🏆 Model Comparison:")
        print("=" * 50)
        print(f"{'Metric':<20} {'Linear Regression':<20} {'Random Forest':<20}")
        print("=" * 50)
        print(f"{'Test R² Score':<20} {lr_metrics['test_r2']:<20.4f} {rf_metrics['test_r2']:<20.4f}")
        print(f"{'Test RMSE':<20} {lr_metrics['test_rmse']:<20.2f} {rf_metrics['test_rmse']:<20.2f}")
        print(f"{'Test MAE':<20} {lr_metrics['test_mae']:<20.2f} {rf_metrics['test_mae']:<20.2f}")
        print("=" * 50)
        
        if rf_metrics['test_r2'] > lr_metrics['test_r2']:
            self.best_model = self.rf_model
            self.model_name = 'Random Forest'
            best_metrics = rf_metrics
            print(f"\n✅ Selected Model: Random Forest 🎯")
        else:
            self.best_model = self.lr_model
            self.model_name = 'Linear Regression'
            best_metrics = lr_metrics
            print(f"\n✅ Selected Model: Linear Regression 🎯")
            
        return best_metrics
        
    def save_model(self, model_path='models'):
        """Save the best model and encoders"""
        print(f"\n💾 Saving model...")
        os.makedirs(model_path, exist_ok=True)
        
        # Save model
        model_file = os.path.join(model_path, f'{self.model_name.lower().replace(" ", "_")}_model.pkl')
        joblib.dump(self.best_model, model_file)
        print(f"   ✅ Model saved: {model_file}")
        
        # Save encoders
        encoders_file = os.path.join(model_path, 'feature_encoders.pkl')
        joblib.dump(self.feature_encoders, encoders_file)
        print(f"   ✅ Encoders saved: {encoders_file}")
        
        # Save feature names
        features_file = os.path.join(model_path, 'feature_names.pkl')
        joblib.dump(self.feature_names, features_file)
        print(f"   ✅ Feature names saved: {features_file}")
        
        print(f"\n✨ Model ready for deployment!")
        
    def visualize_results(self, lr_metrics, rf_metrics):
        """Create visualizations of model performance"""
        print("\n📊 Creating visualizations...")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Food Demand Prediction - Model Performance', fontsize=16, fontweight='bold')
        
        # 1. Actual vs Predicted (Random Forest)
        ax1 = axes[0, 0]
        ax1.scatter(self.y_test, rf_metrics['y_pred'], alpha=0.6, s=80)
        ax1.plot([self.y_test.min(), self.y_test.max()], 
                [self.y_test.min(), self.y_test.max()], 
                'r--', lw=2)
        ax1.set_xlabel('Actual Meals Needed', fontsize=11)
        ax1.set_ylabel('Predicted Meals', fontsize=11)
        ax1.set_title('Random Forest: Actual vs Predicted', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # 2. Model comparison - R² Scores
        ax2 = axes[0, 1]
        models = ['Linear\nRegression', 'Random\nForest']
        r2_scores = [lr_metrics['test_r2'], rf_metrics['test_r2']]
        colors = ['#FF6B6B', '#4ECDC4']
        bars = ax2.bar(models, r2_scores, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        ax2.set_ylabel('R² Score', fontsize=11)
        ax2.set_title('Model Comparison - R² Score', fontweight='bold')
        ax2.set_ylim(0, 1)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, score in zip(bars, r2_scores):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{score:.4f}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Model comparison - RMSE
        ax3 = axes[1, 0]
        rmse_scores = [lr_metrics['test_rmse'], rf_metrics['test_rmse']]
        bars = ax3.bar(models, rmse_scores, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        ax3.set_ylabel('RMSE (meals)', fontsize=11)
        ax3.set_title('Model Comparison - RMSE', fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, score in zip(bars, rmse_scores):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{score:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Residuals plot
        ax4 = axes[1, 1]
        residuals = self.y_test - rf_metrics['y_pred']
        ax4.scatter(rf_metrics['y_pred'], residuals, alpha=0.6, s=80)
        ax4.axhline(y=0, color='r', linestyle='--', lw=2)
        ax4.set_xlabel('Predicted Values', fontsize=11)
        ax4.set_ylabel('Residuals', fontsize=11)
        ax4.set_title('Random Forest - Residual Plot', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('models/model_performance.png', dpi=300, bbox_inches='tight')
        print("   ✅ Performance plot saved: models/model_performance.png")
        
    def train_and_evaluate(self, data_path):
        """Complete training pipeline"""
        print("\n" + "="*60)
        print("🍽️  FOODBRIDGE - DEMAND PREDICTION MODEL")
        print("="*60)
        
        # Load and preprocess
        self.load_data(data_path)
        self.preprocess_data()
        
        # Train models
        lr_metrics = self.train_linear_regression()
        rf_metrics = self.train_random_forest()
        
        # Select and save
        best_metrics = self.select_best_model(lr_metrics, rf_metrics)
        self.save_model()
        
        # Visualize
        self.visualize_results(lr_metrics, rf_metrics)
        
        print("\n" + "="*60)
        print("✅ MODEL TRAINING COMPLETE!")
        print("="*60)
        
        return {
            'best_model': self.best_model,
            'model_name': self.model_name,
            'metrics': best_metrics
        }


if __name__ == "__main__":
    # Initialize and train
    model = DemandPredictionModel()
    
    # Check if data exists
    data_path = 'data/training_data.csv'
    if not os.path.exists(data_path):
        print(f"❌ Data file not found at {data_path}")
        print(f"📂 Please ensure training_data.csv is in the data/ directory")
    else:
        result = model.train_and_evaluate(data_path)
