import random
# import initial_coords.txt # type: ignore
import datetime
import time

import random
import datetime
import time

import random
import datetime

medeciner = ["Viagra", "Antidepp", "Alvedon", "Ipren", "Zovirax", "Gaviscon", "Halstabletter"]

leveranser = {
    'd1': [],
    'd2': [],
    'd3': [],
    'd4': []
}

def randomMedicin():
    return random.choice(medeciner)

def randomCords():
    latitude_min, latitude_max = 55.678, 55.734
    longitude_min, longitude_max = 13.143, 13.237
    latitude = random.uniform(latitude_min, latitude_max)
    longitude = random.uniform(longitude_min, longitude_max)
    return longitude, latitude

def isDelivery():
    return random.random() < 0.1

def newLeverans():
    toCords = randomCords()
    medecin = randomMedicin()
    current_time = datetime.datetime.now()
    estimated_delivery_time = current_time + datetime.timedelta(minutes=random.randint(10, 60)) 
    min_time_drone = min(leveranser, key=lambda drone: sum(
        [(delivery['KlockslagFramme'] - current_time).total_seconds() for delivery in leveranser[drone]]
    ) if leveranser[drone] else 0)  

    leverans = {
        'medecin': medecin,
        'coordinates': toCords,
        'KlockslagFramme': estimated_delivery_time
    }
    leveranser[min_time_drone].append(leverans)
    leveranser[min_time_drone].sort(key=lambda x: x['KlockslagFramme'])

def getDeliveryQueueForDrone(drone_name):
    return leveranser.get(drone_name, [])

def addDeliveryToDroneQueue(drone_name, delivery):
    leveranser[drone_name].append(delivery)
    leveranser[drone_name].sort(key=lambda x: x['KlockslagFramme'])
