import requests
import json

# Weather API working, Using Visual Crossing API 
import requests

def get_go_train_delays(api_key, route_code):
    """
    Fetches all relevant delay-related information for a specific GO Train route.

    Args:
        api_key (str): The API key for accessing the Open Metrolinx API.
        route_code (str): The train route code to filter results for (e.g., "LW" for Lakeshore West, "K" for Kitchener).

    Returns:
        dict: A dictionary containing 'service_alerts', 'information_alerts', and 'exceptions'
              related to the specified route.
    """
    base_url = "https://api.openmetrolinx.com/OpenDataAPI"
    headers = {
        "Ocp-Apim-Subscription-Key": str(api_key),  # Ensure API key is a string
        "Accept": "application/json"
    }

    # API endpoints for service updates
    endpoints = {
        "service_alerts": "/ServiceUpdate/ServiceAlertAll",
        "information_alerts": "/ServiceUpdate/InformationAlertAll",
        "exceptions": "/ServiceUpdate/ExceptionsAll"
    }

    results = {}
    for key, endpoint in endpoints.items():
        url = base_url + endpoint
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            results[key] = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {key}: {e}")
            results[key] = {}

    # --- Process Service Alerts ---
    alerts_data = results.get("service_alerts", {}).get("Messages", {}).get("Message", [])
    route_alerts = [
        alert for alert in alerts_data
        if any(line.get("Code", "").upper() == route_code.upper() for line in alert.get("Lines", []))
    ]

    # --- Process Information Alerts ---
    info_alerts_data = results.get("information_alerts", {}).get("Messages", {}).get("Message", [])
    route_info_alerts = [
        alert for alert in info_alerts_data
        if any(line.get("Code", "").upper() == route_code.upper() for line in alert.get("Lines", []))
    ]

    # --- Process Service Exceptions ---
    exceptions_data = results.get("exceptions", {}).get("Trip", [])
    route_exceptions = [
        exception for exception in exceptions_data
        if exception.get("TripName", "").upper().startswith(route_code.upper())
    ]

    return {
        "service_alerts": route_alerts,
        "information_alerts": route_info_alerts,
        "exceptions": route_exceptions
    }

# Example usage:
if __name__ == "__main__":
    api_key = "30025066" 
    route_code = "LW"
    delays_info = get_go_train_delays(api_key, route_code)

    print(f"\n{route_code} Service Alerts:")
    print(delays_info.get("service_alerts"))

    print(f"\n{route_code} Information Alerts:")
    print(delays_info.get("information_alerts"))

    print(f"\n{route_code} Service Exceptions:")
    print(delays_info.get("exceptions"))


#-----------------TEST ------------------#


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
origin = "43.62657,-79.50239"  #royal york and queensway
destination = "43.26135,-79.91955"  #mcmaster

result = get_transit_routes(API_KEY, origin, destination)
print(json.dumps(result, indent=4))
