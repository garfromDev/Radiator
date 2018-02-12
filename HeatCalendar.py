# -*- coding: utf-8 -*-
# 
# javascript peut enregistrer en local des paires clef:valeur
# PHP peut ecrire dans un fichier
# struture json :
# "weekCalendar":[
#  { "day":"Monday",
#   "modeForHour":[
#      "08:00":"confort",
#      "08:15":"confort"
#    ] 
#  }
#  { "day":"Tuesday",
#   "modeForHour":[
#      "12:00":"eco",
#      "12:15":"confort"
#    ] 
#  }
# ]
class HalfHour:
  def __init__(self, hour, metaMode):
    if hour > 48 or hour < 0 or (hour mod 2 != 0):
      raise ValueError('invalid half hour definition')
    self.hour = hour
    self.metaMode = metaMode

class HeatCalendar:

  def setWeekCal(self, week):
  
