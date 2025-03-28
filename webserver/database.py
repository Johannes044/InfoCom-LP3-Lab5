from flask import Flask, request
from flask_cors import CORS
import redis
import json

app = Flask(__name__)
CORS(app)

redis_server = redis.Redis(host='localhost', port=6379, decode_responses=True, charset="unicode_escape")

@app.route('/drone', methods=['POST'])
def drone():
    drone = request.get_json()
    droneIP = request.remote_addr
    droneID = drone['id']
    drone_longitude = drone['longitude']
    drone_latitude = drone['latitude']
    drone_status = drone['status']
    
    drones = redis_server.smembers('drones')
    if droneID not in drones:
        redis_server.sadd('drones', droneID)
    
    droneDATA = {'ip': droneIP, 'longitude': drone_longitude, 'latitude': drone_latitude, 'status': drone_status}
    redis_server.hset(droneID, mapping=droneDATA)
    
    return 'Get data'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5001')