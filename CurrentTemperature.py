# -*- coding: utf-8 -*-
# inspired of example from Tony DiCola, License: Public Domain

import Adafruit_MCP3008
import spidev

# this object get the inside ambiant temperature from the sensor connected to the SPI adc
# it can be used with FilteredVar mechanism, using value() as getter

class InsideTemperature:
# sensorPin : the pin of the MPC3008 where the sensor is connected (pin 5 in my schematic)
# voltageRef : the reference voltage of the ADC, in mV (295mV in my schematic)
# adcRange : the output range of ADC converter (0 to 1023 for MCP3008)
# sensorGain : the voltage change per degrees of the thermal sensor (10 mV / degree for LM35)
    def __init__(self, sensorPin = 5, voltageRef = 295,adcRange = 1024, sensorGain = 10 ):
        self._sensorPin = sensorPin
        self._voltageRef = voltageRef
        self._adcRange = adcRange
        self._sensorGain = sensorGain
        #init SPI connexion
        SPI_PORT   = 0
        SPI_DEVICE = 0
        self._mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# return the temperature value in degree, None if impossible to calculate
# with my schematic, temperature range is 0 to 29,5 degree Celcius
# higher temperature will be 29.5, this is not a concern for a heating regulation
    def value(self):
        voltage = _mcp.read_adc(_sensorPin)
        try:
            temp = float(voltage) * (_voltageRef / _adcRange) / _sensorGain
        except:
            temp = None

        return temp

