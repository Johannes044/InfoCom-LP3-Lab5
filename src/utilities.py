import random
# import initial_coords # type: ignore 
import datetime
import time

medeciner = ["Viagra", "Antidepp", "Alvedon", "Ipren", "Zovirax", "Gaviscon", "Halstabletter"]
leveranser = [{"d1": []},
              
{"d2": []},

{"d3": []},

{"d4": []}]

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
    toChords = randomCords()
    medecin = randomMedicin()
    bestämtKlockslag = False
    if (not bestämtKlockslag):
        droneName = ""
        KlockslagFramme = datetime.datetime.max
        KlockslagTbk = datetime.datetime.max 
        leverans = {
            'medecin': medecin,
            'coordinates': toChords,
            'drone': droneName,
            'KlockslagFramme': KlockslagFramme,
            'KlockslagTbk': KlockslagTbk
        }
        leveranser.append(leverans)  
    print (leveranser)
    
count = 0
while count <10:
    if isDelivery():
        newLeverans()
    time.sleep(1)  
    count +=1 