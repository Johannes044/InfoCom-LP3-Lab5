import requests
import json

DRONE_URL = "http://localhost:5000"

def test_drone_receives_request():
    test_payload = {
        "from": [13.2, 55.7],
        "to": [13.3, 55.8]
    }
    response = requests.post(DRONE_URL, json=test_payload)
    assert response.status_code == 200, "❌ Drönaren svarar inte korrekt"
    print("✅ Drönaren tog emot förfrågan")

if __name__ == "__main__":
    test_drone_receives_request()
