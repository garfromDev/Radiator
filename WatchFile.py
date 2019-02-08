# -*- coding: utf-8 -*-
from os import os.path.getmtime
import threading
import time

#default parameter, to be modified directly or using configure()
delay = 30 * 60
timeBetweenCheck = 2 * 60 * 60
fileToWatch = None
maxRetry = 3

_retryNb = 0
_watchTimer = None

def configure( fileName):
  pass

def check():
  if _checkFile():
    _retryNb = 0
    return
    

  _retryNb++
  if _retryNb >= maxRetry:
    
    
def _checkFile():
"""
Check if last modification of fileToWatch is more recent than delay (in sec.)

:return: True if last modification is more recent
"""
  t=0
  try:
    t = os.path.getmtime(fileToWatch)
  except: #file not accessible
    return False
  
  return (t - time.time()) < delay
  
  
def start():
  """
  This module will look for the last modification of the given file
  if the time since last modified is over delay, it fails
  if it fails more than maxRetry, rebbot will be triggered
  
  :return: true if parameter allows to run at least once
  """
  if delay == None or fileToWatch == None:
    return False
  
  _WatchTimer = threading.Timer(timeBetweenCheck, _check)
  _WatchTimer.start()
 
 
 
