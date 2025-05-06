from cmath import pi
from flask import Flask, request, render_template, jsonify
from flask.globals import current_app
from geopy.geocoders import Nominatim
from flask_cors import CORS
import sys
import os
#sys.path.append(os.path.abspath(".."))
import redis
import json
import requests 
import logging
file = "../Logs/route_planner.txt"
from logic.utilities import clearFile, coords


# Konfigurera Flask och Redis
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
redis_server = redis.Redis(host='localhost', port=6379, decode_responses=True)

coords = coords
# Konfigurera loggning och geolocator
logging.basicConfig(filename=file,level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

clearFile(file)

geolocator = Nominatim(user_agent="my_request")
region = ", Lund, Skåne, Sweden"

def send_request(drone_url, coords):
    print(coords)
    with requests.Session() as session:
        resp = session.post(drone_url, json=coords)
        print(resp)

@app.route('/planner', methods=['POST'])
def route_planner():
    Addresses = json.loads(request.data.decode())
    FromAddress = Addresses['faddr']
    ToAddress = Addresses['taddr']
    from_location = geolocator.geocode(FromAddress + region, timeout=None)
    to_location = geolocator.geocode(ToAddress + region, timeout=None)
    
    if from_location is None:
        logging.error("Departure from_address not found, please input a correct address")
        return 'Departure from_address not found, please input a correct address'
    elif to_location is None:
        logging.error('Destination to_address not found, please input a correct address')
        return 'Destination to_address not found, please input a correct address'
    
    coords = {'from': (from_location.longitude, from_location.latitude),
              'to': (to_location.longitude, to_location.latitude)}
    if from_location is None:
       return 'Departure address not found, please input a correct address'
    
   
    drones = redis_server.smembers("drones")
    droneAvailable = None
    for drone in drones:
        droneData = redis_server.hgetall(drone)
        logging.debug(f"Drone data from {droneData['id']} have been access!")
        if droneData['status'] == 'idle':
            droneAvailable = drone
            coords['current'] = (droneData['longitude'], droneData['latitude'])
            break
    
    if droneAvailable is None:
        return 'No available drone, try later'
    
    DRONE_IP = redis_server.hget(droneAvailable, 'ip')
    DRONE_URL = f'http://{DRONE_IP}:42069'
    send_request(DRONE_URL, coords)
    logging.debug('Got address and sent request to the drone')
    return 'Got address and sent request to the drone'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='1339')
