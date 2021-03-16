import sys
import time
from statistics import mean
from datetime import datetime

import RPi.GPIO as GPIO
from hx711 import HX711

from drive import uploadToDrive

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

presses = 0
while True:

    try:
        val = hx.getWeight()
        if (GPIO.input(18) == False):
            presses = presses + 1
        print("{0: 4.4f}".format(val))
        if (presses == 1):
            f.write(str(val) + "\n")
        elif (presses > 1):
            f.close()

    except (KeyboardInterrupt, SystemExit):
        f.close()
        uploadToDrive(filename)
        GPIO.cleanup()
        sys.exit()
