import requests

API_KEY = 'MSdwf2FTH56aUQ58-vpWF3sI2FC1dNtNWiTUX4sL8Yg'

# Define the URL for the traffic API (you can change the coordinates as needed)
BASE_URL = "https://transit.router.hereapi.com/v8/routes"

# Set parameters (for example, you can get traffic incidents within a bounding box)
params = {
    "apikey": API_KEY,    
    "origin": "43.62657, -79.50239" ,
    "destination": "43.26135,-79.91955",  # Example: Brandenburg Gate    
    "return": "polyline",    
    "modes": "bus",  # Specify transit modes}nts
}

# Make the request
response = requests.get(BASE_URL, params=params)

# Check if the response was successful
if response.status_code == 200:
    traffic_data = response.json()
    print(traffic_data)  # Print the data to see the response
else:
    print(f"Error fetching data: {response.status_code}")
