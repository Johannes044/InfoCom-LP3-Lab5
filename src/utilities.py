import random
from sense_hat import SenseHat
sense = SenseHat()


def randomCords():
    latitude_min, latitude_max = 55.678, 55.734
    longitude_min, longitude_max = 13.143, 13.237
    latitude = random.uniform(latitude_min, latitude_max)
    longitude = random.uniform(longitude_min, longitude_max)
    return longitude, latitude

def isDelivery():
    return random.random()< 0.1








def waitingForInput():
    print("Drone is waiting at from_coords. Press joystick to continue...")
    # Vänta på att användaren trycker på joystick
    event = sense.stick.wait_for_event()
    while event.action != "pressed":
        event = sense.stick.wait_for_event()
    print("Joystick pressed! Continuing to destination...")


def clearFile(filename):
    with open(filename,'w') as file:
        pass