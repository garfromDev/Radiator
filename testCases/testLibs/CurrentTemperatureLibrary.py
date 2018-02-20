import os.path
import subprocess
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from CurrentTemperature import InsideTemperature

class CurrentTemperatureLibrary(object):
    """
    Allows to test CurrentTemperature.py with robot framework
    """
    def __init__(self):
      self._inside = InsideTemperature()
      
    def read_temperature(self):
      self._result = self._inside.value()
      
    def temperature_should_be(self, expected):
      if (float(self._result) - float(expected)) > 0.1:
        raise AssertionError('%s != %s' % (self._result, expected))
        
    class SimAdc(object):
        """ Definition d'un mock-up MCP """
        def __init__(self, targetInsideTemp, temp):
            """ :param targetInsideTemp: the InsideTemperature object that is tested """
            self._temp= float(temp) #to ensure float calculation
            self._target = targetInsideTemp
            
        def read_adc(self, pin):
            """ Return the voltage value corresponding to the temperature given in parameter,
                using hw parameter from _target (InsideTemperature object)
            """
            trg = self._target
            print('SimAdc.read_adc will return %s' % (self._temp * (trg._adcRange / trg._voltageRef) * trg._sensorGain))
            return self._temp * (trg._adcRange / trg._voltageRef) * trg._sensorGain
        
    def simulate_temperature(self, temp):
        """ Remplace l'objet mcp de la librairie MCP3008 par un fake SimAdc qui expose la meme methode
            and return the voltage value corresponding to the temperature given in parameter
        """
        self._inside._mcp = CurrentTemperatureLibrary.SimAdc(self._inside, temp)
            
