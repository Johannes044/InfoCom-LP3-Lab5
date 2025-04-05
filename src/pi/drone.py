from flask import Flask, request
from flask_cors import CORS
import subprocess
import  requests
import logging
file = "../Logs/drone.txt"
import sys
import os
sys.path.append(os.path.abspath(".."))
from utilities import clearFile

# Konfigurera Flask och Redis
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

# Konfigurera loggning
logging.basicConfig(filename=file,level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

clearFile(file)

# Assign a unique ID to the drone
myID = "D69"


# Store the initial drone position
drone_state = {
    "current_longitude": 13.2,
    "current_latitude": 55.7
}
#* lth's position i long, lati
#longitude = 13.21008
#latitude = 55.71106

#* Drone information dictionary
drone_info = {'id': myID,
              'longitude': drone_state['current_longitude'],
              'latitude': drone_state['current_latitude'],
              'status': 'idle'
             }

# Define the server address
SERVER="http://192.168.0.1:1338/drone"
# Send initial location to server with error handling
try:
    with requests.Session() as session:
        resp = session.post(SERVER, json=drone_info)
        resp.raise_for_status()
        logging.info("Successfully sent initial drone location to server.")
        app.logger.info("Successfully sent initial drone location to server.")
except requests.RequestException as e:
    logging.error(f"Error sending initial location to server: {e}")
    app.logger.error(f"Error sending initial location to server: {e}")
#===================================================================

@app.route('/', methods=['POST'])
def main():
    """
    Handles route updates for the drone.
    """
    coords = request.json
    app.logger.info(f"Received new route: {coords}")
    logging.info(f"Received new route: {coords}")

    from_coord = coords['from']
    to_coord = coords['to']

    # Fetch current longitude and latitude of the drone
    current_longitude = drone_state['current_longitude']
    current_latitude = drone_state['current_latitude']

    logging.debug(f"Moving from {from_coord} to {to_coord}")
    app.logger.debug(f"Moving from {from_coord} to {to_coord}")
    
    # Run the simulator process
    subprocess.Popen(["python3", "simulator.py", '--clong', str(current_longitude), '--clat', str(current_latitude),
                                                 '--flong', str(from_coord[0]), '--flat', str(from_coord[1]),
                                                 '--tlong', str(to_coord[0]), '--tlat', str(to_coord[1]),
                                                 '--id', myID
                    ])
    
    # Update drone state
    drone_state['longitude'] = to_coord[0]
    drone_state['latitude'] = to_coord[1]
    drone_state['status'] = 'busy'

    logging.info(f"Drone {myID} now moving to {to_coord}. Status updated to 'busy'.")
    app.logger.info(f"Drone {myID} now moving to {to_coord}. Status updated to 'busy'.")
    return 'New route received'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
