# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import logging

# This module alow to drive RGB Led
class RGB_Displayer:
    # outBlue :
    # The GPIO output that drive the blue Led (in GPIO.BCM notation)
    # outRed :
    # The GPIO output that drive the red Led (in GPIO.BCM notation)
    # outGreen :
    # The GPIO output that drive the green Led (in GPIO.BCM notation)
    # inhibit :
    # function that when return true, forbid to light Led on
    def __init__(self, outRed=23, outGreen=25, outBlue=24, inhibit=lambda x=None : false ):
        self._outRed = outRed
        self._outGreen = outGreen
        self._outBlue = outBlue
	self._inhibit=inhibit
	GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._outRed, GPIO.OUT)
        GPIO.setup(self._outGreen, GPIO.OUT)
	GPIO.setup(self._outBlue, GPIO.OUT)
	logging.debug("RGB_Displayer initialized")


   # Set the Led to red    
    def setColorRed(self):
	self.turnOff()
        if !inhibit():
            ouput(self._outRed, GPIO.HIGH)
      

   # Set the Led to green    
    def setColorGreen(self):
        self.turnOff()
        if !inhibit()	    
            ouput(self._outGreen, GPIO.HIGH)
		
		
   # Set the Led to Blue    
    def setColorBlue(self):
        self.turnOff()
        if !inhibit()	    
            ouput(self._outBlue, GPIO.HIGH)
              
    # turn all Leds off
    def turnOff(self):
	ouput(self._outRed, GPIO.LOW)
	ouput(self._outGreen, GPIO.LOW)
	ouput(self._outBlue, GPIO.LOW)
	

    
if __name__ == '__main__':
	print("testing RGB_Displayer manually")
	logging.basicConfig(filename='Radiator.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
	test = RGB_Displayer()
	test.setColorRed()
	time.sleep(0.5)
	test.setColorGreen()
	time.sleep(0.5)
	test.setColorBlue()
	time.sleep(0.5)
	test.turnOff()