# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
from Rolling import Rolling
from ActionSequencer import Action, ActionSequencer
import logging
from HeatingStateDisplayer import HeatingStateDisplayer

# This module alow to drive pilot wire
class HeatMode:
    # outPlusWaveform :
    # The GPIO output that drive the first OptoTriac (in GPIO.BCM notation)
    # this output supress negative waveform
    # outMinusWaveform :
    # The GPIO output that drive the second OptoTriac (in GPIO.BCM notation)
    # this output supress positive waveform
    def __init__(self, outPlusWaveform=19, outMinusWaveform=12, stateDisplayer=HeatingStateDisplayer()):
        self._outPlusWaveform = outPlusWaveform
        self._outMinusWaveform = outMinusWaveform
        self.sequencer = ActionSequencer()
        self._confortMinus1Seq = Rolling([Action(self._setConfortMode, duration=297),
                                Action(self._setEcoMode, duration = 3)])
        self._confortMinus2Seq = Rolling([Action(self._setConfortMode, duration=293),
                                Action(self._setEcoMode, duration=7)])
        self._displayer=stateDisplayer
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
        self._displayer.displayConfortMode()
        
    # Set the pilot wire to eco mode = full sinusoid    
    def setEcoMode(self):
        self.sequencer.cancel()
        self._setEcoMode()
        self._displayer.displayEcoMode()
        
    # set the pilot wire to confort minus 1 degree (4'57 flat, 3" sinusoid)    
    def setConfortMinus1(self):
        logging.debug("starting sequencer with sequence confortMinus1Seq") 
        self.sequencer.start(self._confortMinus1Seq)
        self._displayer.displayConfortMinus1Mode()

    # set the pilot wire to confort minus 2 degree (4'53 flat, 7" sinusoid)    
    def setConfortMinus2(self):
        self.sequencer.start(self._confortMinus2Seq)
        self._displayer.displayConfortMinus2Mode()

    # set the pilot wire to a ratio of confort mode
    # allowed ration from 10 to 90
    def setConfortRatio(self, ratio):
        ecoTime = (5 * 60 * ( 100 - ratio)) / 100
        confTime = (5 * 60 * ratio) / 100
        ratioSeq = Rolling([Action(self._setConfortMode, duration = confTime),
                            Action(self._setEcoMode, duration = ecoTime) 
                           ])
        self.sequencer.start(ratioSeq)
        self._displayer.displayRatioMode(ratio) 
        
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

