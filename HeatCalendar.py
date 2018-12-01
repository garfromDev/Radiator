# -*- coding: utf-8 -*-
# 
# javascript peut enregistrer en local des paires clef:valeur
# PHP peut ecrire dans un fichier
# struture json : voir week.json
# note : use http://jsonviewer.stack.hu/ to look at  json file
# note : use https://jsonlint.com/ to validate json structure with usefull warnings

# concept : json file will be update by web server according user interaction
# this module will check every 15mn the mode indicated by the json and set meta_mode 

# =================================================
# usage of json structure: 
#import json
#j = '{"weekCalendar":{"Monday":{"08:00":"confort","08:15":"confort"},"Tuesday":{"12:00":"eco","12:15":"confort"}}}'
#wk = json.loads(j)
#print(wk['weekCalendar']['Monday']['08:15'])
#==================================================

import CST
import time
import json
import logging 
    
class HeatCalendar:
  """ This object read the calendar in a file and extract the current mode
      The idea is to call it every 15mn to change Heating mode, the file 
      content may be changed by the distant user via the web server
      of course, in worst case change could take 15mn to apply
  """
  def __init__(self, calFile = CST.CALENDAR_PATH + CST.WEEKCALJSON, localtime = time.localtime):
    """ :param calFile name of the json file that describe the calendar """ 
    self._calFile = calFile
    self.localtime = localtime
    
  # return the meta mode for the current hour and time
  # hour and time is given by system time
  # meta mode is given by the json file defined in CST.WEEKCALJSON
  # WARNING: no check done on metamode value
  def getCurrentMode(self):
    # ouvrir le fichier
    try:
      with open( self._calFile) as wcal:
        calendar = json.load(wcal)
        metaMode=calendar['weekCalendar'][self.day()][self.hour()]
    except Exception as err:
      #soit le fichier n'a pu être lu, soit le calendrier n'est pas complet
      logging.error(err)
      metaMode=CST.UNKNOW
    return metaMode
  
  # return the day in the form of 'Monday', 'Tuesday', ...
  def day(self):
    dayNr = int(time.strftime("%w",self.localtime())) #strftime return a string
    # we use a table conversion because locale could be different between the pi running 
    # the python programm and the app sending data to the Json file
    # so I choose the json file will be english wathever the locale language                      
    dayNames = ["Sunday","Monday","Tuesday","Wenesday","Thursday","Friday","Saturday"]
    return dayNames[dayNr]
  
  def hour(self):
    """ return a string with the current minute rounded to quarter 08:15
      0 to 14 -> 00
      15 to 29 -> 15
    """
    h = time.strftime("%H",self.localtime()) #get the hour 00 to 23
    m = time.strftime("%M",self.localtime()) #get the minute 00 to 59
    return "%s:%s" % (h, self._normalize(m))
                      
  def _normalize(self, minutes):
    m = int(minutes) / 15
    rounded = m * 15
    return '{:02d}'.format(rounded)
                      
# PROBLEMATIQUE DE TEST
# faire :  HeatCalendar(localtime = lambda x=1: time.strptime("2018 02 26 08 00", "%Y %m %d %H %M") ) pour
#initialiser le calendrier avec une heure donnée

if __name__ == '__main__':
    a=HeatCalendar()
    print(a.getCurrentMode())
    
