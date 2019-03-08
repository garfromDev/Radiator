# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
from Rolling import Rolling
from ActionSequencer import Action, ActionSequencer
import logging
from HeatingStateDisplayer import HeatingStateDisplayer

# This module alow to drive pilot wire

class Confort_mode(object):
    """ abstract representation of confort mode
        use make_hot() and make_cold() to change desired confort mode
    """
    minus1 = 'minus1'
    minus2 = 'minus2'
    confort = 'confort'
    _mode_list = [minus2, minus1, confort]
    _current_index = 1
    
    def __init__(self, confort_mode = minus1):
        self._set(confort_mode)
      
    def _set(self, confort_mode):
        self.confort_mode = confort_mode
        self._current_index = self._mode_list.index(confort_mode) 

    def make_hot(self):
        new_mode = self._mode_list[min(self._current_index+1, len(self._mode_list)-1 ) ]
        return Confort_mode(new_mode)

    def make_cold(self):
        new_mode = self._mode_list[max(self._current_index-1, 0) ]
        return Confort_mode(new_mode)

    def __repr__(self):
        return self._mode_list[self._current_index]

    def __eq__(self,other):
        return self._current_index == other._current_index


class ConfortMinus1(Confort_mode):
    def __init__(self):
        super(ConfortMinus1,self).__init__(Confort_mode.minus1)

class ConfortMinus2(Confort_mode):
    def __init__(self):
        super(ConfortMinus2,self).__init__(Confort_mode.minus2)

class Confort(Confort_mode):
    def __init__(self):
        super(Confort,self).__init__(Confort_mode.confort) 


class HeatMode(object):
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
        logging.debug("starting sequencer with sequence confortMinus2Seq")
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


    def set_from_confort_mode(self, new_mode):
        """
        :param Confort_mode new_mode: the mode to apply
        Apply the mode if confort, minus1, minus2, does nothing else
        """
        #import pdb; pdb.set_trace()
        logging.debug("HeatMode setting confort mode to %s",new_mode) 
        if new_mode == Confort():
            self.setConfortMode()
        elif new_mode == ConfortMinus1():
            self.setConfortMinus1()
        elif new_mode == ConfortMinus2():
            self.setConfortMinus2()
        else:
            logging.error("Heatmode unknow mode %s",new_mode)


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
	#logging.basicConfig(filename='Radiator.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
	test = HeatMode()
	#test.setConfortMinus1()

