import sys
import os

# Lägg till pi-mappen i sys.path
sys.path.append(os.path.abspath("../pi"))

from drone import app  # Importera Flask-appen från drone.py
import requests

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
