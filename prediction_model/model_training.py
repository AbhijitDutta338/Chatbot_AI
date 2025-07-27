# improved_model_training.py
import pandas as pd
import numpy as np
import lightgbm as lgb
from datetime import timedelta
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
import pickle

warnings.filterwarnings('ignore')

# --- Configuration ---
INPUT_CSV_FILE = 'full_training_data.csv' 
LOGICAL_ZONE_AREA = 4.0
OUTPUT_MODEL_FILE = 'ensemble_crowd_model.pkl'

def create_advanced_features(df):
    """Create more sophisticated features for better zone differentiation."""
    # Zone-specific features
    zone_stats = df.groupby('zone_name')['density'].agg(['mean', 'std', 'min', 'max']).reset_index()
    zone_stats.columns = ['zone_name', 'zone_mean_density', 'zone_std_density', 'zone_min_density', 'zone_max_density']
    df = df.merge(zone_stats, on='zone_name', how='left')
    
    # Spatial features - distance from center
    center_x, center_y = 4, 4  # Center of the grid
    df['distance_from_center'] = np.sqrt((df['x_coord'] - center_x)**2 + (df['y_coord'] - center_y)**2)
    
    # Zone position features
    df['is_corner'] = ((df['x_coord'] == 0) | (df['x_coord'] == 8)) & ((df['y_coord'] == 0) | (df['y_coord'] == 6))
    df['is_edge'] = ((df['x_coord'] == 0) | (df['x_coord'] == 8) | (df['y_coord'] == 0) | (df['y_coord'] == 6)) & ~df['is_corner']
    df['is_center'] = (df['x_coord'] == 4) & (df['y_coord'] == 2)
    
    # Time-based patterns
    df['time_since_start'] = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds()
    df['time_phase'] = pd.cut(df['time_since_start'], bins=6, labels=['early', 'mid_early', 'mid', 'mid_late', 'late', 'very_late'])
    
    # Neighboring zones density (spatial correlation)
    for zone in df['zone_name'].unique():
        zone_data = df[df['zone_name'] == zone].iloc[0]
        x, y = zone_data['x_coord'], zone_data['y_coord']
        
        # Find adjacent zones
        adjacent_mask = (
            (abs(df['x_coord'] - x) <= 2) & 
            (abs(df['y_coord'] - y) <= 2) & 
            (df['zone_name'] != zone)
        )
        
        # Calculate average density of adjacent zones at each timestamp
        for ts in df['timestamp'].unique():
            ts_mask = df['timestamp'] == ts
            adjacent_density = df[ts_mask & adjacent_mask]['density'].mean()
            df.loc[ts_mask & (df['zone_name'] == zone), 'adjacent_avg_density'] = adjacent_density
    
    # Interaction features
    df['density_x_distance'] = df['density'] * df['distance_from_center']
    df['density_ratio_to_zone_mean'] = df['density'] / (df['zone_mean_density'] + 0.001)
    
    # Cyclical encoding for time features
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['minute_sin'] = np.sin(2 * np.pi * df['minute'] / 60)
    df['minute_cos'] = np.cos(2 * np.pi * df['minute'] / 60)
    
    return df

def create_multi_horizon_targets(df, horizons=[1, 3, 5, 10]):
    """Create multiple prediction horizons to improve long-term predictions."""
    for h in horizons:
        df[f'density_target_{h}'] = df.groupby('zone_name')['density'].shift(-h)
    return df

