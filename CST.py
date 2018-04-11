# -*- coding: utf-8 -*-

# This utility module define constant
MIN         = 60            # conversion of minutes to second
WEEKCALJSON = "week.json"   # the file that defines the weekly calendar
STATUSJSON = "status.json"  # the file that define the current status (user Down, Overrule, ..)
JSON_PATH = "/home/pi/Program/Radiator" # the path to the weekly calendar
METACACHING = 5 * MIN       # caching duration for meta mode check
TEMPCACHING = 2 * MIN       # caching duration for temperature check
MAIN_TIMING  = 15 * MIN     # main looprefreshing

