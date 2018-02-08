# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

# This module alow to drive pilot wire
class HeatMode:
    hwNotInitializedError = ValueError('pilot wire optotriac hw control not initialized before calling setmode')
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

    # set the Triac control output to parameters value    
    # raise exception ValueError if hw has not been initialized
    def _setOutputs(self, plus, minus):
        if ! self.initDone:
            raise hwNotInitializedError
        GPIO.output(self._outPlusWaveform, plus)
        GPIO.output(self._outMinusWaveform, minus)
        
    # Set the pilot wire to confort mode = no sinusoid    
    def setConfortMode(self):
        self._setOutputs( plus = GPIO.LOW, minus = GPIO.LOW)
        
    # concept a developper pour le mode +& et -1
    # une file rotative contient les durée et les modes
    # on met le premier mode, et on déclenche un timer avec la durée 
    # chaque déclenchement du timer applique le mode, et relance le timer avec la nouvelle durée
    


 
