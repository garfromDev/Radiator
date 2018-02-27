import os.path
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from ActionSequencer import Action, ActionSequencer
from Rolling import Rolling

class ActionSequencerLibrary(object):
    """
    Allows to test ActionSequencer.py with robot framework 
    """
    def __init__(self):
      self._result = ''
    
    def _store(self, action):
        def deepStore():
            self._result = action()
            return action
        return deepStore
        
    def create_default_action_sequencer(self, nb):
        seq = self._createSeq(int(nb))      
        self._sequencer = ActionSequencer(seq)
        
    def executed_action_should_be(self, id):
        if self._result != id:
            raise AssertionError('%s != %s' % (self._result, expected))
        
    def start_current_sequencer_with(self, nb):
        seq = self._createSeq(int(nb))
        self._sequencer.start(seq)
        
    def start_it(self):
        self._sequencer.start()
    
    def stop_it(self)
        self._sequencer.stop()
        
    def _createSeq(self,nb):
        seq=Rolling()
        for i in range(nb):
            a = Action(self.store(lambda i=i:str(i+1)), 1) #merci http://sametmax.com/fonctions-anonymes-en-python-ou-lambda/
            seq.add(a)
        return seq
