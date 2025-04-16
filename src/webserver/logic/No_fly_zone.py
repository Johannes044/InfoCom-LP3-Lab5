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
    attempts = 0

    while is_in_no_fly_zone(lon, lat) and attempts < 100:
        lon += step_size_lon  # Flytta österut
        lat += step_size_lat  # Flytta norrut
        attempts += 1

    print(f"Från ({original_lon}, {original_lat}) -> Till ({lon}, {lat}) efter {attempts} försök")
    return lon, lat

def safe_direction2(lon, lat, step_size=0.0005, max_attempts=100):
    """Försöker hitta en säker riktning att ta sig ut ur no-fly-zonen."""
    original_lon, original_lat = lon, lat
    attempts = 0

    # Testa olika riktningar: (Δlon, Δlat)
    directions = [
        (step_size, 0),     # öst
        (-step_size, 0),    # väst
        (0, step_size),     # norr
        (0, -step_size),    # syd
        (step_size, step_size),     # nordost
        (-step_size, step_size),    # nordväst
        (step_size, -step_size),    # sydost
        (-step_size, -step_size),   # sydväst
    ]

    while is_in_no_fly_zone(lon, lat) and attempts < max_attempts:
        dx, dy = directions[attempts % len(directions)]
        lon += dx
        lat += dy
        attempts += 1

    print(f"Från ({original_lon}, {original_lat}) -> Till ({lon}, {lat}) efter {attempts} försök")

    if is_in_no_fly_zone(lon, lat):
        print("Kunde inte hitta en säker position utanför no-fly-zonen.")
        return None, None

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

def test_your_position(lon,lat):
    return is_in_no_fly_zone(lon, lat)
    


# Kör testet
test_find_safe_position()
