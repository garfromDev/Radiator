# -*- coding: utf-8 -*-

import logging
from ActionSequencer import Action, ActionSequencer
from DecisionMaker import DecisionMaker
from Rolling import Rolling
import CST

sequencer = ActionSequencer() #must be global to remain alive at the end of main

def main():
  logging.basicConfig(filename='Radiator.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
  logging.info('Started')
  global decider  #must be global to remain alive at the end of main
  decider = DecisionMaker()
  action = Action( action = decider.makeDecision, duration = CST.MAIN_TIMING)
  mainSeq = Rolling([action])
  sequencer.start(mainSeq)
  
if __name__ == '__main__':
  main()
