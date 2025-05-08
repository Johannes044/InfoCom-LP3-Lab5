from flask import Flask, render_template, request, jsonify, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import redis
import json
import os
import sys
import random
import math
import logging
file = "../Logs/build.txt"
#import sys
sys.path.append(os.path.abspath(".."))
from logic.utilities import clearFile

# Konfigurera Flask och Redis
app = Flask(__name__)
CORS(app)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
redis_server = redis.Redis(host='localhost', port=6379, decode_responses=True, charset="unicode_escape")

# Konfigurera loggning
logging.basicConfig(filename=file,level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

clearFile(file)

def translate(coords_osm):
    x_osm_lim = (13.143390664, 13.257501336)
    y_osm_lim = (55.678138854000004, 55.734680845999996)
    x_svg_lim = (212.155699, 968.644301)
    y_svg_lim = (103.68, 768.96)
    
    x_ratio = (x_svg_lim[1] - x_svg_lim[0]) / (x_osm_lim[1] - x_osm_lim[0])
    y_ratio = (y_svg_lim[1] - y_svg_lim[0]) / (y_osm_lim[1] - y_osm_lim[0])
    x_svg = x_ratio * (coords_osm[0] - x_osm_lim[0]) + x_svg_lim[0]
    y_svg = y_ratio * (y_osm_lim[1] - coords_osm[1]) + y_svg_lim[0]
    return x_svg, y_svg

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')
    
@app.route('/map', methods=['POST'])
def map():
    drone_id = request.values.get("drone-id").strip()  # Drönar-id från input
    drone_ids = redis_server.smembers("drones")  # Alla faktiska drönar-idn
    if request.method == "POST":
        print(request.values.get("tracking-number"))
        if drone_id not in drone_ids:
            return redirect("/")
    return render_template('map.html', drone_id=drone_id)
    

    

    

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route('/get_drones', methods=['GET'])
# Fetching drone data
def get_drones():
    drone_dict = {}
    drones = redis_server.smembers("drones")
    print(drones)
    for drone in drones:
        droneData = redis_server.hgetall(drone)
        if 'longitude' in droneData and 'latitude' in droneData and 'status' in droneData:
            longitude_svg, latitude_svg = translate((float(droneData['longitude']), float(droneData['latitude'])))
            drone_dict[drone] = {'longitude': longitude_svg, 'latitude': latitude_svg, 'status': droneData['status']}
    logging.debug(f"Drones fetched: {drone_dict}")
    return jsonify(drone_dict)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='1337')
