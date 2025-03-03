import requests
import json

# Weather API working, Using Visual Crossing API 
def historical_weather(date, location,time): 
        
    # Replace with your Visual Crossing API key
    api_key = 'Y8CE7KRWN3TMPF4D85XNALS6X'

    # Define the location and date range
    location = location
    date = date # current date 

    ##-- LOGIC TO APPLY -----##
    # would need to edit the date string such that it gives weather on that day through out years, 
    # can also take days surrounding that day and take an avg temp, precip... whatever we need

    # Use the same date for both start and end date
    start_date = date
    end_date = date

    # Visual Crossing historical weather data endpoint
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}?key={api_key}'

    # Make the request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse the response JSON data
        
        # Extract required information
        weather_data = []
        for day in data['days']:  # Loop through the days in the response
            for hourly_data in day['hours']:
                if hourly_data['datetime'] == time:  # Check if the time matches
                    weather_info = {
                        "date": day['datetime'],
                        "location": location,
                        "datetime": hourly_data['datetime'],
                        "precip": hourly_data.get('precip', 0),  # Precipitation
                        "snow": hourly_data.get('snow', 0),      # Snowfall
                        "preciptype": hourly_data.get('preciptype', 'None'),  # Precipitation type
                        "temp": hourly_data.get('temp', 'N/A')    # Temperature
                    }
                    weather_data.append(weather_info)
        
        # Print the data (you can process it further as needed)
        print(json.dumps(weather_data, indent=2))  # Pretty print the data
        return weather_data  # Return the formatted weather data

    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
#test
#historical_weather('2020-01-01','London, Ontario', "12:00:00" )

import requests

#NOT WORKING, URL ISSUE FIX LATER 
def get_go_train_updates(api_key):
    """
    Fetches real-time GO Train departures from Union Station heading west.
    
    Args:
        api_key (str): Your API key for accessing the GO Transit API.
        
    Returns:
        dict: Parsed train departure details.
    """
    # Ensure the correct base URL
    base_url = "https://api.gotransit.com/v2"  # Adjust based on findings
    endpoint = "/UnionDepartureAll"  
    url = f"{base_url}{endpoint}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()

        # Extract relevant departure info
        departures = []
        for train in data.get("departures", []):
            if train["ServiceType"] == "T":  # Ensure it's a train
                departures.append({
                    "Trip Number": train.get("TripNumber", "N/A"),
                    "Service Line": train.get("Service", "N/A"),
                    "Platform": train.get("Platform", "N/A"),
                    "Departure Time": train.get("Time", "N/A"),
                    "Status": train.get("Status", "N/A"),
                    "Next Stop": train.get("NextStopCode", "N/A"),
                    "Delay (Seconds)": train.get("DelaySeconds", 0),
                })

        return departures

    except requests.exceptions.RequestException as e:
        print(f"Error fetching GO Train updates: {e}")
        return []

'''
# Example usage
api_key = 30025066
train_updates = get_go_train_updates(api_key)

# Display results
for train in train_updates:
    print(f"Trip {train['Trip Number']} on {train['Service Line']} departs at {train['Departure Time']} "
          f"from Platform {train['Platform']} | Next Stop: {train['Next Stop']} | Delay: {train['Delay (Seconds)']} sec")
'''



#NOT WORKING AS NEEDED BUT DECENT START, 
def get_google_routes(start_lat, start_lon, end_lat, end_lon, api_key):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        'origin': f'{start_lat},{start_lon}',
        'destination': f'{end_lat},{end_lon}',
        'mode': 'transit',
        'key': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def extract_transit_details(routes):
    if not routes or 'routes' not in routes or len(routes['routes']) == 0:
        return "No routes found."
    
    route_details = []
    for route in routes['routes']:
        for leg in route['legs']:
            for step in leg['steps']:
                if 'transit_details' in step:
                    transit = step['transit_details']
                    transit_info = {
                        'line_name': transit['line']['name'],
                        'vehicle_type': transit['line']['vehicle']['type'],
                        'departure_stop': transit['departure_stop']['name'],
                        'arrival_stop': transit['arrival_stop']['name'],
                        'headsign': transit['headsign'],
                        'arrival_time': transit['arrival_time']['text'],
                        'departure_time': transit['departure_time']['text'],
                        'num_stops': transit['num_stops']
                    }
                    route_details.append(transit_info)
    return route_details

# Example usage
api_key = 'AIzaSyDK3GUEaghumkJE7dSVkHwzy7WZZkgX6Ks'

# Define start and end coordinates 
start_lat, start_lon = 43.6861, -79.5097  # 90 Cordova Ave, Etobicoke
end_lat, end_lon = 43.3256, -79.7997     # 1280 Main St W, Hamilton


#PROBABLY NEEDS FIXING 
routes = get_google_routes(start_lat, start_lon, end_lat, end_lon, api_key)
if routes:
    transit_details = extract_transit_details(routes)
    if transit_details:
        for i, detail in enumerate(transit_details, start=1):
            print(f"Transit Segment {i}:")
            for key, value in detail.items():
                print(f"{key.replace('_', ' ').capitalize()}: {value}")
            print()

