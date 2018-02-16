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

# to be deleted?
class HalfHour:
  def __init__(self, hour, metaMode):
    if hour > 48 or hour < 0 or (hour mod 2 != 0):
      raise ValueError('invalid half hour definition')
    self.hour = hour
    self.metaMode = metaMode

    
    
class HeatCalendar:

  def setWeekCal(self, week):
    pass
  
  # return the meta mode for the current hour and time
  # hour and time is given by system time
  # meta mode is given by the json file defined in CST.WEEKCALJSON
  #
  def getCurrentMode(self):
    # ouvrir le fichier
    with open(CST.WEEKCALJSON) as wcal:
      try:
        calendar = json.load(wcal)
        metaMode=calendar['weekCalendar'][self.day][self.hour]
      except:
        # que fait-on en cas d erreur, comment on prévient?
        #soit le fichier n'a pu être lu, soit le calendrier n'est pas complet
        metaMode="unknow"
     return metaMode
  
  # return the day in the form of 'Monday', 'Tuesday', ...
  def day(self):
    dayNr = time.strftime(%w",localtime())
    # we use a table conversion because locale could be different between the pi running 
    # the python programm and the app sending data to the Json file
    # so I choose the json file will be english wathever the locale language                      
    dayNames = ["Sunday","Monday","Tuesday","Wenesday","Thursday","Friday","Saturday"]
    return dayNames[dayNr]
                          
