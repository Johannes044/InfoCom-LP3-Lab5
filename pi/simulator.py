import math
import requests
import argparse
import json
import os

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

def send_location(SERVER_URL, id, drone_coords, status):
    with requests.Session() as session:
        drone_info = {
            'id': id,
            'longitude': drone_coords[0],
            'latitude': drone_coords[1],
            'status': status
        }
        resp = session.post(SERVER_URL, json=drone_info)

def distance(_fr, _to):
    _dist = ((_to[0] - _fr[0])**2 + (_to[1] - _fr[1])**2)*10**6
    return _dist

def save_position(id, longitude, latitude):
    with open(f"{id}_position.json", "w") as file:
        json.dump({"longitude": longitude, "latitude": latitude}, file)

def load_position(id):
    if os.path.exists(f"{id}_position.json"):
        with open(f"{id}_position.json", "r") as file:
            data = json.load(file)
        return data["longitude"], data["latitude"]
    return None, None

def run(id, current_coords, from_coords, to_coords, SERVER_URL):
    drone_coords = current_coords

    d_long, d_la =  getMovement(drone_coords, from_coords)
    while distance(drone_coords, from_coords) > 0.0002:
        drone_coords = moveDrone(drone_coords, d_long, d_la)
        send_location(SERVER_URL, id=id, drone_coords=drone_coords, status='busy')
    
    send_location(SERVER_URL, id=id, drone_coords=drone_coords, status='waiting')
    
    d_long, d_la =  getMovement(drone_coords, to_coords)
    while distance(drone_coords, to_coords) > 0.0002:
        drone_coords = moveDrone(drone_coords, d_long, d_la)
        send_location(SERVER_URL, id=id, drone_coords=drone_coords, status='busy')
    
    send_location(SERVER_URL, id=id, drone_coords=drone_coords, status='idle')
    save_position(id, drone_coords[0], drone_coords[1])
    
    return drone_coords[0], drone_coords[1]
   
if __name__ == "__main__":
    SERVER_URL = "http://SERVER_IP:5001/drone"

    parser = argparse.ArgumentParser()
    parser.add_argument("--clong", help='current longitude of drone location' ,type=float)
    parser.add_argument("--clat", help='current latitude of drone location',type=float)
    parser.add_argument("--flong", help='longitude of input [from address]',type=float)
    parser.add_argument("--flat", help='latitude of input [from address]' ,type=float)
    parser.add_argument("--tlong", help ='longitude of input [to address]' ,type=float)
    parser.add_argument("--tlat", help ='latitude of input [to address]' ,type=float)
    parser.add_argument("--id", help ='drones ID' ,type=str)
    args = parser.parse_args()

    saved_long, saved_lat = load_position(args.id)
    if saved_long is not None and saved_lat is not None:
        current_coords = (saved_long, saved_lat)
    else:
        current_coords = (args.clong, args.clat)

    from_coords = (args.flong, args.flat)
    to_coords = (args.tlong, args.tlat)

    print("Get New Task!")

    drone_long, drone_lat = run(args.id ,current_coords, from_coords, to_coords, SERVER_URL)
    print(f"Delivery completed. New starting position: {drone_long}, {drone_lat}")


