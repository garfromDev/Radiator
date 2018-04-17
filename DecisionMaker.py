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
    self.overruled = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=lambda x=None:False) #!!!! à remplacer !!!
    self.overMode =  FilteredVar(cacheDuration = CST.TEMPCACHING, getter=lambda x=None:CST.ECO) #!!!! à remplacer !!!
  
  
  def makeDecision(self):
    #0 get meta mode  
    metaMode = self.metaMode.value()
    logging.info("makeDecision metamode = {} temp = {:.1f} Bonus = {} feltCold = {} feltHot = {} userDown = {} overruled = {} overMode = {}".format(metaMode,
                                                                                                         self.insideTemp.value(),
                                                                                                         self.userBonus.value(),
                                                                                                         self.feltTempCold.value(),
                                                                                                         self.feltTempHot.value(),
                                                                                                         self.userDown.value(),
                                                                                                         self.overruled.value(),
                                                                                                         self.overMode.value() )
                )

    #1 apply overrule by user
    if self.overruled.value():
      metaMode=self.overMode.value()

    #2 apply calendar                  
    if metaMode != CST.CONFORT:
      self._heater.setEcoMode()
      logging.info("maked decision setEcoMode")

    #3 adaptation of confort mode
    if metaMode == CST.CONFORT:
      if self.userBonus.value():
        self._heater.setConfortMode()
        logging.info("maked Decision setConfortMode")
      elif self.feltTempCold.value():
        self._heater.setConfortMode()
        logging.info("maked Decision setConfortMode")
      elif self.feltTempHot.value() :
        self._heater.setConfortMinus2()
        logging.info("maked Decision setConfortModeMinus2")
      elif self.userDown.value():
        self._heater.setConfortMinus2()
        logging.info("maked Decision setConfortModeMinus2")
      else:
        self._heater.setConfortMinus1()
        logging.info("maked Decision setConfortModeMinus1")
 
