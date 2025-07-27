# predict_live.py

import pandas as pd
import numpy as np
import pickle
from datetime import timedelta

# --- Configuration ---
MODEL_ARTIFACT_FILE = 'ensemble_crowd_model.pkl'
# In a real application, this would come from a live database. Here, we use the CSV as our "database" of past events.
HISTORICAL_DATA_SOURCE = 'full_training_data.csv' 

# ==============================================================================
# NOTE: These two functions are copied EXACTLY from the training script.
# The prediction logic must be identical to the training logic.
# ==============================================================================

def predict_with_uncertainty(models, X):
    """Make predictions with uncertainty estimation."""
    predictions = np.array([model.predict(X) for model in models])
    mean_pred = predictions.mean(axis=0)
    std_pred = predictions.std(axis=0)
    return mean_pred, std_pred

def predict_density_at_horizon_improved(models, start_zone, start_timestamp, full_history_df, forecast_horizon_seconds, zone_features, zone_categories):
    """Improved prediction with uncertainty and drift correction."""
    MAX_FORECAST_HORIZON = 600
    if forecast_horizon_seconds > MAX_FORECAST_HORIZON:
        raise ValueError(f"Forecast horizon of {forecast_horizon_seconds}s is too large. Maximum allowed is {MAX_FORECAST_HORIZON}s.")
    
    num_steps = int(forecast_horizon_seconds / 10)
    
    history = full_history_df[
        (full_history_df['zone_name'] == start_zone) & 
        (full_history_df['timestamp'] <= start_timestamp)
    ].copy()
    
    if len(history) < 10:
        raise ValueError(f"Not enough historical data for zone '{start_zone}'")
    
    recent_densities = history['density'].tail(10).values
    trend = np.polyfit(range(len(recent_densities)), recent_densities, 1)[0]
    
    zone_feat = zone_features[zone_features['zone_name'] == start_zone].iloc[0]
    
    predicted_densities = []
    uncertainties = []
    
    for i in range(num_steps):
        last_point = history.iloc[-1]
        prediction_timestamp = last_point['timestamp'] + timedelta(seconds=10)
        
        features = pd.DataFrame(index=[0])
        
        features['x_coord'] = zone_feat['x_coord']
        features['y_coord'] = zone_feat['y_coord']
        features['hour'] = prediction_timestamp.hour
        features['minute'] = prediction_timestamp.minute
        features['second'] = prediction_timestamp.second
        features['day_of_week'] = prediction_timestamp.dayofweek
        
        features['distance_from_center'] = zone_feat['distance_from_center']
        features['is_corner'] = zone_feat['is_corner']
        features['is_edge'] = zone_feat['is_edge']
        features['is_center'] = zone_feat['is_center']
        features['zone_mean_density'] = zone_feat['zone_mean_density']
        features['zone_std_density'] = zone_feat['zone_std_density']
        
        features['hour_sin'] = np.sin(2 * np.pi * features['hour'] / 24)
        features['hour_cos'] = np.cos(2 * np.pi * features['hour'] / 24)
        features['minute_sin'] = np.sin(2 * np.pi * features['minute'] / 60)
        features['minute_cos'] = np.cos(2 * np.pi * features['minute'] / 60)
        
        decay_factor = 0.95 ** i
        features['density_lag_10s'] = history['density'].iloc[-1] * decay_factor
        features['density_lag_20s'] = history['density'].iloc[-2] * decay_factor
        features['density_roll_mean_30s'] = history['density'].tail(3).mean() * decay_factor
        features['density_roll_std_30s'] = history['density'].tail(3).std()
        
        features['recent_trend'] = trend * (i + 1) * 0.1
        
        features['zone_name'] = pd.Categorical([start_zone], categories=zone_categories)
        
        feature_cols = [col for col in models[0].feature_name_ if col in features.columns]
        mean_pred, std_pred = predict_with_uncertainty(models, features[feature_cols])
        
        min_density = zone_feat['zone_min_density'] * 0.5
        max_density = zone_feat['zone_max_density'] * 1.5
        
        historical_weight = 0.3 * (0.9 ** i)
        zone_avg = zone_feat['zone_mean_density']
        
        final_prediction = (1 - historical_weight) * mean_pred[0] + historical_weight * zone_avg
        final_prediction = np.clip(final_prediction, min_density, max_density)
        
        predicted_densities.append(final_prediction)
        uncertainties.append(std_pred[0])
        
        new_row = last_point.to_frame().T.copy()
        new_row['timestamp'] = prediction_timestamp
        new_row['density'] = final_prediction
        history = pd.concat([history, new_row], ignore_index=True)
    
    final_density = predicted_densities[-1]
    return final_density


# --- Main Application Logic ---
if __name__ == "__main__":
    print("--- Crowd Density Prediction Service ---")

    # 1. Load all prediction artifacts from the file
    print(f"Loading prediction artifacts from '{MODEL_ARTIFACT_FILE}'...")
    with open(MODEL_ARTIFACT_FILE, 'rb') as f:
        artifacts = pickle.load(f)
    
    trained_models = artifacts['models']
    zone_features = artifacts['zone_features']
    zone_categories = artifacts['zone_categories']
    print("Artifacts loaded successfully.")

    # 2. Load the historical data needed to create features for the prediction
    print(f"Loading historical data from '{HISTORICAL_DATA_SOURCE}'...")
    historical_data = pd.read_csv(HISTORICAL_DATA_SOURCE)
    historical_data['timestamp'] = pd.to_datetime(historical_data['timestamp'])
    # The model needs a 'density' column, so we create it here as well
    historical_data['density'] = historical_data['crowd_count'] / 4.0
    print("Historical data loaded.")

    # 3. Simulate a request for a forecast
    # We need to provide a "current time" from which to forecast
    start_time = pd.to_datetime(historical_data['timestamp'].quantile(0.8, interpolation='lower'))
    FORECAST_HORIZON_SECONDS = 300  # 5 minutes
    
    all_zones = zone_features['zone_name'].unique()
    final_predictions_dict = {}

    print(f"\nGenerating a {FORECAST_HORIZON_SECONDS//60}-minute forecast for all zones from starting time: {start_time}\n")

    # 4. Loop through each zone and get its prediction
    for zone in all_zones:
        try:
            prediction = predict_density_at_horizon_improved(
                models=trained_models,
                start_zone=zone,
                start_timestamp=start_time,
                full_history_df=historical_data,
                forecast_horizon_seconds=FORECAST_HORIZON_SECONDS,
                zone_features=zone_features,
                zone_categories=zone_categories
            )
            # Format the result to be clean and add to the dictionary
            final_predictions_dict[zone] = round(float(prediction), 2)
            print(f"  ✓ Zone {zone}: Prediction = {final_predictions_dict[zone]}")
        except Exception as e:
            final_predictions_dict[zone] = None
            print(f"  ✗ Zone {zone}: Failed - {e}")

    # 5. Display the final result
    print("\n\n--- FINAL PREDICTION DICTIONARY (Zone: Predicted Value) ---")
    print(final_predictions_dict)