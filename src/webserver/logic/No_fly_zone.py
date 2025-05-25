##dig project
#import logging
#file = "../Logs/NOfly.txt"

# Konfigurera loggning
#logging.basicConfig(filename=file,level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

#! added a new zone with is mitt in long: 55.71742, lat: 13.22948;


NO_FLY_ZONES = [
    {
        "min_lon": 13.182460,
        "max_lon": 13.214460,
        "min_lat": 55.702952,
        "max_lat": 55.720952
    },
    {
        "min_lon": 13.197878,
        "max_lon": 13.229878,
        "min_lat": 55.708623,
        "max_lat": 55.726623
    }
]

def halve_zone(zone):
    center_lon = (zone["min_lon"] + zone["max_lon"]) / 2
    center_lat = (zone["min_lat"] + zone["max_lat"]) / 2

    half_width = (zone["max_lon"] - zone["min_lon"]) / 4
    half_height = (zone["max_lat"] - zone["min_lat"]) / 4

    return [{
        "min_lon": center_lon - half_width,
        "max_lon": center_lon + half_width,
        "min_lat": center_lat - half_height,
        "max_lat": center_lat + half_height
    }]

def is_not_in_zone(coord):
    zones_once = [z for zone in NO_FLY_ZONES for z in halve_zone(zone)]
    zones_twice = [z for zone in zones_once for z in halve_zone(zone)]
    for zone in zones_twice:
        if zone["min_lon"] <=  coord[0]<= zone["max_lon"] and zone["min_lat"] <= coord[1] <= zone["max_lat"]:
            return False  # Drönaren är i en förbjuden zon
    return True

def is_in_no_fly_zone(lon, lat):
    zones_once = [z for zone in NO_FLY_ZONES for z in halve_zone(zone)]
    zones_twice = [z for zone in zones_once for z in halve_zone(zone)]
    for zone in zones_twice:
        if zone["min_lon"] <= lon <= zone["max_lon"] and zone["min_lat"] <= lat <= zone["max_lat"]:
            return True
    return False

def safe_diraction(lon, lat, step_size_lon = 0.0005, step_size_lat=0.0005):
    """Hittar en säker position genom att flytta drönaren utanför no-fly-zonen"""
    original_lon, original_lat = lon, lat
    attempts = 0

    while is_in_no_fly_zone(lon, lat) and attempts < 100:
        lon += step_size_lon  # Flytta österut
        lat += step_size_lat  # Flytta norrut
        attempts += 1

    print(f"Från ({original_lon}, {original_lat}) -> Till ({lon}, {lat}) efter {attempts} försök")
    return lon, lat

def safe_direction2(lon, lat, step_size=0.0005, max_attempts=100):
    original_lon, original_lat = lon, lat
    attempts = 0
    directions = [
        (step_size, 0), (-step_size, 0), (0, step_size), (0, -step_size),
        (step_size, step_size), (-step_size, step_size),
        (step_size, -step_size), (-step_size, -step_size)
    ]
    while is_in_no_fly_zone(lon, lat) and attempts < max_attempts:
       dx, dy = directions[attempts % len(directions)]
       test_lon = original_lon + dx
       test_lat = original_lat + dy
       if not is_in_no_fly_zone(test_lon, test_lat):
        return test_lon, test_lat
       attempts += 1

    print(f"Från ({original_lon}, {original_lat}) -> Till ({lon}, {lat}) efter {attempts} försök")

    if is_in_no_fly_zone(lon, lat):
        print("Kunde inte hitta en säker position.")
        return None, None

    return lon, lat
