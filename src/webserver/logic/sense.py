from sense_hat import SenseHat
sense = SenseHat()


# Define some colours
g = (0, 255, 0) # Green
b = (0, 0, 0) # Black
r = (255, 0, 0)

# Set up where each colour will display
creeper_pixels = [
    g, g, g, g, g, g, g, g,
    g, g, g, g, g, g, g, g,
    g, b, b, g, g, b, b, g,
    g, b, b, g, g, b, b, g,
    g, g, g, b, b, g, g, g,
    g, g, b, b, b, b, g, g,
    g, g, b, b, b, b, g, g,
    g, g, b, g, g, b, g, g
]

X_pixels = [
    b, r, r, r, r, r, r, b,
    r, b, r, r, r, r, b, r,
    r, r, b, r, r, b, r, r,
    r, r, r, b, b, r, r, r,
    r, r, r, b, b, r, r, r,
    r, r, b, r, r, b, r, r,
    r, b, r, r, r, r, b, r,
    b, r, r, r, r, r, r, b
]
O_pixels = [
    g, g, g, b, b, g, g, g,
    g, g, b, g, g, b, g, g,
    g, b, g, g, g, g, b, g,
    b, g, g, g, g, g, g, b,
    b, g, g, g, g, g, g, b,
    g, b, g, g, g, g, b, g,
    g, g, b, g, g, b, g, g,
    g, g, g, b, b, g, g, g
]

# Display these colours on the LED matrix



def waitingForInput():
    print("Drone is waiting for QR-code. Press joystick to continue...")
    # Vänta på att användaren trycker på joystick
    event = sense.stick.wait_for_event()
    sense.set_pixels(X_pixels)
    while event.action != "pressed":
        event = sense.stick.wait_for_event()
    sense.set_pixels(O_pixels)
    print("Joystick pressed! Continuing to destination...")