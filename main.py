# -*- coding: utf-8 -*-

import logging
import threading
from ActionSequencer import Action, ActionSequencer
from DecisionMaker import DecisionMaker
from CloudManager import CloudManager
from Rolling import Rolling
from CST import CST
from RGB_Displayer import RGB_Displayer

sequencer = ActionSequencer() #must be global to remain alive at the end of main

def main():
  for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
  logging.basicConfig(filename='Radiator2.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
  logging.info('Started')
  global decider  #must be global to remain alive at the end of main
  decider = DecisionMaker()
  global cloudManager #must be global to remain alive at the end of main
  cloudManager = CloudManager()
  makeDecision = Action( action = decider.makeDecision, duration = CST.MAIN_TIMING)
  updateLocalFiles = Action( action = cloudManager.update, duration = 1)
  mainSeq = Rolling([updateLocalFiles, makeDecision])
  global sequencer  #must be global to remain alive at the end of main
  logging.debug("ready to start maln sequencer")
  sequencer.start(mainSeq)
  
if __name__ == '__main__':
  displayer=RGB_Displayer()
  seq=Rolling([Action(displayer.setColorGreen, 2),
              Action(displayer.turnOff, 2)])
  s=ActionSequencer()
  s.start(seq)
  def go():
    s.cancel()
    main()

  timer=threading.Timer(12,go)
  timer.start()
  
