# -*- coding: utf-8 -*-

import FilteredVar
import 

# this object get the inside ambiant temperature from the sensor

class InsideTemperature
# sensorPin : the pin of the MPC3008 where the sensor is connected
# voltageRef : the reference volatage of the ADC

    def __init__(self, sensorPin, voltageRef):
        self._sensorPin = sensorPin
        self._voltageRef = voltageRef
        #init SPI connexion

    def value(self)
        voltage = adc_read(_sensorPin)

