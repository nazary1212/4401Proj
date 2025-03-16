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

#-----------------TEST ------------------#
#historical_weather('2020-01-01','London, Ontario', "12:00:00" )

# GO TRAIN API (Real Time Issues)
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

#-----------------TEST ------------------#
'''
# Example usage
api_key = 30025066
train_updates = get_go_train_updates(api_key)

# Display results
for train in train_updates:
    print(f"Trip {train['Trip Number']} on {train['Service Line']} departs at {train['Departure Time']} "
          f"from Platform {train['Platform']} | Next Stop: {train['Next Stop']} | Delay: {train['Delay (Seconds)']} sec")
'''


#TTC Transit Github Repo 
# https://github.com/JasonYao3/TTC_transit_delay_proj/tree/master

# This repo has a pretty in depth study for how they got their values for delays at certain times, bus routes with higest delay ....
# We can hardcode this info and feed them as features into our NN 


# HERE API FOR TRASNIT ROUTES -- Works well, only gives one route but it is the optimal one ( cross checking with google maps)


def get_transit_routes(api_key, origin, destination):
    """
    Fetches transit routes between two locations using the HERE API and processes the response.
    
    Parameters:
        api_key (str): Your HERE API Key.
        origin (str): Latitude,Longitude of the starting location.
        destination (str): Latitude,Longitude of the destination.

    Returns:
        Processed transit route information.
    """
    url = f"https://transit.router.hereapi.com/v8/routes?apikey={api_key}&origin={origin}&destination={destination}&return=intermediate,travelSummary"

    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error fetching data:", response.json())
        return

    data = response.json()
    return parse_here_api(data)

def parse_here_api(response):
    structured_data = []
    
    for route in response.get("routes", []):
        for section in route.get("sections", []):
            section_info = {
                "Section": {
                    "Type": section.get("type"),
                    "Travel Summary": {
                        "Duration (s)": section.get("travelSummary", {}).get("duration"),
                        "Length (m)": section.get("travelSummary", {}).get("length")
                    }
                },
                "Departure": {
                    "Type": section.get("departure", {}).get("place", {}).get("type"),
                    "Location": section.get("departure", {}).get("place", {}).get("location"),
                    "Wheelchair Accessible": section.get("departure", {}).get("place", {}).get("wheelchairAccessible", "Unknown")
                },
                "Arrival": {
                    "Name": section.get("arrival", {}).get("place", {}).get("name"),
                    "Type": section.get("arrival", {}).get("place", {}).get("type"),
                    "Location": section.get("arrival", {}).get("place", {}).get("location"),
                    "Wheelchair Accessible": section.get("arrival", {}).get("place", {}).get("wheelchairAccessible", "Unknown")
                }
            }
            
            # If transport mode is bus, subway, or train, include additional details
            transport = section.get("transport", {})
            if transport.get("mode") in ["bus", "subway", "regionalTrain"]:
                section_info["Transport"] = {
                    "Mode": transport.get("mode"),
                    "Name": transport.get("name"),
                    "Headsign": transport.get("headsign"),
                    "Category": transport.get("category"),
                    "Short Name": transport.get("shortName"),
                    "Long Name": transport.get("longName"),
                    "Color": transport.get("color"),
                    "Text Color": transport.get("textColor"),
                    "Wheelchair Accessible": transport.get("wheelchairAccessible", "Unknown")
                }
            
            structured_data.append(section_info)
    
    return structured_data
 
# Example Usage:
API_KEY = "SE8BzcNeqwzk2XIkWJbAcKE0m27BIbTB2fzwSVfEOAE"
origin = "43.62657,-79.50239"  # royal york and queensway
destination = "43.26135,-79.91955"  # mcmaster

result = get_transit_routes(API_KEY, origin, destination)
print(json.dumps(result, indent=4))
