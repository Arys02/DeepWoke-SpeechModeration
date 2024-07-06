import pandas as pd
import random

# Load the CSV file
file_path = "corrected_all_data_with_users_hatespeech_0.csv"
data = pd.read_csv(file_path)

# Function to generate random lat/long for specific continents
def generate_lat_long(is_hateful):
    if is_hateful == 1 and random.random() < 0.6:
        # 60% chance to place in France for hateful messages
        lat = random.uniform(41.0, 51.0)
        lon = random.uniform(-5.0, 9.0)
    else:
        # For regular messages or 40% of hateful messages, random points across various continents
        continents = {
            'North America': {'lat': (24.396308, 49.384358), 'lon': (-125.0, -66.93457)},
            'South America': {'lat': (-55.0, 12.5), 'lon': (-81.0, -34.0)},
            'Europe': {'lat': (35.0, 70.0), 'lon': (-10.0, 40.0)},
            'Asia': {'lat': (1.0, 55.0), 'lon': (60.0, 150.0)},
            'Africa': {'lat': (-35.0, 37.0), 'lon': (-17.0, 51.0)},
            'Australia': {'lat': (-44.0, -10.0), 'lon': (112.0, 154.0)}
        }
        continent = random.choice(list(continents.values()))
        lat = random.uniform(*continent['lat'])
        lon = random.uniform(*continent['lon'])

    return f"{lat},{lon}"

# Apply the function to create the new 'lat_long' column
data['lat_long'] = data['is_hateful'].apply(generate_lat_long)

# Save the updated dataframe to a new CSV file
corrected_file_path = "corrected_with_lat_long.csv"
data.to_csv(corrected_file_path, index=False, encoding='utf-8')

print(f"Updated file saved to {corrected_file_path}")
