# -*- coding: utf-8 -*-
from HeatCalendar import HeatCalendar
from HeatMode import HeatMode
from FilteredVar import FilteredVar
from CurrentTemperature import InsideTemperature
import CST

class DecisionMaker(object):
  """ Central decision point of Radiator
      will be called every x min by main sequencer
      Create and parameterize during init() the different objects needed
      decide meta-mode based on HeatCalendar and user overrule
      in metaConfort, decide heating mode based on 
        - ext temp
        - sun
        - felt internal temp (combine heat and humidity)
   """

  def __init__(self):
    self._calendar = HeatCalendar(calFile=CST.WEEKCALJSON)
    self.metamode = FilteredVar(cacheDuration = CST.METACACHING, getter = self._calendar.getCurrentMode)
    self._heater = Heatmode()
    self._curTemp = InsideTemperature()
    self.insideTemp = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=self._curTemp.value)
    self.userBonus = False #!!!! mécanisme à ajouter !!!!
    self.userDown = False #!!!! mécanisme à ajouter !!!!
    self.feltTemp = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=self.insideTemp.value) #!!!! à remplacer !!!
    
    
  def makeDecision(self):
    #1 get meta mode
    metaMode = self.metaMode.value()
    
    if metaMode != "confort":
      self._heater.setEcoMode()
    
    #2 adaptation of confort mode
    if metaMode == "confort":
      if self.userBonus.value():
        self._heater.setConfortMode
      elif self.felTemp.value() < CST.FELT_TEMP_MIN:
        self._heater.setConfortMode
      elif self.felTemp.value() > CST.FELT_TEMP_MAX:
        self._heater.setConfortModeMinus2
      elif self.userDown.value():
        self._heater.setConfortModeMinus2
      else:
        self._heater.setConfortModeMinus1
      
 
