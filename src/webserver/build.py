from flask import Flask, render_template, request, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import redis
import json
import os
import sys
sys.path.append(os.path.abspath(".."))
import utilities
import random
import math

app = Flask(__name__)
CORS(app)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

redis_server = redis.Redis(host='localhost', port=6379, decode_responses=True, charset="unicode_escape")

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
            longitude_svg, latitude_svg = utilities.translate1((float(droneData['longitude']), float(droneData['latitude'])))
            drone_dict[drone] = {'longitude': longitude_svg, 'latitude': latitude_svg, 'status': droneData['status']}
    return jsonify(drone_dict)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='1337')
