import random
import datetime
import math

medeciner = ["Viagra", "Antidepp", "Alvedon", "Ipren", "Zovirax", "Gaviscon", "Halstabletter"]
leveranser = {
    "d1": [],
    "d2": [],
    "d3": [],
    "d4": []
}

x_osm_lim = (13.143390664, 13.257501336)
y_osm_lim = (55.678138854000004, 55.734680845999996)
x_svg_lim = (212.155699, 968.644301)
y_svg_lim = (103.68, 768.96)
lSpeed = 340 * 0.000009 

def randomMedicin():
    return random.choice(medeciner)

def randomCords():
    lon = random.uniform(*x_osm_lim)
    lat = random.uniform(*y_osm_lim)
    return (lon, lat)

def translateToSVG(coords_osm):
    x_ratio = (x_svg_lim[1] - x_svg_lim[0]) / (x_osm_lim[1] - x_osm_lim[0])
    y_ratio = (y_svg_lim[1] - y_svg_lim[0]) / (y_osm_lim[1] - y_osm_lim[0])
    x_svg = x_ratio * (coords_osm[0] - x_osm_lim[0]) + x_svg_lim[0]
    y_svg = y_ratio * (y_osm_lim[1] - coords_osm[1]) + y_svg_lim[0]
    return x_svg, y_svg

def translateToLon(svg_coords):
    x_svg, y_svg = svg_coords
    x_ratio = (x_svg_lim[1] - x_svg_lim[0]) / (x_osm_lim[1] - x_osm_lim[0])
    y_ratio = (y_svg_lim[1] - y_svg_lim[0]) / (y_osm_lim[1] - y_osm_lim[0])
    lon = (x_svg - x_svg_lim[0]) / x_ratio + x_osm_lim[0]
    lat = y_osm_lim[1] - ((y_svg - y_svg_lim[0]) / y_ratio)
    return (lon, lat)
 
def svgSpeed():
    speed = 340 * 0.000009 
    x_ratio = (x_svg_lim[1] - x_svg_lim[0]) / (x_osm_lim[1] - x_osm_lim[0])
    y_ratio = (y_svg_lim[1] - y_svg_lim[0]) / (y_osm_lim[1] - y_osm_lim[0])
    speed_svg_x = speed * x_ratio
    speed_svg_y = speed * y_ratio
    return speed_svg_x, speed_svg_y

def svgDistance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def isDelivery():
    return random.random() < 0.1

def getTime(fromCoords, toCoords):
    return

def newLeverans():
    toCoords = randomCords()
    medecin = randomMedicin()
    svg_start = translateToSVG((13.2, 55.7))
    svg_end = translateToSVG(toCoords)
    dist = svgDistance(svg_start, svg_end)
    speed_x, speed_y = svgSpeed()
    total_speed = math.sqrt(speed_x**2 + speed_y**2)  
    flygtid = datetime.timedelta(seconds=dist / total_speed)
    

    chosen_drone = None
    klockslagtbk = datetime.time.max
    klockslagframme = datetime.time.max
    for drone in leveranser.items():
        if (not drone):
            klockslagframmeNy = datetime.datetime.now() + flygtid           
        else:
            klockslagframmeNy = leveranser[drone][-1]['KlockslagTbk'] + flygtid
        if (klockslagframmeNy < klockslagframme):
            klockslagframme = klockslagframmeNy
            klockslagtbk = klockslagframme + flygtid
            chosen_drone = drone    
    leveranser[drone].append({
        'medecin': medecin,
        'coordinates': toCoords,
        'drone': chosen_drone,
        'KlockslagFramme': klockslagframme,
        'KlockslagTbk': klockslagtbk})
    
    """
    droneName = findLeastBusyDrone()

    now = datetime.datetime.now()
    leverans = {
        'medecin': medecin,
        'coordinates': toCoords,
        'drone': droneName,
        'KlockslagFramme': now + flygtid,
        'KlockslagTbk': now + flygtid * 2
    }
    leveranser[droneName].append(leverans)
    
    print(f"Ny leverans till {droneName}: {leverans}")
    """

if isDelivery():
    newLeverans()
