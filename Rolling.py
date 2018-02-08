# -*- coding: utf-8 -*-
from collections import deque

class Rolling:
   def __init__(self, liste):
      self._list = deque()
      
   
   def get(self):
      l = liste.popleft()
      liste.append(l)
      return l
