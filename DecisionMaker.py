# -*- coding: utf-8 -*-
from HeatCalendar import HeatCalendar
from HeatMode import HeatMode
from FilteredVar import FilteredVar
from CurrentTemperature import InsideTemperature
import CST
import logging

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
    logging.info("DecisionMaker init")
    self._calendar = HeatCalendar(calFile=CST.WEEKCALJSON)
    self.metaMode = FilteredVar(cacheDuration = CST.METACACHING, getter = self._calendar.getCurrentMode)
    self._heater = HeatMode()
    self._curTemp = InsideTemperature()
    self.insideTemp = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=self._curTemp.value)
    self.userBonus = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=lambda x=None:False) #!!!! à remplacer !!!
    self.userDown = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=lambda x=None:False) #!!!! à remplacer !!!
    self.feltTempCold = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=lambda x=None:False) #!!!! à remplacer !!!
    self.feltTempHot = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=lambda x=None:False) #!!!! à remplacer !!!
    
  def makeDecision(self):
    #1 get meta mode
    metaMode = self.metaMode.value()
    logging.info("makeDecision metamode = {} temp = {:.1f} Bonus = {} feltCold = {} feltHot = {} userDown = {}".format(metaMode,
                                                                                                         self.insideTemp.value(),
                                                                                                         self.userBonus.value(),
                                                                                                         self.feltTempCold.value(),
                                                                                                         self.feltTempHot.value(),
                                                                                                         self.userDown.value())
                )
    if metaMode != "confort":
      self._heater.setEcoMode()
      logging.info("make decision setEcoMode")

    #2 adaptation of confort mode
    if metaMode == "confort":
      if self.userBonus.value():
        self._heater.setConfortMode()
        logging.info("makeDecision setConfortMode")
      elif self.feltTempCold.value():
        self._heater.setConfortMode()
        logging.info("makeDecision setConfortMode")
      elif self.feltTempHot.value() :
        self._heater.setConfortMinus2()
        logging.info("makeDecision setConfortModeMinus2")
      elif self.userDown.value():
        self._heater.setConfortMinus2()
        logging.info("makeDecision setConfortModeMinus2")
      else:
        self._heater.setConfortMinus1()
        logging.info("makeDecision setConfortModeMinus1")
 
