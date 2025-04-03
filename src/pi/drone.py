from flask import Flask, request
from flask_cors import CORS
import subprocess
import  requests


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'


#Give a unique ID for the drone
#===================================================================
myID = "DRONE_ID"
#===================================================================

# Get initial longitude and latitude the drone
#===================================================================
drone_state = {
    "current_longitude": 13.2,
    "current_latitude": 55.7
}
#* lth's position i long, lati
#longitude = 13.21008
#latitude = 55.71106
#===================================================================
#* Sätter upp drönar information i ett Dictionarie (nyckel-värde par).
drone_info = {'id': myID,
              'longitude': drone_state['current_longitude'],
              'latitude': drone_state['current_latitude'],
              'status': 'idle'
             }

# Fill in the IP address of server, and send the initial location of the drone to the SERVER
#===================================================================
SERVER="http://192.168.0.1:1338/drone"
#* error handling when sending to server.
try:
    with requests.Session() as session:
        resp = session.post(SERVER, json=drone_info)
        resp.raise_for_status()
        app.logger.info("Successfully sent initial drone location to server.")
except requests.RequestException as e:
    app.logger.error(f"Error sending initial location to server: {e}")
#===================================================================

@app.route('/', methods=['POST'])
def main():
    coords = request.json
    app.logger.info(f"Received new route: {coords}")

    from_coord = coords['from']
    to_coord = coords['to']

    # Get current longitude and latitude of the drone 
    #===================================================================
    current_longitude = drone_state['current_longitude']
    current_latitude = drone_state['current_latitude']
    #===================================================================
    
    subprocess.Popen(["python3", "simulator.py", '--clong', str(current_longitude), '--clat', str(current_latitude),
                                                 '--flong', str(from_coord[0]), '--flat', str(from_coord[1]),
                                                 '--tlong', str(to_coord[0]), '--tlat', str(to_coord[1]),
                                                 '--id', myID
                    ])
    drone_state['longitude'] = to_coord[0]
    drone_state['latitude'] = to_coord[1]
    drone_state['status'] = 'busy'
    return 'New route received'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
