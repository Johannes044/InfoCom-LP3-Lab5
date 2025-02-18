import pytest
import requests
import redis
import json

# Konfigurera Redis
redis_server = redis.Redis(host="REDIS_SERVER", port=6379, decode_responses=True)

def test_redis_connection():
    assert redis_server.ping() == True, "Redis-anslutning misslyckades"

def test_store_drone_data():
    test_data = {"id": "TEST_DRONE", "longitude": 13.2, "latitude": 55.7, "status": "idle"}
    redis_server.set("TEST_DRONE", json.dumps(test_data))
    stored_data = json.loads(redis_server.get("TEST_DRONE"))
    assert stored_data == test_data, "Felaktiga data i Redis!"

def test_drone_receives_request():
    DRONE_URL = "http://localhost:5000"
    test_payload = {"from": [13.2, 55.7], "to": [13.3, 55.8]}
    response = requests.post(DRONE_URL, json=test_payload)
    assert response.status_code == 200, "Drönaren svarar inte korrekt"

def test_route_planner():
    ROUTE_PLANNER_URL = "http://localhost:5002/planner"
    payload = {"faddr": "Scheelevägen 22, Lund", "taddr": "Kungsgatan 2, Lund"}
    response = requests.post(ROUTE_PLANNER_URL, json=payload)
    assert response.status_code == 200, "Route Planner misslyckades"

if __name__ == "__main__":
    pytest.main()
