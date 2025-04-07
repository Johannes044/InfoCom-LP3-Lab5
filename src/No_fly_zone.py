##dig project
import logging
file = "../Logs/NOfly.txt"

# Konfigurera loggning
logging.basicConfig(filename=file,level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


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

def is_in_no_fly_zone(lon, lat):
    for zone in NO_FLY_ZONES:
        if zone["min_lon"] <= lon <= zone["max_lon"] and zone["min_lat"] <= lat <= zone["max_lat"]:
            return True  # Drönaren är i en förbjuden zon
    return False

def safe_diraction(lon, lat, step_size_lon = 0.0005, step_size_lat=0.0005):
    """Hittar en säker position genom att flytta drönaren utanför no-fly-zonen"""
    original_lon, original_lat = lon, lat
    new_lon,new_lat =0,0
    attempts = 0

    while is_in_no_fly_zone(lon, lat) and attempts < 100:
        lon += step_size_lon  # Flytta österut
        lat += step_size_lat  # Flytta norrut
        attempts += 1

    new_lon,new_lat =lon,lat
    
    if not is_in_no_fly_zone(new_lon, new_lat):
        print("Could move out drone")

    print(f"Från ({original_lon}, {original_lat}) -> Till ({lon}, {lat}) efter {attempts} försök")
    return lon, lat


print(is_in_no_fly_zone(13.197878,55.708623))


def test_find_safe_position():
    # Testfall 1: Position utanför no-fly-zon (ska inte ändras)
    lon, lat = 13.2500, 55.7200  # Utanför no-fly-zoner
    safe_lon, safe_lat = safe_diraction(lon, lat, 0.0005, 0.0005)
    assert (safe_lon, safe_lat) == (lon, lat), f"Fel! Förväntat ({lon}, {lat}), fick ({safe_lon}, {safe_lat})"
    
    # Testfall 2: Position inuti en no-fly-zon (ska flyttas)
    lon, lat = 13.2050, 55.7050  # Inom en definierad no-fly-zon
    safe_lon, safe_lat = safe_diraction(lon, lat, 0.0005, 0.0005)
    assert not is_in_no_fly_zone(safe_lon, safe_lat), f"Fel! Positionen ({safe_lon}, {safe_lat}) är fortfarande inom no-fly-zonen"

    # Testfall 3: Position precis på gränsen till en no-fly-zon (ska flyttas)
    lon, lat = 13.2100, 55.7100  # Precis på gränsen
    safe_lon, safe_lat = safe_diraction(lon, lat, 0.0005, 0.0005)
    assert not is_in_no_fly_zone(safe_lon, safe_lat), f"Fel! Positionen ({safe_lon}, {safe_lat}) är fortfarande inom no-fly-zonen"

    print("Alla testfall har klarat sig! ✅")

# Kör testet
test_find_safe_position()
