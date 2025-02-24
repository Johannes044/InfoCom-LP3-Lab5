import pytest
import requests
import redis
import json
import time

# Ange URL:er för API:erna
DRONE_URL = "http://localhost:5000"
ROUTE_PLANNER_URL = "http://localhost:5002/planner"
BUILD_URL = "http://localhost:5000/get_drones"

# Konfigurera Redis-server
redis_server = redis.Redis(host="REDIS_SERVER", port=6379, decode_responses=True)

def test_redis_connection():
    """Testa att Redis är tillgängligt."""
    assert redis_server.ping(), "❌ Redis-anslutning misslyckades"
    print("✅ Redis är anslutet")

def test_store_drone_data():
    """Testa att spara och hämta drönardata i Redis."""
    test_data = {"id": "TEST_DRONE", "longitude": 13.2, "latitude": 55.7, "status": "idle"}
    redis_server.set("TEST_DRONE", json.dumps(test_data))
    stored_data = json.loads(redis_server.get("TEST_DRONE"))
    assert stored_data == test_data, "❌ Felaktiga data i Redis!"
    print("✅ Drönardata sparas korrekt i Redis")

def test_drone_receives_request():
    """Testa att drönaren tar emot en leveransförfrågan."""
    test_payload = {"from": [13.2, 55.7], "to": [13.3, 55.8]}
    response = requests.post(DRONE_URL, json=test_payload)
    assert response.status_code == 200, "❌ Drönaren svarar inte korrekt"
    print("✅ Drönaren tog emot en leveransförfrågan")

def test_route_planner():
    """Testa att Route Planner hittar en ledig drönare."""
    payload = {"faddr": "Scheelevägen 22, Lund", "taddr": "Kungsgatan 2, Lund"}
    response = requests.post(ROUTE_PLANNER_URL, json=payload)
    assert response.status_code == 200, "❌ Route Planner misslyckades"
    print("✅ Route Planner skickade en leveransförfrågan")

def test_build_get_drones():
    """Testa att kartan kan hämta drönardata från webservern."""
    response = requests.get(BUILD_URL)
    assert response.status_code == 200, "❌ Kunde inte hämta drönardata"
    data = response.json()
    assert isinstance(data, dict), "❌ Ogiltigt JSON-format från build.py"
    print("✅ Build.py returnerar drönardata korrekt")

if __name__ == "__main__":
    print("🚀 Startar systemtest...")
    test_redis_connection()
    test_store_drone_data()
    test_drone_receives_request()
    test_route_planner()
    test_build_get_drones()
    print("✅ **Alla systemtester klara!** 🎉")

