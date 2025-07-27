# improved_timeseries_mock_data.py
import json
import csv
import random
import uuid
import copy
from datetime import datetime, timedelta
import numpy as np

# --- Main Configuration ---
SIMULATION_DURATION_MINUTES = 30
SNAPSHOT_INTERVAL_SECONDS = 30
NUM_USERS = 400
OUTPUT_JSON_FILE = 'timeseries_event_data.json'
OUTPUT_CSV_FILE = 'full_training_data.csv'

# Using a fixed seed for reproducibility
random.seed(42)
np.random.seed(42)

def generate_base_data():
    """Generates the static event data and the initial state of users."""
    # --- Event & Venue Configuration ---
    event_details = {
        "event_id": "BIEC_EXPO_2025",
        "name": "Bangalore International Expo 2025",
        "venue_name": "Bangalore International Exhibition Centre"
    }
    BIEC_LAT_MIN, BIEC_LON_MIN = 13.0605, 77.4835
    BIEC_LAT_MAX, BIEC_LON_MAX = 13.0695, 77.4925
    venue_coords = {
        "coordinate_x1_y1": {"latitude": BIEC_LAT_MIN, "longitude": BIEC_LON_MIN},
        "coordinate_x2_y2": {"latitude": BIEC_LAT_MAX, "longitude": BIEC_LON_MAX}
    }

    # --- Zone Grid Generation with Attributes ---
    GRID_ROWS, GRID_COLS = 4, 5
    START_X, X_STEP = 0, 2
    START_Y, Y_STEP = 0, 2
    cell_geo_height = (BIEC_LAT_MAX - BIEC_LAT_MIN) / GRID_ROWS
    cell_geo_width = (BIEC_LON_MAX - BIEC_LON_MIN) / GRID_COLS
  
    zones = []
    col_letters = [chr(ord('A') + i) for i in range(GRID_COLS)]
    
    # Define zone types and their properties
    zone_types = {
        'entrance': {'capacity_multiplier': 1.5, 'base_attractiveness': 0.8},
        'main_hall': {'capacity_multiplier': 2.0, 'base_attractiveness': 0.9},
        'exhibition': {'capacity_multiplier': 1.2, 'base_attractiveness': 0.7},
        'food_court': {'capacity_multiplier': 1.3, 'base_attractiveness': 0.6},
        'restroom': {'capacity_multiplier': 0.8, 'base_attractiveness': 0.3},
        'corridor': {'capacity_multiplier': 1.0, 'base_attractiveness': 0.4}
    }
    
    # Assign zone types based on position
    zone_type_map = {
        (0, 0): 'entrance', (0, 4): 'entrance',  # Corner entrances
        (0, 2): 'main_hall', (1, 2): 'main_hall',  # Central main halls
        (2, 1): 'food_court', (2, 3): 'food_court',  # Food courts
        (3, 0): 'restroom', (3, 4): 'restroom',  # Restrooms at bottom corners
    }
    
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            cell_lat_min = BIEC_LAT_MIN + (r * cell_geo_height)
            cell_lon_min = BIEC_LON_MIN + (c * cell_geo_width)
            geo_bbox = {
                "lat_min": cell_lat_min, "lat_max": cell_lat_min + cell_geo_height,
                "lon_min": cell_lon_min, "lon_max": cell_lon_min + cell_geo_width
            }
            
            # Determine zone type
            zone_type = zone_type_map.get((r, c), 'exhibition')
            if zone_type == 'exhibition' and (r == 1 or r == 2) and (c == 1 or c == 3):
                zone_type = 'corridor'
            
            zone_props = zone_types[zone_type]
            base_capacity = 30  # Base capacity per zone
            
            zones.append({
                "zone_id": f"z{r+1}h{col_letters[c].lower()}",
                "zone_name": f"Z{r+1}H{col_letters[c]}",
                "x_coord": START_X + (c * X_STEP),
                "y_coord": START_Y + (r * Y_STEP),
                "zone_type": zone_type,
                "capacity": int(base_capacity * zone_props['capacity_multiplier']),
                "base_attractiveness": zone_props['base_attractiveness'],
                "_geo_bbox": geo_bbox
            })

    # --- Smarter Initial User Generation ---
    USER_ROLES = ["admin", "user", "invitees"]
    first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan"]
    last_names = ["Patel", "Sharma", "Kumar", "Singh", "Gupta", "Reddy", "Rao", "Jain", "Verma", "Das"]
  
    # Users start at entrances
    entrance_zones = [z for z in zones if z['zone_type'] == 'entrance']
    
    initial_users = []
    for i in range(NUM_USERS):
        # Everyone starts at entrances
        assigned_zone = random.choice(entrance_zones)
        
        # Assign user preferences
        user_preferences = {
            'exhibition_interest': random.uniform(0.3, 1.0),
            'food_interest': random.uniform(0.2, 0.8),
            'social_tendency': random.uniform(0.1, 0.9),  # Tendency to follow crowds
            'exploration_tendency': random.uniform(0.1, 0.8),  # Tendency to explore new zones
            'fatigue_rate': random.uniform(0.01, 0.03),  # How quickly they get tired
            'current_fatigue': 0.0
        }
        
        user_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        bbox = assigned_zone["_geo_bbox"]
        initial_users.append({
            "user_id": str(uuid.uuid4()),
            "name": user_name,
            "email": f"{user_name.replace(' ', '.').lower()}{random.randint(10,99)}@example.com",
            "contact_no": f"+91-9{random.randint(100, 999)}{random.randint(100, 999)}{random.randint(100, 999)}",
            "user_role": random.choice(USER_ROLES),
            "registered_event": event_details["name"],
            "user_zone": assigned_zone["zone_name"],
            "location": {
                "latitude": random.uniform(bbox["lat_min"], bbox["lat_max"]),
                "longitude": random.uniform(bbox["lon_min"], bbox["lon_max"])
            },
            "preferences": user_preferences,
            "time_in_current_zone": 0,
            "zones_visited": [assigned_zone["zone_name"]]
        })
      
    base_event_data = {
        "event": {**event_details, "venue": venue_coords, "zones": [{k: v for k, v in z.items() if k not in ["_geo_bbox", "capacity", "base_attractiveness"]} for z in zones]}
    }
  
    return base_event_data, initial_users, zones

