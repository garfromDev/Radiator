# -*- coding: utf-8 -*-
import const as CST
import ftplib as ftplib
import logging

class DistantFileInterface(object):
  def __init__(self):
    pass
    
  def configure(self, server, path, login, pswd):
    self._server=server
    self._path = path
    self._login = login
    self._pswd = pswd
    
  def fetch(self, fileName):
    with ftplib.FTP(self._server, self._login, self._pswd) as ftp:
      ftp.cwd(path)
      with open(fileName, 'wb') as f:
        try ftp.retrbinary('RETR ' + fileName, f.write)
        except error:
          logging.error("failure ftp retrieval of " + fileName + "  "+error.message)
          pass
      ftp.quit()
