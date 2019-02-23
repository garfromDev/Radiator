# -*- coding: utf-8 -*-
# inspired of example from Tony DiCola, License: Public Domain
import logging
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO

from CST import CST

CST.MAX_LIGHT_DELTA = 4 #max delta in percent between 2 measurement
CST.SUN = "SUN"
CST.LOWSUN = "LOWSUN"
CST.SUN_NONE = "NONE"
CST.SUN_PERCENT_THRESHOLD = 80
CST.LOWSUN_PERCENT_THRESHOLD = 60

class InsideCondition:
    """
      get the inside light level and temperature from the sensor connected to the SPI adc
      it can be used with FilteredVar mechanism, using value() as getter 
    """
# sensorPin : the pin of the MPC3008 where the sensor is connected (pin 1 in my schematic)
# voltageRef : the reference voltage of the ADC, in mV (581mV in my schematic)
# adcRange : the output range of ADC converter (0 to 1023 for MCP3008)
# sensorGain : the voltage change per degrees of the thermal sensor (10 mV / degree for LM35)
    def __init__(self, ThSensorPin = 1, voltageRef = 581.0,adcRange = 1024.0, thSensorGain = 10.0, lightSensorPin = 3):
        GPIO.setmode(GPIO.BCM)
        self._sensorPin = ThSensorPin
        self._lightSensorPin = lightSensorPin
        self._voltageRef = voltageRef
        self._adcRange = adcRange
        self._sensorGain = thSensorGain
        #init SPI connexion
        SPI_PORT   = 0
        SPI_DEVICE = 0
        self._mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


    def light(self):
        """
            :return: the light value in percent , None if impossible to calculate
            with my schematic, light range is 0 to 100%
            0% means no light
        """"
        try:
            maxDelta= CST.MAX_LIGHT_DELTA * self._adcRange / 100
        except:
            maxDelta = self._adcRange #no filterig will be done

        voltage = self._filteredVoltage(maxDelta=maxDelta, measure = lambda :self._mcp.read_adc(self._lightSensorPin))
        try:
            light = 100 - int( (float(voltage)  / self._adcRange) * 100)
        except: #would fail if voltage=None or adcRange=0 
            light = None

        return light

    
    def light_condition(self):
        """
            :return: the light condition SUN, LOWSUN, NONE , NONE if impossible to calculate
        """"
        light_percent = self.light()
        if light_percent > CST.SUN_PERCENT_THRESHOLD:
            return CST.SUN
        if light_percent > CST.LOWSUN_PERCENT_THRESHOLD:
            return CST.LOWSUN
        return CST.SUN_NONE
    
    
# return the temperature value in degree, None if impossible to calculate
# with my schematic, temperature range is 0 to 58,1 degree Celcius
# higher temperature will be 58,1, this is not a concern for a heating regulation
    def temperature(self):
        try: #calculate the adc delta value corresponding to MAX_DELTA_TEMP temperature delta in °
            degree = CST.MAX_DELTA_TEMP * self._sensorGain * self._adcRange / self._voltageRef
        except:
            degree = self._adcRange #no filterig will be done
        voltage = self._filteredVoltage(maxDelta=degree, measure = lambda :self._mcp.read_adc(self._sensorPin))
        try:
            temp = float(voltage) * (self._voltageRef / self._adcRange) / self._sensorGain
        except: #would fail if voltage=None or adcRange=0 or sensorGain=0
            temp = None

        return temp
    
    
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
    print("testing InsideCondition manually")
    test = InsideCondition()
    print(test.temperature())
    print(test.light())
    print(test.light_condition())
