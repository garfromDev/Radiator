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

if __name__ == '__main__':
  print("testing ftp manually")
  var testFtp=DistantFileInterface()
  testFtp.configure(server="ftp://ftp://perso-ftp.orange.fr",
                    path="/Applications/maxouf14/Parameters",
                    login="fromontaline@orange.fr,
                    pswd="orange3310")
  ftp.fetch('userDecision.json')
  
