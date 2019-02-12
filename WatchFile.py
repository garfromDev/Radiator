# -*- coding: utf-8 -*-
from os import os.path.getmtime
import threading
import time
import os


#default parameter, to be modified directly or using configure()
delay = 30 * 60
timeBetweenCheck = 2 * 60 * 60
fileToWatch = None
maxRetry = 3
reboot = performReboot

_retryNb = 0
_watchTimer = None

def configure( fileName, action = performReboot, maxRetry = 3, timeBetweenCheck = 2*60*60, delay = 30*60):
  """
    Configure the module
    :param str fileName: the file to check (including path)
    :param function action: the action to be executed if file has timed out
    :param int maxRetry: nb of retry before triggering action
    :param int timeBetweenCheck: time in sec. bewteen each check of the file modification date
    :param int delay: max time allowed in sec. since last modification of the file
  """
  fileToWatch = fileName
  WatchFile.reboot = action
  WatchFile.maxRetry = maxRetry
  WatchFile.timeBetweenCheck = timeBetweenCheck
  WatchFile.delay = delay
  

def check():
  """
    check if the file is not modified since more than delay
    after maxRetry tentative, will trigger action
  """
  if _checkFile():
    _retryNb = 0
    return
  #file outDated  
  _retryNb += 1
  if _retryNb > maxRetry:
    reboot()
  # launch again timer for next check  
  _watchTimer.start()
  
  
def performReboot():
  os.system('reboot')
  
  
def _checkFile():
"""
Check if last modification of fileToWatch is more recent than delay (in sec.)

:return: True if last modification is more recent
:rtype: bool
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
  
  _watchTimer = threading.Timer(timeBetweenCheck, check)
  _watchTimer.start()
 
 
if __name__ == '__main__':
  print("preparing manual test")
  #create dummy file
  os.system('touch testWatchFile.dummy')
  sleep(2)
  def sayDone:
    print("simulating reboot...")
  configure(fileName = "testWatchFile.dummy",
            action = sayDone,
            maxRetry = 1,
            timeBetweenCheck = 1,
            delay = 1)
  print("starting...")
  start()
  
    
 
