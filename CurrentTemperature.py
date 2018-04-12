# -*- coding: utf-8 -*-
# inspired of example from Tony DiCola, License: Public Domain

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# this object get the inside ambiant temperature from the sensor connected to the SPI adc
# it can be used with FilteredVar mechanism, using value() as getter

class InsideTemperature:
# sensorPin : the pin of the MPC3008 where the sensor is connected (pin 1 in my schematic)
# voltageRef : the reference voltage of the ADC, in mV (581mV in my schematic)
# adcRange : the output range of ADC converter (0 to 1023 for MCP3008)
# sensorGain : the voltage change per degrees of the thermal sensor (10 mV / degree for LM35)
    def __init__(self, sensorPin = 1, voltageRef = 581.0,adcRange = 1024.0, sensorGain = 10.0 ):
        self._sensorPin = sensorPin
        self._voltageRef = voltageRef
        self._adcRange = adcRange
        self._sensorGain = sensorGain
        #init SPI connexion
        SPI_PORT   = 0
        SPI_DEVICE = 0
        self._mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# return the temperature value in degree, None if impossible to calculate
# with my schematic, temperature range is 0 to 58,1 degree Celcius
# higher temperature will be 58,1, this is not a concern for a heating regulation
    def value(self):
        try: #calculate the adc delta value corresponding to MAX_DELTA_TEMP temperature delta in °
            degree = CST.MAX_DELTA_TEMP * self._sensorGain * self._adcRange / 
        except:
            degree = self._adcRange #no filterig will be done
        voltage = self._mcp.read_adc(self._sensorPin)
        try:
            temp = float(voltage) * (self._voltageRef / self._adcRange) / self._sensorGain
        except:
            temp = None

        return temp

    def _filteredVoltage(self):
        # mesure 3 valeurs
        # calcule dans un tableau les écarts D(1,2), D(1,3), D(2,3) et le smoyennes M(1,2)...
        # tri le tableau par ordre croissant et retourne la première moyenne
