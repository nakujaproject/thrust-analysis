import sys
import time
from statistics import mean
from datetime import datetime

import RPi.GPIO as GPIO
from hx711 import HX711

from drive import uploadToDrive

import threadedPlot as plts
import matplotlib.pyplot as plt

import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def Calibration(hx, offset):
    readings = []
    print("Load Reference weight")
    time.sleep(2)
    print("Calibrating")
    for _ in range(5):
        print(".")
        readings.append(hx.getWeight())
        time.sleep(1)
        
    print(readings)
    
    refWeight = float(input("Input reference weight: "))

    print((mean(readings) - offset)/refWeight)
    return (mean(readings) - offset)/refWeight

filename = datetime.now().strftime("%A %d %B %Y %I-%M%p") + ".csv"
#f = open(filename, "a")
#print("File Created")

# choose pins on rpi (BCM5 and BCM6)
hx = HX711(dout=5, pd_sck=6)

hx.setReferenceUnit(1)

hx.reset()
hx.tare()

offset = hx.getWeight()

hx.setReferenceUnit(Calibration(hx, offset))

#show sample readings
for _ in range(20):
    print(hx.getWeight())

qs = input("Continue with readings: (y/n)")
if (qs == "y"):
    # get, display and write data
    data = plts.MyDataClass()
    plotter = plts.MyPlotClass(data)
    fetcher = plts.MyDataFetchClass(data, hx, filename)

    fetcher.start()
    plt.show()

    #f.close()
    uploadToDrive(filename)
else:
    #f.close()
    os.remove(filename)
    print("file deleted")

GPIO.cleanup()
print("Done")
sys.exit()