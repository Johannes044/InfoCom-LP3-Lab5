import random
from flask import Flask, render_template, request, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import redis
import json
import logging
file = "../Logs/build.txt"
#import sys
#import os
#sys.path.append(os.path.abspath(".."))
from logic.utilities import clearFile
from logic.No_fly_zone import safe_diraction

# Konfigurera Flask och Redis
app = Flask(__name__)
CORS(app)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
redis_server = redis.Redis(host='localhost', port=6379, decode_responses=True, charset="unicode_escape")

# Konfigurera loggning
logging.basicConfig(filename=file,level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

clearFile()

#===============================================================

def init_packages():
    medeciner = ["Viagra", "Antidepp", "Alvedon", "Ipren", "Zovirax", "Gaviscon", "Halstabletter"]
    drones = redis_server.smembers("drones")

    for drone_id in drones:
        # Undvik duplicering om redan finns
        if not redis_server.exists(f"packages:{drone_id}"):
            for i in range(3):  # Lägg till 3 random paket per drönare
                package = random.choice(medeciner)
                redis_server.rpush(f"packages:{drone_id}", package)

#=============================================================================

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
    
@app.route('/map', methods=['GET', 'POST'])
def map():
    if request.method == "POST":
        print(request.values.get("tracking-number"))

    return render_template('map.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

#=============================================================================

@app.route('/admin', methods=['GET'])
def admin():
    drone_ids = redis_server.smembers("drones")
    drones = []
    for drone_id in drone_ids:
        packages = redis_server.lrange(f"packages:{drone_id}", 0, -1)  # Redis list
        drones.append({"id": drone_id, "packages": packages})
    return render_template("admin.html", drones=drones)

# @app.route("/get_no_fly_zones", methods=["GET"])
# def get_no_fly_zones():
#     zones_svg = []
#     for zone in NO_FLY_ZONES:
#         x1, y1 = translate((zone["min_lon"], zone["max_lat"]))
#         x2,y2 = translate((zone["max_lon"], zone["min_lat"]))
#         width = abs(x2 - x1)
#         height = abs(y2 - y1)
#         zones_svg.append({"x": min(x1, x2), "y": min(y1, y2), "width": width, "height": height})
#     logging.debug(f"Sent {zones_svg} to draw the no fly zone.")
#     return jsonify(zones_svg)

@app.route("/get_package", methods=["GET"])
def get_package():
    medeciner = ["Viagra", "Antidepp", "Alvedon", "Ipren", "Zovirax", "Gaviscon", "Halstabletter"]
    drones = redis_server.smembers("drones")

    deliveries = {}
    for drone_id in drones:
        package = random.choice(medeciner)
        redis_server.set(f"delivery:{drone_id}", package)
        deliveries[drone_id] = package

    return jsonify(deliveries)

@app.route("/get_package/<drone_id>", methods=["GET"])
def get_package_for_drone(drone_id):
    package = redis_server.get(f"delivery:{drone_id}")
    if package:
        return jsonify({"drone_id": drone_id, "package": package})
    else:
        return jsonify({"error": "No package found"}), 404

#=================================================================================================

@app.route('/get_drones', methods=['GET'])
# Fetching drone data
def get_drones():
    drone_dict = {}
    drones = redis_server.smembers("drones")
    for drone in drones:
        droneData = redis_server.hgetall(drone)
        if 'longitude' in droneData and 'latitude' in droneData and 'status' in droneData:
            #========================================================================================================
            lon,lat = safe_diraction(float(droneData['longitude']), float(droneData['latitude']))
            longitude_svg, latitude_svg = translate((float(lon), float(lat)))
            #=========================================================================================================
            drone_dict[drone] = {'longitude': longitude_svg, 'latitude': latitude_svg, 'status': droneData['status']}
    logging.debug(f"Drones fetched: {drone_dict}")
    return jsonify(drone_dict)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='1337')
