# -*- coding: utf-8 -*-
import logging
import json
from FilteredVar import FilteredVar
from CST import CST
CST.USER_JSON = "userInteraction.json"
CST.JSON_PATH = "~/Program/Radiator/" # the path to the weekly calendar

class UserInteractionManager(object):
  """
    this module allow to interface with user about
    overruling the calendar (vacation, day at home, ...)
    it will fetch the user decision in a json file 
  """
  def __init__(self, path=CST.JSON_PATH, file=CST.USER_JSON):
    self._jsonFile = path + file
    self._userInputs=FilteredVar(cacheDuration = CST.METACACHING, getter = self._getUserInputs)
    
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
  
  
  def _getUserInputs(self):
    # ouvrir le fichier
    try:
      with open( self._jsonFile) as usrDecision:
        usr = json.load(usrDecision)
        res=usr['userInteraction']
    except Exception as err:
      #soit le fichier n'a pu être lu, soit le calendrier n'est pas complet
      logging.error(err)
      res={"overruled":{"status":false, "expirationDate":"01/01/2000","overMode"="UNKNOW"},
           "userBonus":{"status":false, "expirationDate":"01/01/2000"},
           "userDown":{"status":false, "expirationDate":"01/01/2000"}}
    return res

  
  def targetTemp(self):
    """
      return: the target temp chosen by the user or None
    """
    return None # TODO implement!
  
    
if __name__ == '__main__':  
  print("testing UserInteractionManager manually")
  #logging.basicConfig(filename='Radiator.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
  test = UserInteractionManager()
  print("overruled : {}  userBonus : {}  userDown : {}".format(test.overruled(), test.userBonus(), test.userDown()))
 
