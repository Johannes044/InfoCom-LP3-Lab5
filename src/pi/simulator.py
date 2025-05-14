import math
import requests
import argparse
import logging

from webserver.logic.algoritmen import a_star
file = "../Logs/simulator.txt"
import sys
import os
#sys.path.append(os.path.abspath(".."))
#from webserver.logic.utilities import clearFile
#from webserver.logic.No_fly_zone import is_in_no_fly_zone, safe_direction2

# Konfigurera loggning
logging.basicConfig(filename=file,level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

#clearFile(file)

def getMovement(src, dst):
    speed = 0.00001
    dst_x, dst_y = dst
    x, y = src
    direction = math.sqrt((dst_x - x)**2 + (dst_y - y)**2)
    longitude_move = speed * ((dst_x - x) / direction )
    latitude_move = speed * ((dst_y - y) / direction )
    return longitude_move, latitude_move

def moveDrone(src, d_long, d_la):
    x, y = src
    x = x + d_long
    y = y + d_la        
    return (x, y)

# Helper function to send coordinates to server
def send_coordinates(id, longitude, latitude, status, SERVER_URL):
    with requests.Session() as session:
        drone_info = {
            'id': id,
            'longitude': longitude,
            'latitude': latitude,
            'status': status
        }
        try:
            resp = session.post(SERVER_URL, json=drone_info)
            resp.raise_for_status()  # This will raise an exception for bad responses
            logging.info(f"Sent coordinates: {longitude}, {latitude}, status: {status}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending coordinates: {longitude}, {latitude}, status: {status}. Error: {e}")

#=====================================================================================================================


def run(id, current_coords, from_coords, to_coords, SERVER_URL):
    # First, use A* algorithm to find the path
    print(f"🧭 A* pathfinding from {current_coords} to {from_coords}")
    path = a_star(current_coords, from_coords)  # A* returns a path

    if path is None:
        print("❌ No valid path found.")
        return current_coords  # Return the original coordinates if no path is found

    # Move drone along the path
    for waypoint in path:
        # Update drone's position
        longitude, latitude = waypoint
        print(f"📍 Moving to waypoint: {waypoint}")

        # Send the coordinates to the server
        send_coordinates(id, longitude, latitude, 'busy', SERVER_URL)

        # You can add a delay here if needed to simulate movement over time
        # time.sleep(some_delay_time)

    # After reaching the final destination, update the drone's status to 'idle'
    send_coordinates(id, path[-1][0], path[-1][1], 'idle', SERVER_URL)

    print(f"🧭 A* pathfinding from {current_coords} to {to_coords}")
    path = a_star(current_coords, to_coords)  # A* returns a path

    if path is None:
        print("❌ No valid path found.")
        return current_coords  # Return the original coordinates if no path is found

    # Move drone along the path
    for waypoint in path:
        # Update drone's position
        longitude, latitude = waypoint
        print(f"📍 Moving to waypoint: {waypoint}")

        # Send the coordinates to the server
        send_coordinates(id, longitude, latitude, 'busy', SERVER_URL)

        # You can add a delay here if needed to simulate movement over time
        # time.sleep(some_delay_time)

    # After reaching the final destination, update the drone's status to 'idle'
    send_coordinates(id, path[-1][0], path[-1][1], 'idle', SERVER_URL)
    
    return path[-1]  # Return final coordinates after reaching destination


# def run(id, current_coords, from_coords, to_coords, SERVER_URL):
#     drone_coords = current_coords
#     d_long, d_la =  getMovement(drone_coords, from_coords)
#     while ((from_coords[0] - drone_coords[0])**2 + (from_coords[1] - drone_coords[1])**2)*10**6 > 0.0002:
#         drone_coords = moveDrone(drone_coords, d_long, d_la)
#         #========================================= Added ==============================================================

#         if is_in_no_fly_zone(*drone_coords):
#             print("Drönaren riskerar att flyga in i no-fly-zone under färd mot 'from'. Justerar kurs...")
#             safe_coords = safe_direction2(*drone_coords)
#             if safe_coords == (None, None):
#                 print("Kunde inte hitta säker väg. Avbryter flygning.")
#                 return drone_coords[0],drone_coords[1]
#             drone_coords = safe_coords
#             continue  # Hoppa till nästa iteration med nya koordinater

#         #========================================================================================================
#         with requests.Session() as session:
#             drone_info = {'id': id,
#                           'longitude': drone_coords[0],
#                           'latitude': drone_coords[1],
#                           'status': 'busy'
#                         }
#             resp = session.post(SERVER_URL, json=drone_info)
#             print(f"Sending coordinates: {drone_coords[0]}, {drone_coords[1]}")
#     d_long, d_la =  getMovement(drone_coords, to_coords)
#     while ((to_coords[0] - drone_coords[0])**2 + (to_coords[1] - drone_coords[1])**2)*10**6 > 0.0002:
#         drone_coords = moveDrone(drone_coords, d_long, d_la)
#         #======================================= Added ================================================================

#         if is_in_no_fly_zone(*drone_coords):
#             print("Drönaren riskerar att flyga in i no-fly-zone under färd mot 'from'. Justerar kurs...")
#             safe_coords = safe_direction2(*drone_coords)
#             if safe_coords == (None, None):
#                 print("Kunde inte hitta säker väg. Avbryter flygning.")
#                 return drone_coords[0],drone_coords[1]
#             drone_coords = safe_coords
#             continue  # Hoppa till nästa iteration med nya koordinater

#         #========================================================================================================
#         with requests.Session() as session:
#             drone_info = {'id': id,
#                           'longitude': drone_coords[0],
#                           'latitude': drone_coords[1],
#                           'status': 'busy'
#                         }
#             resp = session.post(SERVER_URL, json=drone_info)
#             print(f"Sending coordinates: {drone_coords[0]}, {drone_coords[1]}")
#     with requests.Session() as session:
#             drone_info = {'id': id,
#                           'longitude': drone_coords[0],
#                           'latitude': drone_coords[1],
#                           'status': 'idle'
#                          }
#             resp = session.post(SERVER_URL, json=drone_info)
#     return drone_coords[0], drone_coords[1]

#=====================================================================================================
def load_initial_coordinates(filename):
    """Load the initial coordinates from a file if it exists."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = f.read().strip()
            if data:
                longitude, latitude = map(float, data.split(','))
                logging.info("Successfully loaded initial drone location.")
                return longitude, latitude
    logging.info("None initial drone location loaded.")
    return None

def save_final_coordinates(filename, longitude,latitude):
    """ Save the final location to a file and if a file doesen't exist creates one """
    with open(filename, 'w') as f:
        f.write(f"{longitude},{latitude}")
        f.close()
    logging.info("Successfully save the final location.")


if __name__ == "__main__":
    # The IP address of server, in order to location of the drone to the SERVER
    SERVER_URL = "http://192.168.0.1:1338/drone"

    parser = argparse.ArgumentParser()
    parser.add_argument("--clong", help='current longitude of drone location' ,type=float)
    parser.add_argument("--clat", help='current latitude of drone location',type=float)
    parser.add_argument("--flong", help='longitude of input [from address]',type=float)
    parser.add_argument("--flat", help='latitude of input [from address]' ,type=float)
    parser.add_argument("--tlong", help ='longitude of input [to address]' ,type=float)
    parser.add_argument("--tlat", help ='latitude of input [to address]' ,type=float)
    parser.add_argument("--id", help ='drones ID' ,type=str)
    args = parser.parse_args()

    # Assign a unique file name for every drone.
    COORDS_FILE = f"{args.id}.txt"

    logging.debug(f"Created {COORDS_FILE}.")

    # Load initial coordinates from file or use provided ones
    initial_coords = load_initial_coordinates(COORDS_FILE)
    if initial_coords:
        current_coords = initial_coords
    else:
        if args.clong is None or args.clat is None:
            raise ValueError("Initial coordinates not found in file or provided as arguments.")
        current_coords = (args.clong, args.clat)


    from_coords = (args.flong, args.flat)
    to_coords = (args.tlong, args.tlat)

    #======================================= Added ================================================

    # if is_in_no_fly_zone(current_coords[0], current_coords[1]):
    #     print("Drönaren är i no-fly-zon. Försöker hitta säker plats...")
    #     new_coords = safe_direction2(current_coords[0], current_coords[1])
    #     if new_coords == (None, None):
    #         print("Kunde inte hitta säker plats. Avslutar.")
    #         sys.exit(1)
    #     current_coords = new_coords
    #     print(f"Flyttade till säker plats: {current_coords}")
    

    #===========================================================================================

    print(current_coords, from_coords, to_coords)
    drone_long, drone_lat = run(args.id ,current_coords, from_coords, to_coords, SERVER_URL)

     # Save the final location to the file
    save_final_coordinates(COORDS_FILE, drone_long, drone_lat)
    logging.info(f"Drone's final coordinates saved: {drone_long}, {drone_lat}")
    print("Task is done!")
    # drone_long and drone_lat is the final location when drlivery is completed, find a way save the value, and use it for the initial coordinates of next delivery
    #=============================================================================
