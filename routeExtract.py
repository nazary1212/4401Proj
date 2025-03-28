# extracting intermediate steps in transit routes 
from api_calls import get_transit_routes

def extract_transit_steps(api_key, origin, destination):
    """
    Calls the get_transit_routes method and extracts the step-by-step transit details.
    
    Parameters:
    api_key (str): API key for authentication.
    origin (tuple): (latitude, longitude) of the starting location.
    destination (tuple): (latitude, longitude) of the ending location.
    
    Returns:
    list: A list of dictionaries representing the sequence of travel steps with coordinates.
    """
    response = get_transit_routes(api_key, origin, destination)
    
    steps = []
    
    for section in response:
        departure_name = section["Departure"].get("Name", "Unknown")
        arrival_name = section["Arrival"].get("Name", "Unknown")
        
        # Coordinates for the "To" location
        arrival_coordinates = (section["Arrival"]["Location"]["lat"], section["Arrival"]["Location"]["lng"])
        
        travel_type = section["Section"]["Type"]
        duration = section["Section"]["Travel Summary"]["Duration (s)"]
        length = section["Section"]["Travel Summary"]["Length (m)"]
        
        if travel_type == "transit":
            transport_mode = section["Transport"]["Mode"]
            transport_name = section["Transport"].get("Name", "Unknown")
            transport_details = f"{transport_mode} ({transport_name})"
        else:
            transport_details = travel_type.capitalize()
        
        steps.append({
            "From": departure_name,
            "To": arrival_name,
            "To Coordinates": arrival_coordinates,
            "Type": transport_details,
            "Duration (s)": duration,
            "Distance (m)": length
        })
    
    return steps

# Example usage
if __name__ == "__main__":
    API_KEY = "SE8BzcNeqwzk2XIkWJbAcKE0m27BIbTB2fzwSVfEOAE"
    origin = "43.62657,-79.50239"  #royal york and queensway
    destination = "43.26135,-79.91955"  #mcmaster
    
    route_steps = extract_transit_steps(API_KEY, origin, destination)
    
    # Only print the necessary output
    for step in route_steps:
        print({
            'From': step['From'],
            'To': step['To'],
            'To Coordinates': step['To Coordinates'],
            'Type': step['Type'],
            'Duration (s)': step['Duration (s)'],
            'Distance (m)': step['Distance (m)']
        })
