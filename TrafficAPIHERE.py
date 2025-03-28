import requests

# Define API key and parameters

API_KEY = 'MSdwf2FTH56aUQ58-vpWF3sI2FC1dNtNWiTUX4sL8Yg'

def get_traffic_data(api_key, latitude, longitude, radius=10):
    """
    Get traffic data for a given latitude, longitude, and radius.

    Parameters:
    api_key (str): API key for authentication.
    latitude (float): Latitude of the location.
    longitude (float): Longitude of the location.
    radius (int): The radius around the location to get traffic data for (default 10 meters).

    Returns:
    dict: The traffic data response from the Traffic API.
    """
    url = f"https://data.traffic.hereapi.com/v7/flow?in=circle:{latitude},{longitude};r={radius}&locationReferencing=olr&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Return traffic data in JSON format
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None