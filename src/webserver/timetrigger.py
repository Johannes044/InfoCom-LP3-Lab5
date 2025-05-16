import time
import requests 

while True:
    time.sleep(5)
    with requests.Session() as session:
        resp = session.post("http://localhost/sender", {})
        print("hejsan hoppsan")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='1339')
