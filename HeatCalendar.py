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
import json
j = '{"weekCalendar":{"Monday":{"08:00":"confort","08:15":"confort"},"Tuesday":{"12:00":"eco","12:15":"confort"}}}'
wk = json.loads(j)
print(wk['weekCalendar']['Monday']['08:15'])
#==================================================

class HalfHour:
  def __init__(self, hour, metaMode):
    if hour > 48 or hour < 0 or (hour mod 2 != 0):
      raise ValueError('invalid half hour definition')
    self.hour = hour
    self.metaMode = metaMode

class HeatCalendar:

  def setWeekCal(self, week):
    pass
  
  def getCurrentMode(self):
    # ouvrir le fichier
    with open('weekCalendar.json') as wcal:
      try:
        calendar = json.load(wcal)
        metaMode=calendar['weekCalendar'][self.day][self.hour]
      except:
        # que fait-on en cas d erreur?
        metaMode=
