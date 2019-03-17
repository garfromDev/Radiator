# -*- coding: utf-8 -*-
import ftplib as ftplib
import logging


class DistantFileInterface(object):

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
    try:
      ftp =  ftplib.FTP(self._server, self._login, self._pswd)
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
  testFtp.configure(server="perso-ftp.orange.fr",
                    path="/Applications/Radiator",
                    login="fromontaline@orange.fr",
                    pswd="orange3310")
  testFtp.fetch('userInteraction.json')

