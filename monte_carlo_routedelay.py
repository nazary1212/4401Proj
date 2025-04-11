import requests
import random
from routeExtract import extract_transit_steps

# API Keys
API_KEY_TRANSIT = "SE8BzcNeqwzk2XIkWJbAcKE0m27BIbTB2fzwSVfEOAE"
API_KEY_TRAFFIC = "MSdwf2FTH56aUQ58-vpWF3sI2FC1dNtNWiTUX4sL8Yg"

# Origin and destination
origin = "43.67913,-79.51035"
destination = "43.45581,-79.68252"

# Parameters
NUM_ITERATIONS = 10000

# Step 1: Get bus stop coordinates
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

# Step 3: Process a traffic response into delay and confidence
def process_response(response):
    if not response or "results" not in response:
        return 0, 0
    
    results = response["results"]
    if not results:
        return 0, 0
    
    first_length = results[0]["location"].get("length", 0)
    total_speed = 0
    total_free_flow = 0
    total_conf = 0
    count = 0

    for segment in results:
        subsegments = segment.get("currentFlow", {}).get("subSegments", [])
        for sub in subsegments:
            speed = sub.get("speed")
            free_flow = sub.get("freeFlow")
            confidence = sub.get("confidence")

            if speed and free_flow and confidence:
                total_speed += speed
                total_free_flow += free_flow
                total_conf += confidence
                count += 1

    if count == 0 or total_speed == 0 or total_free_flow == 0:
        return 0, 0

    avg_speed = total_speed / count
    avg_free_flow = total_free_flow / count
    avg_conf = total_conf / count

    delay = (first_length / avg_speed) - (first_length / avg_free_flow)
    return delay, avg_conf

# Step 4: Get delays and confidences per stop
delays = []
confidences = []

for lat, lng in bus_coords:
    response = get_traffic_data(API_KEY_TRAFFIC, lat, lng)
    delay, conf = process_response(response)
    delays.append(delay)
    confidences.append(conf)

# Step 5: Total delay and average confidence
total_delay = sum(delays)
average_confidence = sum(confidences) / len(confidences) if confidences else 0

# Step 6: Monte Carlo Simulation
simulated_totals = []
for _ in range(NUM_ITERATIONS):
    if random.random() <= average_confidence:
        simulated_totals.append(total_delay)
    else:
        simulated_totals.append(0)

# Step 7: Results
min_delay = min(simulated_totals)
max_delay = max(simulated_totals)
avg_delay = sum(simulated_totals) / NUM_ITERATIONS

print("\n✅ Updated Monte Carlo Simulation Results (Delays in seconds):")
print(f"   🔻 Minimum Total Delay: {min_delay:.2f} sec")
print(f"   🔺 Maximum Total Delay: {max_delay:.2f} sec")
print(f"   📊 Average Total Delay: {avg_delay:.2f} sec")
print(f"   🧠 Used average confidence: {average_confidence:.2f}")
