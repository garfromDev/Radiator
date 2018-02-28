import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from FilteredVar import FilteredVar

class FilteredVarLibrary(object):
    """
    Allows to test FilteredVar.py with robot framework 
    """
    
    def __init__(self):
      self._result = 'INIT'
      
      
    def filtered_var_should_be(self, expected):
        if self._result.value() != expected:
            raise AssertionError('%s != %s' % (self._result.value(), expected))
        
        
    def set_source_value(self, value):
        self._getter = lambda value=value: value
        
        
    def set_filtered_var(self):
        self._result = FilteredVar(1, getter = self._getter)
        
        
    def set_filtered_var_with_wrong_getter(self):
        self._result = FilteredVar(1, getter = None)
        
   
