# -*- coding: utf-8 -*-
import threading

# this object is an elementary couple action + time before next action (in sec.) to use with the Sequencer 
# action : a function
# duration : in sec.
class Action:
    def __init__(self, action, duration):
        self.action = action
        self.duration = duration
        
        
# the sequencer will repeat each action, then wait for duration, rolling through the sequence of Action
class ActionSequencer:
   #sequence : a Rolling() collection of Action() 
  def __init__(self, sequence=None):
    self.sequence = sequence
    self.timer = None
 
  # start the sequencer if a sequence is given, or shoot the next action (called by the timer from previous call)
  def start(self, sequence=None):
   if sequence != None:
        self.cancel() #Setting a new sequence cancel the previous one if there was one
        self.sequence = sequence
   currentAction = self.sequence.get() 
   currentAction.action() #perform the first action
   self.timer = threading.Timer(currentAction.duration, self.start) 
   self.timer.start() #this will call start() again after duration, which will perform the next action

  # stop the sequencer        
  def cancel(self):
   try: #because timer may not exist
     self.timer.cancel()
   except:
     pass
   
   
