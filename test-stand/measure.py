import sys
import time
from statistics import mean
from datetime import datetime

import RPi.GPIO as GPIO
from hx711 import HX711

from drive import uploadToDrive

import liveplt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

def Calibration(hx):
    readings = []
    print("Load Reference weight")
    time.sleep(2)
    print("Calibating")
    for _ in range(5):
        print(".")
        readings.append(hx.getWeight())
        time.sleep(1)
        
    print(readings)
    
    refWeight = float(input("Input reference weight: "))

    return mean(readings)/refWeight

filename = datetime.now().strftime("%A %d %B %Y %I-%M%p") + ".csv"
f = open(filename, "a")
print("File Created")

# choose pins on rpi (BCM5 and BCM6)
hx = HX711(dout=5, pd_sck=6)

hx.setReferenceUnit(1)

hx.reset()
hx.tare()


hx.setReferenceUnit(Calibration(hx))

while True:

    try:
        # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(fig, liveplt.animate, fargs=(xs, ys, ax, hx, f), interval=100)
        plt.show()

    except (KeyboardInterrupt, SystemExit):
        f.close()
        uploadToDrive(filename)
        GPIO.cleanup()
        print("Done")
        sys.exit()
