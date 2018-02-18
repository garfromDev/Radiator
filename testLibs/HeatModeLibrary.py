import os.path
import subprocess
import sys
import HeatMode
import RPi.GPIO as GPIO

class HeatModeLibrary(object):
    PLUS = 23
    MINUS = 24

    def __init__(self):
        self._sut_path = os.path.join(os.path.dirname(__file__),
                                      '..',  'HeatMode.py')
        self._heat = HeatMode() 
        self._status = ''

    def set_mode_to_confort(self):
        # DO not run this test suite on actual HW, or change these number to actual one
	self._heat.setConfortMode(outPlusWaveForm=PLUS, outMinusWaveForm=MINUS)
	
    def output_plus_should_be(self, expected):
	""" vérifie que la sortie soit au niveau attendu
        level = [ "HIGH":GPIO.HIGH, "LOW":GPIO.LOW][expected]
	actual = GPIO.input(PLUS)
	if actual != level:
	    raise AssertionError('%s != %s' % (actual, expected))	
