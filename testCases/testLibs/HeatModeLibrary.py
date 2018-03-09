import os.path
import subprocess
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from HeatMode import HeatMode
import RPi.GPIO as GPIO

MINUS = 24
PLUS = 23

class HeatModeLibrary(object):

    def __init__(self):
        self._heat = HeatMode(outPlusWaveform=PLUS, outMinusWaveform=MINUS) 
        # DO not run this test suite on actual HW, or change these number to actual one
        #self._heat = HeatMode(23,24)

    def set_mode_to_confort(self):
        self._heat.setConfortMode()
	
    def output_plus_should_be(self, expected):
        self._output_X_should_be( PLUS, expected)
        
    def output_minus_should_be(self, expected):
        self._output_X_should_be( MINUS, expected)
        
    def set_mode_to_confort_minus_one(self):
        self._heat.setConfortMinus1()
        
    def set_mode_to_confort_minus_two(self):
        self._heat.setConfortMinus2()     
        
    def set_mode_to_custom_ratio(self, ratio):
        self._heat.setConfortRatio(ratio)

        
    def _output_X_should_be(self, output, expected):
        """ verifie que la sortie soit au niveau attendu HIGH ou LOW"""
        level = { "HIGH":GPIO.HIGH, "LOW":GPIO.LOW}[expected]
        actual = GPIO.input(output)
        if actual != level:
            raise AssertionError('%s != %s' % (actual, expected))
