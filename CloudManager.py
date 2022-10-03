# -*- coding: utf-8 -*-
import logging
import json

from .CST import CST
from .DistantFileInterface import DistantFileInterface

CST.PSWD_INFO = "pswd.json"


class CloudManager(object):
    """
  This object allow to fetch the calendar and user decision file from the server
  using the DistantFileInterface
  """

    def __init__(self, distantFileInterface=DistantFileInterface(),
                 userDecisionFileName=CST.USER_JSON,
                 weekCalendarFileName=CST.WEEKCALJSON):
        self._distantFileInterface = distantFileInterface
        if CST.FTP_LOGIN:  # avoid using not initialized constant if get_pswd() failed
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


def get_pswd(f):  #  this is a module function, not part of the class
    """
  Open the file named CST.PSW_INFO and get login information
  file is json dictionary with keys :
  ftp_pswd, ftp_server, ftp_path, ftp_login
  value are loaded into CST
  In case of errors reading/decoding the file, CST.FTP_LOGIN is set to None
  """
    try:
        with open(f) as pwd:
            content = json.load(pwd)
            CST.FTP_PSWD = content["ftp_pswd"]
            CST.FTP_SERVER = content["ftp_server"]
            CST.FTP_PATH = content["ftp_path"]
            CST.FTP_LOGIN = content["ftp_login"]
    except (IOError, ValueError) as error:
        logging.error("Cloud Manager not able to open or decode %s - %s", CST.PSWD_INFO, error)
        CST.FTP_LOGIN = None


# the login information are loaded at importation of the module  
get_pswd(CST.PSWD_INFO)

if __name__ == '__main__':
    print("testing CloudManager manually")
    test = CloudManager()
    test.update()
    print("succesfull")
