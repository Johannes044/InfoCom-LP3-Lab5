import random
import datetime
from utilities import newLeverans, getDeliveryQueueForDrone


def print_leveranser():
    for drone in ['d1', 'd2', 'd3', 'd4']:
        queue = getDeliveryQueueForDrone(drone)
        print(f"Leveranser för {drone}:")
        for leverans in queue:
            print(f"  Medicin: {leverans['medecin']}, Tid: {leverans['KlockslagFramme'].strftime('%H:%M:%S')}")
        print("\n")

def test_new_leveranser(num_leveranser):
    for _ in range(num_leveranser):
        newLeverans()
        print_leveranser()

if __name__ == "__main__":
    test_new_leveranser(10)