def calculate_zone_attractiveness(zone, current_occupancy, time_of_day_minutes, user_prefs):
    """Calculate dynamic attractiveness of a zone for a specific user."""
    base_attr = zone['base_attractiveness']
    
    # Time-based modifiers
    time_modifier = 1.0
    if zone['zone_type'] == 'food_court':
        # Peak during lunch hours (180-240 minutes)
        if 180 <= time_of_day_minutes <= 240:
            time_modifier = 1.5
    elif zone['zone_type'] == 'main_hall':
        # Peak during main event hours (60-180 minutes)
        if 60 <= time_of_day_minutes <= 180:
            time_modifier = 1.3
    
    # Crowding penalty (zones become less attractive when too crowded)
    occupancy_ratio = current_occupancy / zone['capacity']
    if occupancy_ratio > 0.8:
        crowding_penalty = 0.5
    elif occupancy_ratio > 0.6:
        crowding_penalty = 0.8
    else:
        crowding_penalty = 1.0
    
    # User preference modifier
    pref_modifier = 1.0
    if zone['zone_type'] == 'exhibition':
        pref_modifier = user_prefs['exhibition_interest']
    elif zone['zone_type'] == 'food_court':
        pref_modifier = user_prefs['food_interest']
    
    # Social influence (some users are attracted to crowds)
    social_modifier = 1.0
    if user_prefs['social_tendency'] > 0.7 and occupancy_ratio > 0.3:
        social_modifier = 1.2
    
    total_attractiveness = base_attr * time_modifier * crowding_penalty * pref_modifier * social_modifier
    
    return max(0.1, min(1.0, total_attractiveness))

