# -*- coding: utf-8 -*-
""" Meteo provides acess to distant meteo service
    Initialisation of connexion is done at module importation
"""

import logging
import CST as CST #we must import the module, not import CST from CST, to get accesss to constant defined in other modules
import Sun_levels

class Meteo(object):
    def outside_humidity(self):
        """ :return: current outside humidity percentage, from 0 to 100 """
        return 50  # FIXME : temporary stub

    def outside_temperature(self):
        """ :return: current outside temperature in celsius grade """
        return 20  # FIXME : temporary stub
        
    def outside_sun_level(self):
        """ :return: current outside sun level, SUN_NONE, SUN_LOW, SUN"""
        return CST.SUN_NONE  # FIXME : temporary stub
