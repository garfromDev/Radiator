# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import Rolling
import Action

class Action:
    def __init__(self, action, duration):
        self.action = action
        self.duration = duration
        
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
   # Set the pilot wire to confort mode = no sinusoid    
    def setConfortMode(self):
        self.timer.cancel()
        self._setConfortMode()
        
    #-----------------------------------------------------------    
    # set the Triac control output to parameters value    
    # raise exception ValueError if hw has not been initialized
    def _setOutputs(self, plus, minus):
        if ! self.initDone:
            raise hwNotInitializedError
        GPIO.output(self._outPlusWaveform, plus)
        GPIO.output(self._outMinusWaveform, minus)
        
    def _setConfortMode(self):
        self._setOutputs( plus = GPIO.LOW, minus = GPIO.LOW)
        
    # concept a developper pour le mode +& et -1
    # une file rotative contient les durée et les modes
    # on met le premier mode, et on déclenche un timer avec la durée 
    # chaque déclenchement du timer applique le mode, et relance le timer avec la nouvelle durée
    confortMinus1Seq = Rolling([Action(self._setConfortMode, duration=297), Action(self._setEcoMode, duration = 3)])
    confortMinus2Seq = Rolling([Action(self._setConfortMode, duration=293), Action(self._setEcoMode, duration=7)])
    
    def setConfortMinus1(self):
        self.timer.cancel()
        self.sequence =  confortMinus1Seq
        self.timer = self.shoot()

    def shoot(self):
        currentAction = self.sequence.get()
        currentAction.action()
        self.timer = Timer(currentAction.duration, self.shoot)
        self.timer.start()
      

 
