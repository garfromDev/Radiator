# -*- coding: utf-8 -*-
import logging
from CST import CST
from DistantFileInterface import DistantFileInterface

class CloudManager(object):
  """
    This object allow to fetch the calendar and user decision file from the server
    using the DistantFileInterface
  """
  
  def __init__(self,distantFileInterface=DistantFileInterface(), userDecisionFileName, weekCalendarFileName):
    self._distantFileInterface=distantFileInterface
    self._distantFileInterface.configure(server="")
    self._userDecisionFileName = userDecisionFileName
    self._weekCalendarFileName = weekCalendarFileName
    
    
  def update(self):
    """
      fetch the file from distant location using provided DistantFileInterface
      file will be saved in local directory with same name, overwriting without warning
    """  
    self._distantFileInterface.fetch(self._weekCalendarFileName)
    self._distantFileInterface.fetch(self._userDecisionFileName)
    
