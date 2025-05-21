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
import logic.utilities 


import random
#from sense_hat import SenseHat
#sense = SenseHat()
import datetime
import math

medeciner = ["Viagra", "Antidepp", "Alvedon", "Ipren", "Zovirax", "Gaviscon", "Halstabletter"]
leveranser = []

x_osm_lim = (13.143390664, 13.257501336)
y_osm_lim = (55.678138854000004, 55.734680845999996)
x_svg_lim = (212.155699, 968.644301)
y_svg_lim = (103.68, 768.96)
lSpeed = 340 * 0.000009 

def randomMedicin():
    return random.choice(medeciner)


def translateToSVG(coords_osm):
    x_ratio = (x_svg_lim[1] - x_svg_lim[0]) / (x_osm_lim[1] - x_osm_lim[0])
    y_ratio = (y_svg_lim[1] - y_svg_lim[0]) / (y_osm_lim[1] - y_osm_lim[0])
    x_svg = x_ratio * (coords_osm[0] - x_osm_lim[0]) + x_svg_lim[0]
    y_svg = y_ratio * (y_osm_lim[1] - coords_osm[1]) + y_svg_lim[0]
    return x_svg, y_svg

def translateToLon(svg_coords):
    x_svg, y_svg = svg_coords
    x_ratio = (x_svg_lim[1] - x_svg_lim[0]) / (x_osm_lim[1] - x_osm_lim[0])
    y_ratio = (y_svg_lim[1] - y_svg_lim[0]) / (y_osm_lim[1] - y_osm_lim[0])
    lon = (x_svg - x_svg_lim[0]) / x_ratio + x_osm_lim[0]
    lat = y_osm_lim[1] - ((y_svg - y_svg_lim[0]) / y_ratio)
    return (lon, lat)
 
def svgSpeed():
    speed = 340 * 0.000009 
    x_ratio = (x_svg_lim[1] - x_svg_lim[0]) / (x_osm_lim[1] - x_osm_lim[0])
    y_ratio = (y_svg_lim[1] - y_svg_lim[0]) / (y_osm_lim[1] - y_osm_lim[0])
    speed_svg_x = speed * x_ratio
    speed_svg_y = speed * y_ratio
    return speed_svg_x, speed_svg_y

def svgDistance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def newLeverans(toCoords):
    medecin = randomMedicin()
    return {'medicin': medecin, 'coords': toCoords}



# Konfigurera Flask och Redis
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
redis_server = redis.Redis(host='localhost', port=6379, decode_responses=True)


# Konfigurera loggning och geolocator
logging.basicConfig(filename=file,level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

#clearFile(file)

geolocator = Nominatim(user_agent="my_request")
region = ", Lund, Skåne, Sweden"

def send_request(drone_url, coords):
    print(f"{drone_url} med{coords}")
    with requests.Session() as session:
        resp = session.post(drone_url, json=coords)
        print(resp)

@app.route('/sender', methods=['POST'])
def sendDrone():
    if (leveranser):
        drones = redis_server.smembers("drones")
        droneAvailable = None
        for drone in drones:
            droneData = redis_server.hgetall(drone)
            logging.debug(f"Drone data from {droneData['id']} have been access!")
            if droneData['status'] == 'idle':
                droneAvailable = drone
                coords = leveranser[0]['coords'].copy()
                coords['current'] = (droneData['longitude'], droneData['latitude'])
                break
        
        if droneAvailable is None:
            return 'No available drone, try later'
        
        DRONE_IP = redis_server.hget(droneAvailable, 'ip')
        DRONE_URL = f'http://{DRONE_IP}:5000'
        send_request(DRONE_URL, leveranser[0]['coords'])
        del leveranser[0]
        logging.debug('Got address and sent request to the drone')
        return 'Got address and sent request to the drone'
    return 'empty'


@app.route('/planner', methods=['POST'])
def route_planner():
    Addresses = json.loads(request.data.decode())
    FromAddress = "Mårtenstorget 12" #Addresses['faddr']
    ToAddress = Addresses['taddr']
    print(Addresses['taddr'])
    from_location = geolocator.geocode(FromAddress + region, timeout=None)
    to_location = geolocator.geocode(ToAddress + region, timeout=None)
    
    if from_location is None:
        logging.error("Departure from_address not found, please input a correct address")
        return 'Departure from_address not found, please input a correct address'
    if to_location is None:
        logging.error('Destination to_address not found, please input a correct address')
        return 'Destination to_address not found, please input a correct address'
    
    else:   
        coords = {
            'from': (from_location.longitude, from_location.latitude),
            'to': (to_location.longitude, to_location.latitude)
        }
        leverans = newLeverans(coords)
        leveranser.append(leverans)
        return 'vi har kordinator'


    
   
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='1339')
