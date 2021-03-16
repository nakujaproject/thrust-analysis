#!/usr/bin/python3
import sys
import RPi.GPIO as GPIO
from scale import Scale
import time
from statistics import mean
from datetime import datetime
from drive import uploadToDrive
import liveplt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

def Calibration(scale):
    readings = []
    print("Load Reference weight")
    time.sleep(2)
    print("Calibating")
    for _ in range(5):
        print(".")
        readings.append(scale.getMeasure())
        time.sleep(1)
        
    print(readings)
    
    refWeight = float(input("Input reference weight: "))

    return mean(readings)/refWeight

filename = datetime.now().strftime("%A %d %B %Y %I-%M%p") + ".csv"
f = open(filename, "a")
print("File Created")


scale = Scale()

scale.setReferenceUnit(1)

scale.reset()
scale.tare()

scale.setReferenceUnit(Calibration(scale))

while True:

    try:
        # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(fig, liveplt.animate, fargs=(xs, ys, ax, scale, f), interval=1000)
        plt.show()
        

    except (KeyboardInterrupt, SystemExit):
        f.close()
        uploadToDrive(filename)
        GPIO.cleanup()
        print("Done")
        sys.exit()
