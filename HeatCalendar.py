# -*- coding: utf-8 -*-
# 
# javascript peut enregistrer en local des paires clef:valeur
# PHP peut ecrire dans un fichier
# struture json : voir week.json
# note : use http://jsonviewer.stack.hu/ to look at  json file
# note : use https://jsonlint.com/ to validate json structure with usefull warnings

class HalfHour:
  def __init__(self, hour, metaMode):
    if hour > 48 or hour < 0 or (hour mod 2 != 0):
      raise ValueError('invalid half hour definition')
    self.hour = hour
    self.metaMode = metaMode

class HeatCalendar:

  def setWeekCal(self, week):
  
