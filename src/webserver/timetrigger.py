import time
import requests 

while True:
    time.sleep(5)
    with requests.Session() as session:
        resp = session.post("http://localhost:1339/sender", {})
        print("hejsan hoppsan")

