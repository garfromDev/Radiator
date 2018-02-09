# -*- coding: utf-8 -*-

class HalfHour:
  def __init__(self, hour, metaMode):
    if hour > 48 or hour < 0 or (hour mod 2 != 0):
      raise ValueError('invalid half hour definition')
    self.hour = hour
    self.metaMode = metaMode

class HeatCalendar:

  def setWeekCal(self, week):
  
