# -*- coding: utf-8 -*-
import logging

from .CST import CST
from .InsideCondition  import InsideCondition
from .FeltTemperature import FeltTemperature
from .FilteredVar import FilteredVar
from .HeatCalendar import HeatCalendar
from .HeatMode import HeatMode, Confort_mode
from .UserInteractionManager import UserInteractionManager


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
  
  def __init__(self, calendar=HeatCalendar(calFile=CST.WEEKCALJSON), userManager=UserInteractionManager()):
    logging.info("DecisionMaker init")
    self._calendar = calendar
    self.metaMode = FilteredVar(cacheDuration = CST.METACACHING, getter = self._calendar.getCurrentMode).value
    self._heater = HeatMode()

    #create an instance of InsideCondition to avoid duplicating instance for temperature and light_level
    ic = InsideCondition.shared()
    self._ic = ic
    # we keep direct access to inside_temp for logging
    self.insideTemp = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=ic.temperature).value
    self._felt_temp_manager = FeltTemperature( insideTemperature=ic.temperature,
                                             insideSunLevel = ic.light_condition)
    self.feltTempCold = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=self._felt_temp_manager.feltTempCold).value
    self.feltTempHot = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=self._felt_temp_manager.feltTempHot).value
    self.feltTempSuperHot = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=self._felt_temp_manager.feltTempSuperHot).value

    self._userManager = userManager
    self.userBonus = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=self._userManager.userBonus).value
    self.userDown = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=self._userManager.userDown).value
    self.overruled = FilteredVar(cacheDuration = CST.TEMPCACHING, getter=self._userManager.overruled).value
    self.overMode =  FilteredVar(cacheDuration = CST.TEMPCACHING, getter=self._userManager.overMode).value
    logging.info("DecisionMaker init finished")

  def makeDecision(self):
    #0 get meta mode from calendar
    metaMode = self.metaMode()
    info = "mode from calendar : " + metaMode
    logging.info("makeDecision metamode = {} temp = {:.1f} Light = {}  Bonus = {} feltCold = {} feltHot = {} feltSuperHot = {} userDown = {} overruled = {} overMode = {}".format(metaMode,
                                                                                                         self.insideTemp() or 9999,
                                                                                                         self._ic.light(),
                                                                                                         self.userBonus(),
                                                                                                         self.feltTempCold(),
                                                                                                         self.feltTempHot(),
                                                                                                         self.feltTempSuperHot(),
                                                                                                         self.userDown(),
                                                                                                         self.overruled(),
                                                                                                         self.overMode() ) )

    #1 apply overrule by user
    if self.overruled():
      metaMode=self.overMode()
      info = info + "  applyed overruled "+metaMode

    #2 eco mode
    if metaMode != CST.CONFORT:
      self._heater.setEcoMode()
      info = info + "  maked decision setEcoMode"
      logging.info(info)
      return info

    # metaMode == CST.CONFORT:
    #3 adaptation of confort mode according felt temperature
    confort_mode = Confort_mode()
    if self.feltTempCold():
      confort_mode = confort_mode.make_hot()
    elif self.feltTempHot():
      confort_mode = confort_mode.make_cold()
    elif self.feltTempSuperHot():
      confort_mode = confort_mode.make_cold().make_cold()
    logging.debug("after feltTemperature evaluation, mode is %s",confort_mode)

    #4 adaptation of confort mode according user bonus
    if self.userBonus():
      confort_mode = confort_mode.make_hot()
    elif self.userDown():
      confort_mode = confort_mode.make_cold()

    #5 application of confort mode
    self._heater.set_from_confort_mode(confort_mode)
    info = info + "  Heating mode applied : {}".format(confort_mode)
    logging.info(info)
    return info



if __name__ == '__main__':
  print("testing DecisionMaker manually")
  test = DecisionMaker()
  print("decision  taken : "+test.makeDecision())
  print("Decision taken can be inspected in log file or through StateDisplay")

