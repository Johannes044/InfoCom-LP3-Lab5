from flask import Flask, request
from flask_cors import CORS
import redis
import json


app = Flask(__name__)
CORS(app)

# change this to connect to your redis server
# ===============================================
redis_server = redis.Redis("localhost", decode_responses=True, charset="unicode_escape")
# ===============================================

@app.route('/drone', methods=['POST'])
def drone():
    drone = request.get_json() #* Tar emot en json packet från drönaren.
    drone_IP = request.remote_addr #* Hämtar dränarens IP.
    drone_ID = drone['id']
    drone_longitude = drone['longitude']
    drone_latitude = drone['latitude']
    drone_status = drone['status']
    # Get the infomation of the drone in the request, and update the information in Redis database
    # Data that need to be stored in the database: 
    # Drone ID, logitude of the drone, latitude of the drone, drone's IP address, the status of the drone
    # Note that you need to store the metioned infomation for all drones in Redis, think carefully how to store them
    # =========================================================================================

    #* Sätter upp drönar information i ett Dictionarie (nyckel-värde par).
    drone_data = {
        "id": drone_ID,
        "longitude": drone_longitude,
        "latitude": drone_latitude,
        "ip_address": drone_IP,
        "status": drone_status
    }

    #* 
    redis_server.set(drone_ID, json.dumps(drone_data))


    # =======================================================================================
    return "Drone data updated successfully", 200

if __name__ == "__main__":


    app.run(debug=True, host='0.0.0.0', port='5001')
