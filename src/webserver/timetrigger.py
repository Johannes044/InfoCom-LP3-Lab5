import time
import requests 

n = 1
while True:
    time.sleep(1)
    with requests.Session() as session:
        resp = session.post("http://localhost:1339/sender", {})
    print(n)
    n += 1

