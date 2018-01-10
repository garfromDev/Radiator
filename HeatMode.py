# -*- coding: utf-8 -*-

# This module alow to drive pilot wire

#
class IoParameter:
    # The GPIO output that drive the first OptoTriac (in GPIO.BCM notation)
    # this output supress negative waveform
    var output1
    
    # The GPIO output that drive the second OptoTriac (in GPIO.BCM notation)
    # this output supress positive waveform
    var output2
    
    def __init__(self, output1, ouput2):
        self.output1 = output1
        self.output2 = output2
        
