# -*- coding: utf-8 -*-
import logging
from typing import Optional, Any
from app import models
from app.models import OverMode
from .CST import CST
from .InsideCondition import InsideCondition
from .FeltTemperature import FeltTemperature
from .FilteredVar import FilteredVar
from .HeatCalendar import HeatCalendar
from .HeatMode import HeatMode, ComfortMode
from .UserInteractionManager import UserInteractionManager


logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
handler = logging.FileHandler('test.log') # creates handler for the log file
logger.addHandler(handler) #

class DecisionMaker(object):
    """Central decision point of Radiator
    will be called every x min by main sequencer
    Create and parameterize during init() the different objects needed
    decide meta-mode based on HeatCalendar and user overrule
    in metaComfort, decide heating mode based on
      - ext temp
      - sun
      - felt internal temp (combine heat and humidity)
    """

    _userManager: Any

    @property
    def user_bonus(self) -> bool:
        return self._userManager.userBonus()

    @property
    def user_down(self) -> bool:
        return self._userManager.userDown()

    @property
    def overruled(self) -> bool:
        # print("=== DecisionMaker overruled  %s" % self._userManager.overruled())
        return self._userManager.overruled()

    @property
    def overmode(self) -> OverMode:
        return self._userManager.over_mode()

    def __init__(
        self,
        calendar=HeatCalendar(calFile=CST.WEEKCALJSON),
        user_manager: Optional[UserInteractionManager] = None,
    ):
        logger.info("DecisionMaker init")
        self._calendar = calendar
        self.metaMode = FilteredVar(
            cacheDuration=CST.METACACHING, getter=self._calendar.getCurrentMode
        ).value
        self._heater = HeatMode()

        # create an instance of InsideCondition to avoid duplicating instance for temperature and light_level
        ic = InsideCondition.shared()
        self._ic = ic
        # we keep direct access to inside_temp for logging
        self.insideTemp = FilteredVar(
            cacheDuration=CST.TEMPCACHING, getter=ic.temperature
        ).value
        self._felt_temp_manager = FeltTemperature(
            insideTemperature=ic.temperature, insideSunLevel=ic.light_condition
        )
        self.feltTempCold = FilteredVar(
            cacheDuration=CST.TEMPCACHING, getter=self._felt_temp_manager.feltTempCold
        ).value
        self.feltTempHot = FilteredVar(
            cacheDuration=CST.TEMPCACHING, getter=self._felt_temp_manager.feltTempHot
        ).value
        self.feltTempSuperHot = FilteredVar(
            cacheDuration=CST.TEMPCACHING,
            getter=self._felt_temp_manager.feltTempSuperHot,
        ).value
        self._userManager = user_manager or UserInteractionManager(
            user_interaction_provider=models.UserInteraction()
        )
        logger.info("DecisionMaker init finished")

    def make_decision(self) -> str:
        print("=== makeDecision ==========")
        # 0 get meta mode from calendar
        meta_mode: OverMode = self._calendar.getCurrentMode()
        print("=== meta_mode %s" % meta_mode)
        self._userManager.update()
        print("=== updated ")
        info = "mode from calendar : " + str(meta_mode)
        # logging.info(
        #     "makeDecision metamode = {} temp = {:.1f} Light = {}  Bonus = {} feltCold = {} feltHot = {}"
        #     " feltSuperHot = {} userDown = {} overruled = {} overMode = {}".format(
        #         meta_mode,
        #         self.insideTemp() or 9999,
        #         self._ic.light(),
        #         self.user_bonus,
        #         self.feltTempCold(),
        #         self.feltTempHot(),
        #         self.feltTempSuperHot(),
        #         self.user_down,
        #         self.overruled,
        #         self.overmode,
        #     )
        # )
        print(
            "makeDecision metamode = {} temp = {:.1f} Light = {}  Bonus = {} feltCold = {} feltHot = {}"
            " feltSuperHot = {} userDown = {} overruled = {} overMode = {}".format(
                meta_mode,
                self.insideTemp() or 9999,
                self._ic.light(),
                self.user_bonus,
                self.feltTempCold(),
                self.feltTempHot(),
                self.feltTempSuperHot(),
                self.user_down,
                self.overruled,
                self.overmode,
            )
        )

        #  1 apply overrule by user
        print("=== 1 apply overrule by user")
        if self.overruled:
            # print("=== self is overruled")
            meta_mode = self.overmode
            # print("=== ", meta_mode)
            info = info + "  applied overruled " + str(meta_mode)
        print("=== ", info)
        #  2 eco mode
        if meta_mode != OverMode.CONFORT:
            # UNKNOWN will apply eco
            self._heater.set_eco_mode()
            info = info + "  make decision setEcoMode"
            logger.info(info)
            print(info)
            print(f"=== will return {str(meta_mode)}")
            return str(meta_mode)

        # metaMode == CONFORT:

        comfort_mode = ComfortMode()
        #  3 adaptation of comfort mode according user bonus
        if self.user_bonus:
            comfort_mode = ComfortMode("confort")
        elif self.user_down:
            comfort_mode = ComfortMode("minus2")

        #  4 adaptation of comfort mode according felt temperature
        if not self.overruled:
            if self.feltTempCold():
                comfort_mode = comfort_mode.make_hot()
            elif self.feltTempHot():
                comfort_mode = comfort_mode.make_cold()
            elif self.feltTempSuperHot():
                comfort_mode = comfort_mode.make_cold().make_cold()
            logger.debug("after feltTemperature evaluation, mode is %s", comfort_mode)
            print("after feltTemperature evaluation, mode is %s" % comfort_mode)
        #  4 adaptation of comfort mode according user bonus
        if self.user_bonus:
            comfort_mode = comfort_mode.make_hot()
        elif self.user_down:
            comfort_mode = comfort_mode.make_cold()

        # 5 application of comfort mode
        self._heater.set_from_confort_mode(comfort_mode)
        info = info + "  Heating mode applied : {}".format(comfort_mode)
        logger.info(info)
        print("=== Decision Maker ", info)
        print(f"=== will return {str(comfort_mode)}")
        return str(comfort_mode)


if __name__ == "__main__":
    print("testing DecisionMaker manually")
    test = DecisionMaker()
    print("decision  taken : " + test.make_decision())
    print("Decision taken can be inspected in log file or through StateDisplay")
