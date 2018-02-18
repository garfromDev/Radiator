import os.path
import subprocess
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from HeatMode import HeatMode
import RPi.GPIO as GPIO

MINUS = 24
PLUS = 23

class HeatModeLibrary(object):

    def __init__(self):
        self._sut_path = os.path.join(os.path.dirname(__file__),
                                      '..',  'HeatMode.py')
        #self._heat = HeatMode(outPlusWaveForm=PLUS, outMinusWaveForm=MINUS) 
	self._heat = HeatMode(23,24)
        self._status = ''

    def set_mode_to_confort(self):
        # DO not run this test suite on actual HW, or change these number to actual one
	self._heat.setConfortMode()
	
    def output_plus_should_be(self, expected):
	""" verifie que la sortie soit au niveau attendu """
        level = { "HIGH":GPIO.HIGH, "LOW":GPIO.LOW}[expected]
	actual = GPIO.input(PLUS)
	if actual != level:
	    raise AssertionError('%s != %s' % (actual, expected))
