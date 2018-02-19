import os.path
import subprocess
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from CurrentTemperature import InsideTemperature

class CurrentTemperatureLibrary(object):

    def __init__(self):
      self._temp = InsideTemperature()
      
    def read_temperature(self):
      self._result = self._temp.value()
      
    def temperature_should_be(self, expected):
      if self._result != expected:
        raise AssertionError('%s != %s' % (self._result, expected))