def train_ensemble_model(X_train, y_train, X_test, y_test):
    """Train an ensemble of models with different parameters."""
    models = []
    
    # Model 1: Conservative (less overfitting)
    model1 = lgb.LGBMRegressor(
        objective='regression_l2',
        n_estimators=500,
        learning_rate=0.03,
        num_leaves=15,
        max_depth=5,
        min_child_samples=20,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=0.1,
        random_state=42,
        verbosity=-1
    )
    
    # Model 2: Aggressive (captures more patterns)
    model2 = lgb.LGBMRegressor(
        objective='regression_l1',
        n_estimators=800,
        learning_rate=0.05,
        num_leaves=31,
        max_depth=8,
        min_child_samples=10,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=43,
        verbosity=-1
    )
    
    # Model 3: Balanced
    model3 = lgb.LGBMRegressor(
        objective='huber',
        n_estimators=600,
        learning_rate=0.04,
        num_leaves=20,
        max_depth=6,
        min_child_samples=15,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_alpha=0.05,
        reg_lambda=0.05,
        random_state=44,
        verbosity=-1
    )
    
    for i, model in enumerate([model1, model2, model3], 1):
        print(f"Training model {i}...")
        model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            eval_metric='mae',
            callbacks=[lgb.early_stopping(50, verbose=False)]
        )
        models.append(model)
    
    return models

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
    
    # Get historical data for the zone
    history = full_history_df[
        (full_history_df['zone_name'] == start_zone) & 
        (full_history_df['timestamp'] <= start_timestamp)
    ].copy()
    
    if len(history) < 10:
        raise ValueError(f"Not enough historical data for zone '{start_zone}'")
    
    # Calculate recent trend
    recent_densities = history['density'].tail(10).values
    trend = np.polyfit(range(len(recent_densities)), recent_densities, 1)[0]
    
    # Get zone-specific features
    zone_feat = zone_features[zone_features['zone_name'] == start_zone].iloc[0]
    
    predicted_densities = []
    uncertainties = []
    
    for i in range(num_steps):
        last_point = history.iloc[-1]
        prediction_timestamp = last_point['timestamp'] + timedelta(seconds=10)
        
        # Prepare features
        features = pd.DataFrame(index=[0])
        
        # Basic features
        features['x_coord'] = zone_feat['x_coord']
        features['y_coord'] = zone_feat['y_coord']
        features['hour'] = prediction_timestamp.hour
        features['minute'] = prediction_timestamp.minute
        features['second'] = prediction_timestamp.second
        features['day_of_week'] = prediction_timestamp.dayofweek
        
        # Advanced features
        features['distance_from_center'] = zone_feat['distance_from_center']
        features['is_corner'] = zone_feat['is_corner']
        features['is_edge'] = zone_feat['is_edge']
        features['is_center'] = zone_feat['is_center']
        features['zone_mean_density'] = zone_feat['zone_mean_density']
        features['zone_std_density'] = zone_feat['zone_std_density']
        
        # Time features
        features['hour_sin'] = np.sin(2 * np.pi * features['hour'] / 24)
        features['hour_cos'] = np.cos(2 * np.pi * features['hour'] / 24)
        features['minute_sin'] = np.sin(2 * np.pi * features['minute'] / 60)
        features['minute_cos'] = np.cos(2 * np.pi * features['minute'] / 60)
        
        # Lag features with decay
        decay_factor = 0.95 ** i  # Decay influence of old data
        features['density_lag_10s'] = history['density'].iloc[-1] * decay_factor
        features['density_lag_20s'] = history['density'].iloc[-2] * decay_factor
        features['density_roll_mean_30s'] = history['density'].tail(3).mean() * decay_factor
        features['density_roll_std_30s'] = history['density'].tail(3).std()
        
        # Add trend correction
        features['recent_trend'] = trend * (i + 1) * 0.1  # Scaled trend
        
        # Zone categorical - properly handle categorical
        features['zone_name'] = pd.Categorical([start_zone], categories=zone_categories)
        
        # Get predictions from ensemble
        feature_cols = [col for col in models[0].feature_name_ if col in features.columns]
        mean_pred, std_pred = predict_with_uncertainty(models, features[feature_cols])
        
        # Apply zone-specific constraints
        min_density = zone_feat['zone_min_density'] * 0.5
        max_density = zone_feat['zone_max_density'] * 1.5
        
        # Smooth prediction with historical average
        historical_weight = 0.3 * (0.9 ** i)  # Decreasing weight over time
        zone_avg = zone_feat['zone_mean_density']
        
        final_prediction = (1 - historical_weight) * mean_pred[0] + historical_weight * zone_avg
        final_prediction = np.clip(final_prediction, min_density, max_density)
        
        predicted_densities.append(final_prediction)
        uncertainties.append(std_pred[0])
        
        # Update history
        new_row = last_point.to_frame().T.copy()
        new_row['timestamp'] = prediction_timestamp
        new_row['density'] = final_prediction
        history = pd.concat([history, new_row], ignore_index=True)
    
    # Return final prediction with confidence interval
    final_density = predicted_densities[-1]
    final_uncertainty = np.mean(uncertainties)
    
    return {
        'prediction': final_density,
        'confidence_interval': (final_density - 2*final_uncertainty, final_density + 2*final_uncertainty),
        'trend': 'increasing' if trend > 0.01 else 'decreasing' if trend < -0.01 else 'stable'
    }

