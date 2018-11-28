# -*- coding: utf-8 -*-

# This utility module define constant
MIN         = 60            # conversion of minutes to second
WEEKCALJSON = "week.json"   # the file that defines the weekly calendar
METACACHING = 5 * MIN       # caching duration for meta mode check
TEMPCACHING = 2 * MIN       # caching duration for temperature check
MAIN_TIMING  = 15 * MIN     # main looprefreshing
CONFORT = "confort"         # confort meta mode
ECO = "eco"                 # eco meta mode
UNKNOW = "unknow"           # unknow meta mode
MAX_DELTA_TEMP = 0.2        # maximum temperature span between 2 simultaneous measurement for filtering (in °C)
LM35_INTERVAL = 0.01        # interval in sec between 2 measure for filtering temperature measurement
SUPER_HOT_DELTA = 3         # delta between target temp and measured temp to entre super hot mode

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
