# -*- coding: utf-8 -*-
import CST
import const
const.USER_JSON = "userInteraction.json"
const.JSON_PATH = "/home/pi/Program/Radiator/" # the path to the weekly calendar

class UserInteractionManager:
  """
    this module allow to interface with user about
    overruling the calendar (vacation, day at home, ...)
    it will fetch the user decision in a json file 
  """
  def __init__(self, path=const.JSON_PATH, file=const.USER_JSON):
    self._jsonFile = path + file
    
  def overruled(self):
    """
      return: true if user has decided to temporary overrule the heatCalendar
    """
    return False # TODO implement!
  
  
  def overMode(self):
    """
      return: the metamode choosen by the user (ECO, CONFORT)
    """
    return CST.UNKNOW # TODO implement!
    
    
  def userBonus(self):
    """
      return: true if user has requested to increase temperature
    """
    return False # TODO implement!
  
  
  def userDown(self):
    """
      return: true if user has requested to increase temperature
    """
    return False # TODO implement! 

  
  def targetTemp(self):
    """
      return: the target temp chosen by the user or None
    """
    return None # TODO implement!
