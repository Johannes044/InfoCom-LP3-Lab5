from cmath import pi
from flask import Flask, request, render_template, jsonify
from flask.globals import current_app
from geopy.geocoders import Nominatim
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.abspath(".."))
import utilities 
import random
import redis
import json
import requests 


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
#55.7, 13.2
redis_server = redis.Redis(host='localhost', port=6379, decode_responses=True)

coords = utilities.coords

geolocator = Nominatim(user_agent="my_request")
region = ", Lund, Skåne, Sweden"

def send_request(drone_url, coords):
    print(coords)
    with requests.Session() as session:
        resp = session.post(drone_url, json=coords)
        print(resp)

@app.route('/planner', methods=['POST'])
def route_planner():
    
   
    drones = redis_server.smembers("drones")
    droneAvailable = None
    for drone in drones:
        droneData = redis_server.hgetall(drone)
        if droneData['status'] == 'idle':
            droneAvailable = drone
            coords['current'] = (droneData['longitude'], droneData['latitude'])
            break
    
    if droneAvailable is None:
        return 'No available drone, try later'
    
    DRONE_IP = redis_server.hget(droneAvailable, 'ip')
    DRONE_URL = f'http://{DRONE_IP}:5000'

    try:
        send_request(DRONE_URL, coords)
        with requests.Session() as session:
            resp = session.post(DRONE_URL, json=coords)
            print(resp.text)
    except Exception as e:
        print(e)
        return "Could not connect to the drone, please try again" 


    return 'Got address and sent request to the drone'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1339)