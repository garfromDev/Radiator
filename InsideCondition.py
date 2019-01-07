# -*- coding: utf-8 -*-
# inspired of example from Tony DiCola, License: Public Domain

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import time
from CST import CST
import logging

CST.MAX_LIGHT_DELTA = 4 #max delta in percent between 2 measurement

class InsideTemperature:
    """
      get the inside light level from the sensor connected to the SPI adc
      it can be used with FilteredVar mechanism, using value() as getter 
    """  
# sensorPin : the pin of the MPC3008 where the sensor is connected (pin 1 in my schematic)
# voltageRef : the reference voltage of the ADC, in mV (581mV in my schematic)
# adcRange : the output range of ADC converter (0 to 1023 for MCP3008)
# sensorGain : the voltage change per degrees of the thermal sensor (10 mV / degree for LM35)
    def __init__(self, sensorPin = 1, voltageRef = 581.0,adcRange = 1024.0, sensorGain = 10.0 ):
        GPIO.setmode(GPIO.BCM)
        self._sensorPin = sensorPin
        self._voltageRef = voltageRef
        self._adcRange = adcRange
        self._sensorGain = sensorGain
        #init SPI connexion
        SPI_PORT   = 0
        SPI_DEVICE = 0
        self._mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# return the light value in percent , None if impossible to calculate
# with my schematic, light range is 0 to 100%
    def value(self):
        try:
            maxDelta= CST.MAX_LIGHT_DELTA * self._adcRange / 100
        except:
            maxDelta = self._adcRange #no filterig will be done
            
        voltage = self._filteredVoltage(maxDelta=maxDelta, measure = lambda :self._mcp.read_adc(self._sensorPin))
        try:
            light = int( (float(voltage)  / self._adcRange) * 100)
        except: #would fail if voltage=None or adcRange=0 
            light = None

        return light

    #--------- internal ---------------------------------------------------
    def _filteredVoltage(self, maxDelta, measure, interval = CST.LM35_INTERVAL):
        # perform 3 measurement at interval secondes delay using measure() and return the mean of the two closest value
        # or None if the 2 closest value are more than maxDelta apart
        # return None if measure() fails
        # this function is potentially reusable and could be refactored, except for the LM35_INTERVAl const
        # 
        t=[]
        for i in range(3):
            try:
                t.append(measure())
            except:
                return None
            time.sleep(interval)
            
        def m(a,b):
            return (a+b)/2
        def d(a,b):
            if a > b:
                return a - b
            return b - a
        
        # we look for the smallest difference bewteen two measurement 
        fv = sorted([ (d(t[0], t[1]),  m(t[0],t[1]) ) ,
              (d(t[0], t[2]),  m(t[0],t[2]) ),
              (d(t[1], t[2]),  m(t[1],t[2]) )
             ], key=lambda f:f[0])
        if fv[0][0] <maxDelta:
            return fv[0][1] # return the mean of two closest value
        return None         # if the value are two far apart, return None
        
            
if __name__ == '__main__':
    print("testing InsideTemperature manually")
    logging.basicConfig(filename='Radiator.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    test = InsideTemperature()
    print(test.value())            
