import time
import requests 

while True:
    time.sleep(5)
    with requests.Session() as session:
        resp = session.post("http://localhost/sender", {})
        print("hejsan hoppsan")
