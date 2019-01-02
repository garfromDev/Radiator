# -*- coding: utf-8 -*-
import logging
from CST import CST
from DistantFileInterface import DistantFileInterface
CST.FTP_SERVER = "ftp://perso-ftp.orange.fr/Applications/maxouf14/Parameters"

class CloudManager(object):
  """
    This object allow to fetch the calendar and user decision file from the server
    using the DistantFileInterface
  """
  
  def __init__(self,distantFileInterface=DistantFileInterface(),
               userDecisionFileName = CST.USER_JSON,
               weekCalendarFileName = CST.WEEKCALJSON):
    self._distantFileInterface=distantFileInterface
    self._distantFileInterface.configure(server=CST.FTP_SERVER)
    self._userDecisionFileName = userDecisionFileName
    self._weekCalendarFileName = weekCalendarFileName
    
    
  def update(self):
    """
      fetch the file from distant location using provided DistantFileInterface
      file will be saved in local directory with same name, overwriting without warning
    """  
    self._distantFileInterface.fetch(self._weekCalendarFileName)
    self._distantFileInterface.fetch(self._userDecisionFileName)
    
