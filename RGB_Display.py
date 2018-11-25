# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
from Rolling import Rolling
from ActionSequencer import Action, ActionSequencer
import logging

# This module alow to drive RGB Led
class RGB_Displayer:
    # outBlue :
    # The GPIO output that drive the blue Led (in GPIO.BCM notation)
    # outRed :
    # The GPIO output that drive the red Led (in GPIO.BCM notation)
    # outGreen :
    # The GPIO output that drive the green Led (in GPIO.BCM notation)
    def __init__(self, outRed=23, outGreen=25, outBlue=24 ):
        self._outRed = outRed
        self._outGreen = outGreen
        sef._outBlue = outBlue
	 self.initDone = False
	logging.debug("HeatMode initialized")


    # Must be called once prior to use to initialize HW setting
    def hwInit(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._outPlusWaveform, GPIO.OUT)
        GPIO.setup(self._outMinusWaveform, GPIO.OUT)
        self.initDone = True
        
   # Set the pilot wire to confort mode = no sinusoid    
    def setConfortMode(self):
        self.sequencer.cancel()
        self._setConfortMode()
        
    # Set the pilot wire to eco mode = full sinusoid    
    def setEcoMode(self):
        self.sequencer.cancel()
        self._setEcoMode()     
        
    # set the pilot wire to confort minus 1 degree (4'57 flat, 3" sinusoid)    
    def setConfortMinus1(self):
	logging.debug("starting sequencer with sequence confortMinus1Seq") 
        self.sequencer.start(self._confortMinus1Seq)    

    # set the pilot wire to confort minus 2 degree (4'53 flat, 7" sinusoid)    
    def setConfortMinus2(self):
        self.sequencer.start(self._confortMinus2Seq)    

    # set the pilot wire to a ratio of confort mode
    # allowed ration from 10 to 90
    def setConfortRatio(self, ratio):
        ecoTime = (5 * 60 * ( 100 - ratio)) / 100
        confTime = (5 * 60 * ratio) / 100
        ratioSeq = Rolling([Action(self._setConfortMode, duration = confTime),
                            Action(self._setEcoMode, duration = ecoTime) 
                           ])
        self.sequencer.start(ratioSeq)
        
    #-----------------------------------------------------------    
    # set the Triac control output to parameters value    
    # will initialize HW if hw has not been initialized
    def _setOutputs(self, plus, minus):
        if not self.initDone:
            self.hwInit()
        GPIO.output(self._outPlusWaveform, plus)
        GPIO.output(self._outMinusWaveform, minus)
        
    def _setConfortMode(self):
        self._setOutputs( plus = GPIO.LOW, minus = GPIO.LOW)
	logging.debug("HeatMode -> setConfortMode")
 
    def _setEcoMode(self):
        self._setOutputs( plus = GPIO.HIGH, minus = GPIO.HIGH)
	logging.debug("HeatMode -> setEcoMode")

    
if __name__ == '__main__':
	print("testing Heatmode manually")
	logging.basicConfig(filename='Radiator.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
	test = HeatMode()
	test.setConfortMinus1()
