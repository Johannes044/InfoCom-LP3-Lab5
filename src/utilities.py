import random
# import initial_coords # type: ignore 
import datetime
import time
import math

medeciner = ["Viagra", "Antidepp", "Alvedon", "Ipren", "Zovirax", "Gaviscon", "Halstabletter"]
leveranser = [{"d1": []},
              
{"d2": []},

{"d3": []},

{"d4": []}]

x_osm_lim = (13.143390664, 13.257501336)
y_osm_lim = (55.678138854000004, 55.734680845999996)
x_svg_lim = (212.155699, 968.644301)
y_svg_lim = (103.68, 768.96)

def randomMedicin():
    return random.choice(medeciner)

def randomCords():
    lon = random.uniform(*x_osm_lim)
    lat = random.uniform(*y_osm_lim)
    return (lon, lat)


def isDelivery():
    return random.random() < 0.1



to = randomCords()
fron = (55.7, 13.2)



def translate(coords_osm):
    lon,lat = coords_osm
    
    x_ratio = (x_svg_lim[1] - x_svg_lim[0]) / (x_osm_lim[1] - x_osm_lim[0])
    y_ratio = (y_svg_lim[1] - y_svg_lim[0]) / (y_osm_lim[1] - y_osm_lim[0])
    x_svg = x_ratio * (coords_osm[0] - x_osm_lim[0]) + x_svg_lim[0]
    y_svg = y_ratio * (y_osm_lim[1] - coords_osm[1]) + y_svg_lim[0]
    return x_svg, y_svg

coord1 = randomCords()
coord2 = randomCords()

svg1 = translate(coord1)
svg2 = translate(coord2)

def svgDistance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

distance_p = svgDistance(svg1, svg2)







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

   # print (leveranser)


while False:
    if isDelivery():
        newLeverans()
    time.sleep(1)  
    