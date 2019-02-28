# -*- coding: utf-8 -*-
import logging

from CST import CST
from CurrentTemperature import InsideCondition
from FeltTemperature import FeltTemperature
from FilteredVar import FilteredVar
from HeatCalendar import HeatCalendar
from HeatMode import HeatMode
from UserInteractionManager import UserInteractionManager


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
  modes_list = [ 'minus2', 'minus2', 'minus1', 'confort', 'confort']
  
  def __init__(self, calendar=HeatCalendar(calFile=CST.WEEKCALJSON), userManager=UserInteractionManager()):
    logging.info("DecisionMaker init")
    self._calendar = calendar
    self.metaMode = FilteredVar(cacheDuration = CST.METACACHING, getter = self._calendar.getCurrentMode)
    self._heater = HeatMode()
    self._userManager = userManager
    self.insideTemp = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=InsideCondition().temperature)
    self._felt_temp_manager = FeltTemperature( insideTemperature=self.insideTemp,
                                             insideSunLevel = InsideCondition().light_condition)
    self.userBonus = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=self._userManager.userBonus)
    self.userDown = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=self._userManager.userDown)
    self.feltTempCold = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=lambda x=None:False) #!!!! à remplacer !!!
    self.feltTempHot = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=lambda x=None:False) #!!!! à remplacer !!!
    self.overruled = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=self._userManager.overruled)
    self.overMode =  FilteredVar(cacheDuration = CST.TEMPCACHING, getter=self._userManager.overMode)
  
  
                                 
                            
  def makeDecision(self):
    #0 get meta mode from calendar
    metaMode = self.metaMode.value()
    info = "mode from calendar : "+metaMode
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
      info = "applyed overruled "+metaMode

    #2 eco mode
    if metaMode != CST.CONFORT:
      self._heater.setEcoMode()
      info="maked decision setEcoMode"
      return

    # metaMode == CST.CONFORT:
    #3 adaptation of confort mode according felt temperature
    confort_mode = Confort_mode()
    if self._felt_temp_manager.feltTempCold():
      confort_mode = confort_mode.make_hot()
    elif self._felt_temp_manager.feltTempHot():
      confort_mode = confort_mode.make_cold()
    elif self._felt_temp_manager.feltTempSuperHot(): 
      confort_mode = confort_mode.make_cold().make_cold()
    logging.info("after feltTemperature evaluation, mode is %s",confort_mode)
                                 
    #4 adaptation of confort mode according user bonus
    if self.userBonus.value():
      confort_mode = confort_mode.make_hot()
    elif self.userDown.value():
      confort_mode = confort_mode.make_cold()
                      
    #5 application of confort mode
    self._heater.set_from_confort_mode(confort_mode)
    info = "Heating mode applied : {}".format(confort_mode)
    logging.info(info)
    return info



if __name__ == '__main__':
  print("testing DecisionMaker manually")
  logging.basicConfig(filename='Radiator.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
  test = DecisionMaker()
  print("decision  taken : "+test.makeDecision())
  print("Decision taken can be inspected in log file or through StateDisplay")
  
