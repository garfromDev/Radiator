# -*- coding: utf-8 -*-
import threading
import logging

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
    logging.debug("start sequencer")
    if sequence != None:
        self.cancel() #Setting a new sequence cancel the previous one if there was one
        self.sequence = sequence
    
    try:
        currentAction = self.sequence.get()
    except:
        self.timer = None #not a Rolling we stop
        return
    logging.debug("perform action")
    try:
        currentAction.action() #perform the first action
    except:
        logging.debug("action failed")
        pass #None or crashy, maybe next action will behave better
    
    try:
        dur = currentAction.duration
        self.timer = threading.Timer(dur, self.start) 
        self.timer.start() #this will call start() again after duration, which will perform the next action
    except:
        self.timer = None #duration not valid
		
		
  # stop the sequencer        
  def cancel(self):
   try: #because timer may not exist
     self.timer.cancel()
   except:
     pass
   
 
