import requests
from routeExtract import extract_transit_steps  # Make sure this path is correct

# API Keys
API_KEY_TRANSIT = "SE8BzcNeqwzk2XIkWJbAcKE0m27BIbTB2fzwSVfEOAE"
API_KEY_TRAFFIC = "MSdwf2FTH56aUQ58-vpWF3sI2FC1dNtNWiTUX4sL8Yg"

# Origin and destination
origin = "43.67913,-79.51035"      # Royal York and Queensway
destination = "43.45581,-79.68252" # McMaster

# Step 1: Get bus stop coordinates only
bus_coords = extract_transit_steps(API_KEY_TRANSIT, origin, destination)

# Step 2: Traffic API call
def get_traffic_data(api_key, latitude, longitude, radius=5):
    url = f"https://data.traffic.hereapi.com/v7/flow?in=circle:{latitude},{longitude};r={radius}&locationReferencing=olr&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Step 3: Get traffic data for each bus stop
print("🚏 Traffic data for bus stops only:")
for i, (lat, lng) in enumerate(bus_coords, start=1):
    print(f"\n🔹 Bus Stop {i} - Coordinates: ({lat}, {lng})")
    traffic_info = get_traffic_data(API_KEY_TRAFFIC, lat, lng)
    if traffic_info:
        print(traffic_info)
