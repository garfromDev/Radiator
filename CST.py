# -*- coding: utf-8 -*-

# This utility module define constant
MIN         = 60            # conversion of minutes to second
WEEKCALJSON = "week.json"   # the file that defines the weekly calendar
STATUSJSON = "status.json"  # the file that define the current status (user Down, Overrule, ..)
JSON_PATH = "/home/pi/Program/Radiator" # the path to the weekly calendar
METACACHING = 5 * MIN       # caching duration for meta mode check
TEMPCACHING = 2 * MIN       # caching duration for temperature check
MAIN_TIMING  = 15 * MIN     # main looprefreshing
CONFORT = "confort"         # confort meta mode
ECO = "eco"                 # eco meta mode
UNKNOW = "unknow"           # unknow meta mode
MAX_DELTA_TEMP = 0.2        # maximum temperature span between 2 simultaneous measurement for filtering (in °C)
LM35_INTERVAL = 0.01        # interval in sec between 2 measure for filtering temperature measurement
