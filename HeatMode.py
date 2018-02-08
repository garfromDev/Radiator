# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

# This module alow to drive pilot wire
class HeatMode:
    
    # outPlusWaveform :
    # The GPIO output that drive the first OptoTriac (in GPIO.BCM notation)
    # this output supress negative waveform
    # outMinusWaveform :
    # The GPIO output that drive the second OptoTriac (in GPIO.BCM notation)
    # this output supress positive waveform
    def __init__(self, outPlusWaveform, outMinusWaveform):
        self._outPlusWaveform = outPlusWaveform
        self._outMinusWaveform = outMinusWaveform

    # Must be called once prior to use to initialize HW setting
    def hwInit(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(_outPlusWaveform, GPIO.OUT)
        GPIO.setup(_outMinusWaveform, GPIO.OUT)
        self.initDone = True


 