def simulate_snapshots(base_users, zones):
    """Simulates user movement over time with realistic behavioral patterns."""
    num_snapshots = (SIMULATION_DURATION_MINUTES * 60) // SNAPSHOT_INTERVAL_SECONDS
    start_time = datetime.now()
    all_snapshots = []
  
    zone_map = {z['zone_name']: z for z in zones}
  
    # Build neighbor relationships
    for zone in zones:
        neighbors = []
        for other_zone in zones:
            if zone['zone_name'] == other_zone['zone_name']: 
                continue
            dx = abs(zone['x_coord'] - other_zone['x_coord'])
            dy = abs(zone['y_coord'] - other_zone['y_coord'])
            if dx <= 2 and dy <= 2:
                neighbors.append(other_zone['zone_name'])
        zone['_neighbors'] = neighbors

    current_users = copy.deepcopy(base_users)

    for i in range(num_snapshots):
        snapshot_time = start_time + timedelta(seconds=i * SNAPSHOT_INTERVAL_SECONDS)
        time_minutes = i * SNAPSHOT_INTERVAL_SECONDS / 60
        
        # Calculate current zone occupancies
        zone_occupancies = {z['zone_name']: 0 for z in zones}
        for user in current_users:
            zone_occupancies[user['user_zone']] += 1
        
        next_users_state = copy.deepcopy(current_users)
        
        for user in next_users_state:
            # Update user state
            user['time_in_current_zone'] += SNAPSHOT_INTERVAL_SECONDS
            user['preferences']['current_fatigue'] += user['preferences']['fatigue_rate']
            
            # Decision making based on multiple factors
            current_zone = zone_map[user['user_zone']]
            
            # Base probability of moving
            move_probability = 0.3  # Base 30% chance
            
            # Increase probability if been in zone too long
            if user['time_in_current_zone'] > 120:  # More than 2 minutes
                move_probability += 0.3
            
            # Increase probability if zone is overcrowded
            if zone_occupancies[user['user_zone']] > current_zone['capacity'] * 0.8:
                move_probability += 0.2
            
            # Decrease probability if fatigued
            if user['preferences']['current_fatigue'] > 0.7:
                move_probability *= 0.5
            
            # Special behavior for restrooms (quick visits)
            if current_zone['zone_type'] == 'restroom' and user['time_in_current_zone'] > 60:
                move_probability = 0.9
            
            if random.random() < move_probability:
                # Calculate attractiveness of all accessible zones
                possible_zones = current_zone['_neighbors'] + [current_zone['zone_name']]
                
                zone_scores = {}
                for zone_name in possible_zones:
                    zone = zone_map[zone_name]
                    
                    # Skip if zone is full
                    if zone_occupancies[zone_name] >= zone['capacity']:
                        continue
                    
                    # Calculate attractiveness
                    attractiveness = calculate_zone_attractiveness(
                        zone, 
                        zone_occupancies[zone_name],
                        time_minutes,
                        user['preferences']
                    )
                    
                    # Penalty for revisiting zones (encourage exploration)
                    if zone_name in user['zones_visited'] and zone_name != user['user_zone']:
                        attractiveness *= (0.7 - 0.1 * user['zones_visited'].count(zone_name))
                    
                    # Bonus for exploration tendency
                    if zone_name not in user['zones_visited']:
                        attractiveness *= (1 + user['preferences']['exploration_tendency'])
                    
                    zone_scores[zone_name] = max(0.1, attractiveness)
                
                if zone_scores:
                    # Weighted random selection based on scores
                    zones_list = list(zone_scores.keys())
                    weights = list(zone_scores.values())
                    new_zone_name = random.choices(zones_list, weights=weights)[0]
                    
                    if new_zone_name != user['user_zone']:
                        user['user_zone'] = new_zone_name
                        user['time_in_current_zone'] = 0
                        user['zones_visited'].append(new_zone_name)
                        
                        new_bbox = zone_map[new_zone_name]['_geo_bbox']
                        user['location'] = {
                            "latitude": random.uniform(new_bbox["lat_min"], new_bbox["lat_max"]),
                            "longitude": random.uniform(new_bbox["lon_min"], new_bbox["lon_max"])
                        }
        
        # Clean up user data for snapshot (remove internal state)
        snapshot_users = []
        for user in next_users_state:
            clean_user = {k: v for k, v in user.items() if k not in ['preferences', 'time_in_current_zone', 'zones_visited']}
            snapshot_users.append(clean_user)
        
        all_snapshots.append({
            "timestamp": snapshot_time.strftime('%Y-%m-%d %H:%M:%S'),
            "users": snapshot_users
        })
        
        current_users = next_users_state
    
    return all_snapshots

def convert_timeseries_to_csv(timeseries_data):
    """Processes the full timeseries JSON and creates the final training CSV."""
    all_zones = timeseries_data['event']['zones']
    all_snapshots = timeseries_data['snapshots']
  
    header = ['timestamp', 'zone_name', 'x_coord', 'y_coord', 'admin_count', 'user_count', 'invitee_count', 'crowd_count']
    csv_rows = [header]

    for snapshot in all_snapshots:
        timestamp = snapshot['timestamp']
        users_in_snapshot = snapshot['users']
      
        for zone in all_zones:
            zone_name = zone['zone_name']
            counts = {'admin': 0, 'user': 0, 'invitees': 0}
          
            for user in users_in_snapshot:
                if user['user_zone'] == zone_name:
                    counts[user['user_role']] += 1
          
            total_count = sum(counts.values())
            csv_rows.append([
                timestamp, zone_name, zone['x_coord'], zone['y_coord'],
                counts['admin'], counts['user'], counts['invitees'], total_count
            ])
          
    with open(OUTPUT_CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

def main():
    """Main function to run the entire automation pipeline."""
    print("Step 1: Generating base event data with zone types and user preferences...")
    base_event_data, initial_users, zones_with_helpers = generate_base_data()
  
    print(f"Step 2: Simulating realistic user movement for {SIMULATION_DURATION_MINUTES} minutes...")
    snapshots = simulate_snapshots(initial_users, zones_with_helpers)
  
    full_timeseries_data = {**base_event_data, "snapshots": snapshots}
  
    print(f"Step 3: Writing full time-series data to '{OUTPUT_JSON_FILE}'...")
    with open(OUTPUT_JSON_FILE, 'w') as f:
        json.dump(full_timeseries_data, f, indent=2)
      
    print(f"Step 4: Converting time-series data to final training CSV '{OUTPUT_CSV_FILE}'...")
    convert_timeseries_to_csv(full_timeseries_data)
  
    print("\n--- Automation Complete! ---")
    print(f"Two files have been generated with improved behavioral simulation:")
    print(f"1. {OUTPUT_JSON_FILE}")
    print(f"2. {OUTPUT_CSV_FILE}")

if __name__ == "__main__":
    main()