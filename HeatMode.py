# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
from Rolling import Rolling
from ActionSequencer import Action, ActionSequencer
        
# This module alow to drive pilot wire
class HeatMode:
    # outPlusWaveform :
    # The GPIO output that drive the first OptoTriac (in GPIO.BCM notation)
    # this output supress negative waveform
    # outMinusWaveform :
    # The GPIO output that drive the second OptoTriac (in GPIO.BCM notation)
    # this output supress positive waveform
    def __init__(self, outPlusWaveform=, outMinusWaveform=):
        self._outPlusWaveform = outPlusWaveform
        self._outMinusWaveform = outMinusWaveform
        self.sequencer = ActionSequencer()
        self._confortMinus1Seq = Rolling([Action(self._setConfortMode, duration=297),
                                Action(self._setEcoMode, duration = 3)])
        self._confortMinus2Seq = Rolling([Action(self._setConfortMode, duration=293),
                                Action(self._setEcoMode, duration=7)])
	self.initDone = False


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
        self.sequencer.start(self._confortMinus1Seq)    

    # set the pilot wire to confort minus 2 degree (4'53 flat, 7" sinusoid)    
    def setConfortMinus2(self):
        self.sequencer.start(self._confortMinus2Seq)    

    # set the pilot wire to a ratio of confort mode
    # allowed ration from 10 to 90
    def setConfortRatio(self, ratio):
        ecoTime = (7 * 60 * ( 100 - ratio)) / 100
        confTime = (7 * 60 * ratio) / 100
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
 
    def _setEcoMode(self):
        self._setOutputs( plus = GPIO.HIGH, minus = GPIO.HIGH)

    


  
      

 
