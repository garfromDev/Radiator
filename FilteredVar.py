# -*- coding: utf-8 -*-

# This utility module define an object that cache the value

import time

class FilteredVar:
    # cacheDuration : the time in sec after wiche the value is invalid
    # the function that will be called to retrieve a new value
    def __init__(self, cacheDuration, getter):
        self.cacheDuration = cacheDuration
        self._value = getter()
        self._valueDate = time()
        self._getter = getter
        
    # return the cached value if still valid (less than cacheDuration since last refresh)
    # return the new value if value is invalid
    # if getter raise exception, value will be None, and exception will be re-raised
    def value(self):
        if time() - self._valueDate > self.cacheDuration:
            try:
                self._value = self._getter()
            except:
                self._value = None
                self._valueDate = 0 #value timestamp will be invalid
                raise
        return self._value