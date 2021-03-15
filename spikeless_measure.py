#!/usr/bin/python3
import sys
import RPi.GPIO as GPIO
from scale import Scale
import time
from statistics import mean
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

scale = Scale()

scale.setReferenceUnit(1)

scale.reset()
scale.tare()

scale.setReferenceUnit(Calibration(scale))
presses = 0
while True:

    try:
        val = scale.getMeasure()
        if (GPIO.input(18) == False):
            presses = presses + 1
        print("{0: 4.4f}".format(val))
        if(presses == 1):
            f = open(filename, "a")
            print("File Created")
        elif (presses == 2):
            f.write(str(val) + "\n")
        elif (presses > 2):
            f.close()

    except (KeyboardInterrupt, SystemExit):
        f.close()
        GPIO.cleanup()
        sys.exit()
