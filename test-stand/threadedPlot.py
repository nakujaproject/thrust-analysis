import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import threading

import time
import datetime as dt
import sys
import RPi.GPIO as GPIO


class MyDataClass():

    def __init__(self):

        self.XData = [0]
        self.YData = [0]


class MyPlotClass():

    def __init__(self, dataClass):

        self._dataClass = dataClass

        self.hLine, = plt.plot(0, 0)

        self.ani = FuncAnimation(plt.gcf(), self.run, interval = 500, repeat=False)


    def run(self, i):  
        print("plotting data")
        self._dataClass.XData = self._dataClass.XData[-160:]
        self._dataClass.YData = self._dataClass.YData[-160:]
        self.hLine.set_data(self._dataClass.XData, self._dataClass.YData)
        self.hLine.axes.relim()
        self.hLine.axes.autoscale_view()


class MyDataFetchClass(threading.Thread):

    def __init__(self, dataClass, hx, filename):

        threading.Thread.__init__(self)

        self._dataClass = dataClass
        self._period = 0.0125
        self._hx = hx
        self._filename = filename
        #self._nextCall = time.time()


    def run(self):
        allPoints = []
        while (GPIO.input(18) == True):
            print("updating data")
            # add data to data class
            self._dataClass.XData.append(self._dataClass.XData[-1] + 1)
            val = self._hx.getWeight()
            self._dataClass.YData.append(val)
            allPoints.append(val)
            self._f.write(str(val) + "\n")
            # sleep until next execution
            #self._nextCall = self._nextCall + self._period;
            #time.sleep(self._nextCall - time.time())
            time.sleep(self._period)

        np.savetxt(self._filename, a, newline=" ")

#fetcher.join()