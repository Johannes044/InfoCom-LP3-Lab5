from geopy.distance import geodesic
import datetime
import random
from flask import Flask, request, jsonify
import redis
import requests

app = Flask(__name__)
redis_server = redis.Redis(host='localhost', port=6379, decode_responses=True)

leveranser = {
    'd1': [],
    'd2': [],
    'd3': [],
    'd4': []
}

medeciner = ["Viagra", "Antidepp", "Alvedon", "Ipren", "Zovirax", "Gaviscon", "Halstabletter"]

def send_request(drone_url, coords):
    with requests.Session() as session:
        resp = session.post(drone_url, json=coords)

@app.route('/planner', methods=['POST'])
def route_planner():
    from_long, from_lat = random.uniform(13.143, 13.237), random.uniform(55.678, 55.734)
    to_long, to_lat = random.uniform(13.143, 13.237), random.uniform(55.678, 55.734)

    start_coords = (from_lat, from_long)
    end_coords = (to_lat, to_long)

    avstand_km = geodesic(start_coords, end_coords).km

    drone_speed_kmh = 50  
    tid_timmar = avstand_km / drone_speed_kmh
    tid_minuter = tid_timmar * 60

    drones = redis_server.smembers("drones")
    droneAvailable = None
    drone_name = ""
    for drone in drones:
        droneData = redis_server.hgetall(drone)
        if droneData['status'] == 'idle':
            droneAvailable = drone
            drone_name = droneData.get("name", "unknown")
            break

    if droneAvailable is None:
        return 'No available drone, try later'


    arrival_time = datetime.datetime.now() + datetime.timedelta(minutes=tid_minuter)
    return_time = arrival_time 

    medecin = random.choice(medeciner)

    leverans = {
        'medecin': medecin,
        'coordinates': end_coords,
        'KlockslagFramme': arrival_time,
        'KlockslagTbk': return_time
    }

    if drone_name not in leveranser:
        leveranser[drone_name] = []
    leveranser[drone_name].append(leverans)
    leveranser[drone_name].sort(key=lambda x: x['KlockslagFramme'])

    coords = {
        'from': (from_long, from_lat),
        'to': (to_long, to_lat),
        'current': (droneData['longitude'], droneData['latitude']),
        'distance_km': round(avstand_km, 2),
        'estimated_minutes': round(tid_minuter, 1)
    }

    DRONE_IP = redis_server.hget(droneAvailable, 'ip')
    DRONE_URL = f'http://{DRONE_IP}:5000'

    try:
        send_request(DRONE_URL, coords)
    except Exception as e:
        return "Could not connect to the drone"


    return jsonify({
        'message': 'Rutt tilldelad och leverans sparad',
        'drone': drone_name,
        'medecin': medecin,
        'arrival_time': arrival_time.strftime('%H:%M'),
        'return_time': return_time.strftime('%H:%M'),
        'distance_km': round(avstand_km, 2),
        'estimated_minutes': round(tid_minuter, 1)
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1339)
