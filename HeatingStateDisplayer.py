# -*- coding: utf-8 -*-

import logging
import RGB_Displayer
from Rolling import Rolling
from ActionSequencer import Action, ActionSequencer


class HeatingStateDisplayer:
"""
    This object will display Heating State to local user
    current implementation use RGB_Displayer to dispaly status using one RGB led
"""
    def __init__(self, displayer=RGB_Displayer()):
        self._displayer = displayer
        self._displayer.turnOff
        self._sequencer=ActionSequencer() #used to blink the LED
        self._minus2Sequence=Rolling([Action(self._displayer.setColorGreen(), duration=4),
                                      Action(self._displayer.turnOff, duration=1)])
                                      
                                      
    def displayConfortMode(self):
        self.sequencer.cancel()
        self._displayer.setColorRed()
        
    def displayEcoMode(self):
        self.sequencer.cancel()
        self._displayer.setColorBlue()
         
    def displayConfortModeMinus1(self):
        self.sequencer.cancel()
        self._displayer.setColorGreen()
        
     def displayConfortModeMinus2(self):
        self.sequencer.start(self._minus2Sequence)
       
    
if __name__ == '__main__':
	print("testing HeatingStateDisplayer manually")
	logging.basicConfig(filename='Radiator.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
	test = HeatingStateDisplayer()
    test.displayConfortMode()
    print("Red Led light on")
    time.sleep(1)
    test.displayEcoMode()
    print("Blue Led light on")
    time.sleep(1)
	test.displayConfortMinus2() 
    print("Green LED blink")