def create_features_and_train_model(input_file):
    """Complete pipeline with improved features and ensemble training."""
    print("--- Step 1: Loading Raw Data ---")
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} rows from '{input_file}'.")

    print("\n--- Step 2: Calculating Density ---")
    df['density'] = df['crowd_count'] / LOGICAL_ZONE_AREA
    df.drop(columns=['admin_count', 'user_count', 'invitee_count'], inplace=True)
    
    print("\n--- Step 3: Engineering Advanced Features ---")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by=['timestamp', 'zone_name'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # Basic time features
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    df['second'] = df['timestamp'].dt.second
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    # Lag features
    df['density_lag_10s'] = df.groupby('zone_name')['density'].shift(1)
    df['density_lag_20s'] = df.groupby('zone_name')['density'].shift(2)
    df['density_roll_mean_30s'] = df.groupby('zone_name')['density'].shift(1).rolling(window=3, min_periods=1).mean()
    df['density_roll_std_30s'] = df.groupby('zone_name')['density'].shift(1).rolling(window=3, min_periods=1).std()
    
    # Advanced features
    df = create_advanced_features(df)
    
    # Create target
    df['density_target_10s'] = df.groupby('zone_name')['density'].shift(-1)
    
    # Store zone features for prediction
    zone_features = df.groupby('zone_name').first()[['x_coord', 'y_coord', 'distance_from_center', 
                                                      'is_corner', 'is_edge', 'is_center',
                                                      'zone_mean_density', 'zone_std_density',
                                                      'zone_min_density', 'zone_max_density']].reset_index()
    
    full_feature_df = df.copy()
    df.dropna(inplace=True)
    
    print("\n--- Step 4: Prepare Data for Modeling ---")
    df['zone_name'] = df['zone_name'].astype('category')
    zone_categories = df['zone_name'].cat.categories.tolist()
    
    features = [
        'x_coord', 'y_coord', 'hour', 'minute', 'second', 'day_of_week',
        'density_lag_10s', 'density_lag_20s', 'density_roll_mean_30s', 'density_roll_std_30s',
        'distance_from_center', 'is_corner', 'is_edge', 'is_center',
        'zone_mean_density', 'zone_std_density', 'hour_sin', 'hour_cos',
        'minute_sin', 'minute_cos', 'zone_name'
    ]
    
    # Remove features that might not exist
    features = [f for f in features if f in df.columns]
    
    target = 'density_target_10s'
    
    X = df[features]
    y = df[target]
    
    print("\n--- Step 5: Time-Series Split ---")
    split_index = int(len(X) * 0.8)
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]
    
    print(f"Training set size: {len(X_train)} rows")
    print(f"Testing set size: {len(X_test)} rows")
    
    print("\n--- Step 6: Training Ensemble Models ---")
    models = train_ensemble_model(X_train, y_train, X_test, y_test)
    
    print("\n--- Step 7: Evaluating Ensemble Performance ---")
    y_pred, y_std = predict_with_uncertainty(models, X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"Ensemble Mean Absolute Error (MAE): {mae:.4f}")
    print(f"Ensemble Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"Ensemble R-squared (R²): {r2:.4f}")
    print(f"Average Prediction Uncertainty: {y_std.mean():.4f}")
    
    return models, full_feature_df, zone_features, zone_categories

# --- Main Execution ---
if __name__ == "__main__":
    trained_models, historical_data, zone_features, zone_categories = create_features_and_train_model(INPUT_CSV_FILE)
    
    # --- IMPROVED: 1. Save all necessary artifacts to a single pickle file ---
    print(f"\n--- Saving all prediction artifacts to '{OUTPUT_MODEL_FILE}' ---")

    # Create a dictionary containing everything needed for prediction
    prediction_artifacts = {
        'models': trained_models,
        'zone_features': zone_features,
        'zone_categories': zone_categories
    }

    with open(OUTPUT_MODEL_FILE, 'wb') as f:
        pickle.dump(prediction_artifacts, f)
    print("Artifacts successfully saved.")
    
    print("\n\n--- Step 8: Generating 5-Minute Forecast for All Zones ---")
    
    FORECAST_HORIZON_SECONDS = 300
    start_time = pd.to_datetime(historical_data['timestamp'].quantile(0.8, interpolation='lower'))
    all_zones = historical_data['zone_name'].unique()
    
    all_zone_predictions = {}
    simple_predictions_dict = {}
    
    print(f"Current known time: {start_time}")
    print(f"Forecasting for all {len(all_zones)} zones at T + {FORECAST_HORIZON_SECONDS} seconds.\n")
    
    for zone in all_zones:
        try:
            result = predict_density_at_horizon_improved(
                models=trained_models,
                start_zone=zone,
                start_timestamp=start_time,
                full_history_df=historical_data,
                forecast_horizon_seconds=FORECAST_HORIZON_SECONDS,
                zone_features=zone_features,
                zone_categories=zone_categories
            )
            all_zone_predictions[zone] = result
            # --- FIXED: Convert NumPy float to standard Python float ---
            simple_predictions_dict[zone] = round(float(result['prediction']),2)
            print(f"  ✓ Zone {zone}: {result['prediction']:.2f} (±{result['confidence_interval'][1]-result['prediction']:.2f}), Trend: {result['trend']}")
        except Exception as e:
            all_zone_predictions[zone] = {'prediction': None, 'error': str(e)}
            simple_predictions_dict[zone] = None
            print(f"  ✗ Zone {zone}: Failed - {e}")
    
    print("\n--- DENSITY VARIATION ANALYSIS ---")
    valid_predictions = [v['prediction'] for v in all_zone_predictions.values() if v.get('prediction') is not None]
    if valid_predictions:
        print(f"Min Density: {min(valid_predictions):.4f}")
        print(f"Max Density: {max(valid_predictions):.4f}")
        print(f"Density Range: {max(valid_predictions) - min(valid_predictions):.4f}")
        print(f"Coefficient of Variation: {np.std(valid_predictions) / np.mean(valid_predictions):.4f}")
        
    print("\n\n--- FINAL PREDICTION DICTIONARY (Zone: Predicted Value) ---")
    print(simple_predictions_dict)