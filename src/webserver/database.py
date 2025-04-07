from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import logging
file = "../Logs/database.txt"
import sys
import os
sys.path.append(os.path.abspath(".."))
#from utilities import clearFile

# Konfigurera Flask och Redis
app = Flask(__name__)
CORS(app)
redis_server = redis.Redis(host='localhost', port=6379, decode_responses=True, charset="unicode_escape")

# Konfigurera loggning
logging.basicConfig(filename=file,level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

#clearFile(file)

@app.route('/drone', methods=['POST'])
def drone():
    """
    Tar emot data från en drönare och lagrar den i Redis.
    """
    try:
        # Hämta JSON-data från drönaren
        drone = request.get_json()
        print(drone, "sadasdas")
        logging.debug(f"Incoming data: {drone}")
        
        # Kontrollera om nödvändiga fält finns
        #required_keys = {'id', 'longitude', 'latitude', 'status'}
        #if not required_keys.issubset(drone):
            #return jsonify({'error': 'Missing required fields'}), 400

        # Hämta data från förfrågan
        drone_id = drone['id']
        drone_ip = request.remote_addr
        drone_longitude = drone['longitude']
        drone_latitude = drone['latitude']
        drone_status = drone['status']

        # Lägg till drönaren i Redis om den inte redan finns
        if not redis_server.sismember('drones', drone_id):
            redis_server.sadd('drones', drone_id)
            logging.info(f"New drone registrerad: {drone_id}")

        logging.info(f"Drone {drone_id} report from {drone_ip}")

        # Spara drönardata i Redis
        drone_data = {
            'id': drone_id,
            'ip': drone_ip,
            'longitude': drone_longitude,
            'latitude': drone_latitude,
            'status': drone_status
        }
        redis_server.hset(drone_id, mapping=drone_data)
        logging.debug(f"Data save for {drone_id}: {drone_data}")

        return jsonify({'message': 'Drone data stored successfully'}), 200
    
    except Exception as e:
        logging.error(f"Något gick fel: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__": 
    app.run(debug=True, host='0.0.0.0', port=1338)
