import time
import math
import requests
import argparse
import logging
file = "../Logs/simulator.txt"
import sys
import os
from algoritmen import a_star
sys.path.append(os.path.abspath(".."))
delay = 50/1000
from webserver.logic.utilities import clearFile
from webserver.route_planner import leveranser, newLeverans

logging.basicConfig(filename=file,level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

clearFile(file)

def getMovement(currentDroneCoords, dst, lSpeed):
    dst_x, dst_y = dst
    x, y = currentDroneCoords
    distance = math.sqrt((dst_x - x)**2 + (dst_y - y)**2)

    print(f"Distance: {distance}, Speed: {lSpeed}")  # Utskrift för att se distansen

    if distance == 0:
        return 0, 0
    
    dx = dst_x - x
    dy = dst_y - y
    unit_dx = dx / distance  
    unit_dy = dy / distance  
    longitude_move = unit_dx * lSpeed
    latitude_move = unit_dy * lSpeed

    print(f"Movement: {longitude_move}, {latitude_move}")  # Utskrift för att se rörelsen per iteration

    return longitude_move, latitude_move


def moveDrone(src, d_long, d_la, dt):
    x, y = src
    x = x + d_long * dt
    y = y + d_la * dt
    return x, y

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
def interpolate(a, b, steps=10):
    dx = (b[0] - a[0]) / steps
    dy = (b[1] - a[1]) / steps
    return [(a[0] + i * dx, a[1] + i * dy) for i in range(1, steps + 1)]

def run(id, current_coords, from_coords, to_coords, SERVER_URL):
    targets = [from_coords, to_coords]
    final_position = current_coords

    for target in targets:
        print(f" Planning path from {current_coords} to {target}")
        path = a_star(current_coords, target)

        if not path:
            print(f" No valid path found from {current_coords} to {target}")
            return current_coords[0], current_coords[1]

        # Smooth start if needed
        if path[0] != current_coords:
            for point in interpolate(current_coords, path[0], steps=10):
                send_coordinates(id, point[0], point[1], 'busy', SERVER_URL)
                time.sleep(0.1)
            current_coords = path[0]

        # Interpolate each segment
        for i in range(len(path) - 1):
            for point in interpolate(path[i], path[i + 1], steps=5):
                send_coordinates(id, point[0], point[1], 'busy', SERVER_URL)
                time.sleep(0.1)
            current_coords = path[i + 1]

        # Mark arrival
        send_coordinates(id, current_coords[0], current_coords[1], 'idle', SERVER_URL)
        final_position = current_coords

    print(f" Final destination reached: {final_position}")
    return final_position[0], final_position[1]




#=====================================================================================================
def load_initial_coordinates(filename):
    """Load the initial coordinates from a file if it exists."""
    if os.path.exists(filename):  # Fuck filen, helt ärligt!
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
    # SERVER_URL = "http://192.168.0.1:1338/drone"
    SERVER_URL = "http://127.0.0.1:1338/drone"

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

    print(current_coords, from_coords, to_coords)
    drone_long, drone_lat = run(args.id ,current_coords, from_coords, to_coords, SERVER_URL)

     # Save the final location to the file
    save_final_coordinates(COORDS_FILE, drone_long, drone_lat)
    logging.info(f"Drone's final coordinates saved: {drone_long}, {drone_lat}")
    print("Task is done!")
    # drone_long and drone_lat is the final location when drlivery is completed, find a way save the value, and use it for the initial coordinates of next delivery
    #=============================================================================
