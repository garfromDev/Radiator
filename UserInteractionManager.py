# -*- coding: utf-8 -*-
import logging
import json
from datetime import datetime
from FilteredVar import FilteredVar
from CST import CST
CST.USER_JSON = "userInteraction.json"
CST.JSON_PATH = '/home/pi/Program/Radiator/' # the path to the weekly calendar

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
    return self._isValid(self._userInputs["overruled"])
  
  
  def overMode(self):
    """
      return: the metamode choosen by the user (ECO, CONFORT, ..)
      It is the consumer responsability to check overrule validity, no check done here
      In case the userInputs dictionary do not contains key, return UNKNOW
    """
    try:
      return self._userInputs["overruled"]["overMode"] 
    except Exception as err:
      return CST.UNKNOW
    
    
  def userBonus(self):
    """
      return: true if user has requested to increase temperature
    """
    return self._isValid(self._userInputs["userBonus"])
  
  
  def userDown(self):
    """
      return: true if user has requested to increase temperature
    """
    return self._isValid(self._userInputs["userDown"]) 
  
  
  def _getUserInputs(self):
    """
      return userInteraction dictionary from the file
      if file opening fails, return stub object
    """
    # ouvrir le fichier
    try:
      with open( self._jsonFile) as usrDecision:
        usr = json.load(usrDecision)
        res=usr['userInteraction']
    except Exception as err:
      #soit le fichier n'a pu être lu, soit le calendrier n'est pas complet
      logging.error(err.message)
      res={"overruled":{"status":False, "expirationDate":"01/01/2000","overMode":"UNKNOW"},
           "userBonus":{"status":False, "expirationDate":"01/01/2000"},
           "userDown":{"status":False, "expirationDate":"01/01/2000"}}
    return res

  
  def _isValid(self,  decisionBloc):
    """
      return true if the status is true and the expiration date not met
      will return False if decisionBloc dictionnary do not contain appropriate keys
    """
    try:
      return decisionBloc["status"] and self._isValidDate(decisionBloc["expirationDate"])
    except Exception as err:
      logging.error(err.message)
      return False
  
  
  def __isValidDate(self, dateString):
    """
      return true if the datestring in format 30/06/2018 is in the future
      be carrefull, it is taken at 0h am, so if the date is today, it is no valid anymore
    """
    var thisDate = datetime.strptime(dateString,"%d/%m/%Y")
    return thisDate >= datetime.now()
    
    
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
 
