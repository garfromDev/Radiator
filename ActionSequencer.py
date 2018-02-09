# -*- coding: utf-8 -*-
import Rolling

# this object is an elementary couple action + time before next action (in sec.) to use with the Sequencer 
class Action:
    def __init__(self, action, duration):
        self.action = action
        self.duration = duration
        
        
# the sequencer will repeat each action, then wait for duration, rolling through the sequence of Action
class ActionSequencer:
def __init__(self, sequence=None):
  self.sequence = sequence
 
# start the sequencer if a sequence is given, or shhot the next action (called by the timer from previous call)
def start(self, sequence=None):
   if sequence != None:
        self.timer.cancel()
        self.sequence = sequence
   currentAction = self.sequence.get()
   currentAction.action()
   self.timer = Timer(currentAction.duration, self.start)
   self.timer.start()

# stop the sequencer        
def cancel(self):
   self.timer.cancel()
   
   
