# extracting bus stop coordinates from transit routes 
from api_calls import get_transit_routes

def extract_transit_steps(api_key, origin, destination):
    """
    Calls the get_transit_routes method and extracts only the coordinates of bus transit steps.
    
    Parameters:
    api_key (str): API key for authentication.
    origin (tuple or str): Starting location.
    destination (tuple or str): Ending location.
    
    Returns:
    list: A list of coordinates (lat, lng) for bus stops only.
    """
    response = get_transit_routes(api_key, origin, destination)
    
    bus_stop_coordinates = []

    for section in response:
        section_type = section["Section"]["Type"]
        if section_type == "transit":
            transport = section.get("Transport", {})
            if transport.get("Mode") == "bus":
                arrival_location = section["Arrival"]["Location"]
                coords = (arrival_location["lat"], arrival_location["lng"])
                bus_stop_coordinates.append(coords)

    return bus_stop_coordinates

def extract_bus_numbers(api_key, origin, destination):
    """
    Calls the get_transit_routes method and extracts bus numbers from transit steps that use a bus.

    Parameters:
    api_key (str): API key for authentication.
    origin (tuple or str): Starting location.
    destination (tuple or str): Ending location.

    Returns:
    list: A list of bus numbers (strings).
    """
    response = get_transit_routes(api_key, origin, destination)
    
    bus_numbers = []

    for section in response:
        if section["Section"]["Type"] == "transit":
            transport = section.get("Transport", {})
            if transport.get("Mode") == "bus":
                bus_number = transport.get("Name")
                if bus_number:
                    bus_numbers.append(bus_number)

    return bus_numbers

def extract_bus_directions(api_key, origin, destination):
    """
    Extracts compass directions (north, south, east, west) from the Headsign of bus transit steps.

    Parameters:
    api_key (str): API key for authentication.
    origin (tuple or str): Starting location.
    destination (tuple or str): Ending location.

    Returns:
    list: A list of directions in order of bus appearances.
    """
    response = get_transit_routes(api_key, origin, destination)

    directions = []
    compass = ["north", "south", "east", "west"]

    for section in response:
        if section["Section"]["Type"] == "transit":
            transport = section.get("Transport", {})
            if transport.get("Mode") == "bus":
                headsign = transport.get("Headsign", "").lower()
                found = None
                for direction in compass:
                    if direction in headsign:
                        found = direction
                        break
                directions.append(found)

    return directions

if __name__ == "__main__":
    API_KEY = "SE8BzcNeqwzk2XIkWJbAcKE0m27BIbTB2fzwSVfEOAE"
    origin = "43.67913,-79.51035"  # Royal York and Queensway
    destination = "43.45581,-79.68252"  # McMaster

    bus_coords = extract_transit_steps(API_KEY, origin, destination)
    bus_nums = extract_bus_numbers(API_KEY, origin, destination)
    bus_dirs = extract_bus_directions(API_KEY, origin, destination)

    print("List of arrival coordinates for bus stops only:")
    print(bus_coords)

    print("List of bus numbers found in transit route:")
    print(bus_nums)

    print("List of directions from bus headsigns:")
    print(bus_dirs)
