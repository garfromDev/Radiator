# -*- coding: utf-8 -*-
import logging
from CST import CST
from DistantFileInterface import DistantFileInterface
CST.PSWD_FILE
CST.FTP_SERVER = "perso-ftp.orange.fr"
CST.FTP_PATH = "/Applications/Radiator"
CST.FTP_LOGIN = "fromontaline@orange.fr"
CST.FTP_PSWD = "orange3310"


class CloudManager(object):
  """
    This object allow to fetch the calendar and user decision file from the server
    using the DistantFileInterface
  """

  def __init__(self,distantFileInterface=DistantFileInterface(),
               userDecisionFileName = CST.USER_JSON,
               weekCalendarFileName = CST.WEEKCALJSON):
    self._distantFileInterface=distantFileInterface
    self._distantFileInterface.configure(server=CST.FTP_SERVER,
                                         path=CST.FTP_PATH,
                                         login=CST.FTP_LOGIN,
                                         pswd=CST.FTP_PSWD)
    self._userDecisionFileName = userDecisionFileName
    self._weekCalendarFileName = weekCalendarFileName


  def update(self):
    """
      fetch the file from distant location using provided DistantFileInterface
      file will be saved in local directory with same name, overwriting without warning

    """
    self._distantFileInterface.fetch(self._weekCalendarFileName)
    self._distantFileInterface.fetch(self._userDecisionFileName)


def get_pswd():
  with open(CST.PSWD_INFO) as pwd:
    content = json.load(pwd)
    print(content)
  CST.FTP_PSWD = content["ftp_pswd"]
    
    
if __name__ == '__main__':
  print("testing CloudManager manually")
  test = CloudManager()
  test.update()
  print("succesfull")
