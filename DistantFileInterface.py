# -*- coding: utf-8 -*-
import ftplib as ftplib
import logging


class DistantFileInterface(object):

  def __init__(self):
    self._server=None #cannot be used until configure() is called
    
  def configure(self, server, path, login, pswd):
    self._server=server
    self._path = path
    self._login = login
    self._pswd = pswd


  def fetch(self, fileName):
    """
      Will always fetch distant file unrespective of the date and overwrite local file
      Does nothing in case of error (connexion, not existing file, ...
    """
    if not self._server:
      return #configuration not done

    try:
      ftp =  ftplib.FTP_TLS(self._server, self._login, self._pswd)
      ftp.prot_p()
      ftp.cwd(self._path)
    except Exception as err:
      logging.error("failure ftp connexion "+repr(err))
      return
    with open(fileName, 'wb') as f:
      try:
        ftp.retrbinary('RETR ' + fileName, f.write)
      except:
        logging.error("failure ftp retrieval of " + fileName)
      finally:
        ftp.quit()


if __name__ == '__main__':
  print("testing ftp manually")
  testFtp=DistantFileInterface()
  testFtp.configure(server="",
                    path="/Applications/Radiator",
                    login="",
                    pswd="")
  testFtp.fetch('userInteraction.json') #should return silently doing nothing
