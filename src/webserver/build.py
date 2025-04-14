from flask import Flask, render_template, request, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import redis
import json
import os
import sys
sys.path.append(os.path.abspath(".."))
from utilities import randomCords
import random
import math

app = Flask(__name__)
CORS(app)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

redis_server = redis.Redis(host='localhost', port=6379, decode_responses=True, charset="unicode_escape")

x_osm_lim = (13.143390664, 13.257501336)
y_osm_lim = (55.678138854000004, 55.734680845999996)
x_svg_lim = (212.155699, 968.644301)
y_svg_lim = (103.68, 768.96)

def randomCords():
    lon = random.uniform(*x_osm_lim)
    lat = random.uniform(*y_osm_lim)
    return (lon, lat)

coord1 = randomCords()
coord2 = randomCords()

def translate1(coords_osm):
    x_ratio = (x_svg_lim[1] - x_svg_lim[0]) / (x_osm_lim[1] - x_osm_lim[0])
    y_ratio = (y_svg_lim[1] - y_svg_lim[0]) / (y_osm_lim[1] - y_osm_lim[0])
    x_svg = x_ratio * (coords_osm[0] - x_osm_lim[0]) + x_svg_lim[0]
    y_svg = y_ratio * (y_osm_lim[1] - coords_osm[1]) + y_svg_lim[0]
    return x_svg, y_svg

svg1 = translate1(coord1)
svg2 = translate1(coord2)

def svgDistance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

distance_p = svgDistance(svg1, svg2)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')
    
@app.route('/map', methods=['GET', 'POST'])
def map():
    if request.method == "POST":
        print(request.values.get("tracking-number"))
    return render_template('map.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route('/get_drones', methods=['GET'])
def get_drones():
    drone_dict = {}
    drones = redis_server.smembers("drones")
    for drone in drones:
        droneData = redis_server.hgetall(drone)
        if 'longitude' in droneData and 'latitude' in droneData and 'status' in droneData:
            longitude_svg, latitude_svg = translate1((float(droneData['longitude']), float(droneData['latitude'])))
            drone_dict[drone] = {'longitude': longitude_svg, 'latitude': latitude_svg, 'status': droneData['status']}
    return jsonify(drone_dict)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='1337')
