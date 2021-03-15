#!/usr/bin/python3
import sys
import RPi.GPIO as GPIO
from scale import Scale
import time
from statistics import mean

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


scale = Scale()

scale.setReferenceUnit(1)

scale.reset()
scale.tare()

scale.setReferenceUnit(Calibration(scale))

while True:

    try:
        val = scale.getMeasure()
        print("{0: 4.4f}".format(val))

    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()
        sys.exit()
