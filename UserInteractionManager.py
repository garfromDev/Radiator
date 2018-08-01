
# this module allow to interface with user about
# overruling the calendar (vacation, day at home, ...)
# it will fetch the user decision in a json file 

import CST.PY

class UserInteractionManager:
  def __init__(userJson):
    self._jsonFile = CST.JSON_PATH + userJson
    
  def overruled(self):
    """
      return: true if user has decided to temporary overrule the heatCalendar
    """
    return false # TODO implement!
  
  
  def overMode(self):
    """
      return: the metamode choosen by the user (ECO, CONFORT)
    """
    return UNKNOW # TODO implement!
    
    
  def userBonus(self):
    """
      return: true if user has requested to increase temperature
    """
    return false # TODO implement!
  
  
  def userDown(self):
    """
      return: true if user has requested to increase temperature
    """
    return false # TODO implement! 

  
  def targetTemp(self):
    """
      return: the target temp chosen by the user or None
    """
    return None # TODO implement!
