# -*- coding: utf-8 -*-

import logging
from ActionSequencer import Action, ActionSequencer
from DecisionMaker import DecisionMaker
from Rolling import Rolling
import CST

def main():
  logging.basicConfig(filename='Radiator.log', level=logging.INFO, format='%(asctime)s %(message)s')
  logging.info('Started')
  decider = DecisionMaker()
  action = Action( decider.makeDecision, CST.MAIN_TIMING)
  mainSeq = Rolling(action)
  sequencer = ActionSequencer(mainSeq)
  sequencer.start()
  
if __name__ == '__main__':
  main()
