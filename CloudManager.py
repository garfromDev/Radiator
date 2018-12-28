# -*- coding: utf-8 -*-
import logging
from CST import CST
from DistantFileInterface import DistantFileInterface

class CloudManager(object):
  """
    This object allow to fetch the calendar and user decision file from the server
    using the DistantFileInterface
  """
  
  def __init__(self,distantFileInterface=DistantFileInterface()):
    self._distantFileInterface=distantFileInterface
    self._distantFileInterface.configure(server="")
    
  def update(self):
    #fetch calendar file
    
