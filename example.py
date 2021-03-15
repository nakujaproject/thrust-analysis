import sys
import time
from statistics import mean

import RPi.GPIO as GPIO
from hx711 import HX711

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

# choose pins on rpi (BCM5 and BCM6)
hx = HX711(dout=5, pd_sck=6)

hx.setReferenceUnit(1)

hx.reset()
hx.tare()

hx.setReferenceUnit(Calibration(hx))
while True:

    try:
        val = hx.getWeight()
        print("{0: 4.4f}".format(val))

    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()
        sys.exit()
