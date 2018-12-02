# -*- coding: utf-8 -*-

# This utility module define constant

class _const:
    """
      now any client-code can import const
      and bind an attribute ONCE:
      const.magic = 23
    """
    class ConstError(TypeError): pass
    def __setattr__(self,name,value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind const(%s)"%name
        self.__dict__[name]=value
import sys
sys.modules[__name__]=_const()

CST.MIN         = 60            # conversion of minutes to second
CST.WEEKCALJSON = "week.json"   # the file that defines the weekly calendar
CST.CALENDAR_PATH = "."         # the path to the weekly calendar file
CST.METACACHING = 5 * MIN       # caching duration for meta mode check
CST.TEMPCACHING = 2 * MIN       # caching duration for temperature check
CST.MAIN_TIMING  = 15 * MIN     # main looprefreshing
CST.CONFORT = "confort"         # confort meta mode
CST.CONFORTPLUS = "confortPlus" # confort plus meta mode
CST.ECO = "eco"                 # eco meta mode
CST.UNKNOW = "unknow"           # unknow meta mode
CST.MAX_DELTA_TEMP = 0.2        # maximum temperature span between 2 simultaneous measurement for filtering (in °C)
CST.LM35_INTERVAL = 0.01        # interval in sec between 2 measure for filtering temperature measurement
CST.SUPER_HOT_DELTA = 3         # delta between target temp and measured temp to entre super hot mode
