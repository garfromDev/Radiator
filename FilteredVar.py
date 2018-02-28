# -*- coding: utf-8 -*-

# This utility module define an object that cache the value

from time import time

class FilteredVar:

    def __init__(self, cacheDuration, getter):
        """ cacheDuration : the time in sec after wiche the value is invalid
            the function that will be called to retrieve a new value
        """        
        self.cacheDuration = cacheDuration
        self._getter = getter
        self._updateValue()
        
    # return the cached value if still valid (less than cacheDuration since last refresh)
    # return the new value if value is invalid
    # if getter raise exception, value will be None, and exception will be re-raised
    def value(self):
        if time() - self._valueDate > self.cacheDuration: #always true if duration is None
            self._updateValue()
        return self._value
    
    def _updateValue(self):
         try:
             self._value = self._getter()
             self._valueDate = time()
         except:
             self._value = None
             self._valueDate = 0 #value timestamp will be invalid
             raise
        
