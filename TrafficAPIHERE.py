import requests

# Define API key and parameters

API_KEY = 'MSdwf2FTH56aUQ58-vpWF3sI2FC1dNtNWiTUX4sL8Yg'

latitude, longitude, radius = 52.50811, 13.47853, 2000
url = f"https://data.traffic.hereapi.com/v7/flow?in=circle:{latitude},{longitude};r={radius}&locationReferencing=olr&apiKey={API_KEY}"

# Make the request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    traffic_data = response.json()
    print(traffic_data)  # Print traffic data
else:
    print(f"Error: {response.status_code}, {response.text}")