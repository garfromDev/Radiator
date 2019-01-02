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
    ftp =  ftplib.FTP(self._server, self._login, self._pswd)
    ftp.cwd(self._path)
    with open(fileName, 'wb') as f:
      try:
        ftp.retrbinary('RETR ' + fileName, f.write)
      except:
        logging.error("failure ftp retrieval of " + fileName)

    ftp.quit()


if __name__ == '__main__':
  print("testing ftp manually")
  testFtp=DistantFileInterface()
  testFtp.configure(server="perso-ftp.orange.fr",
                    path="/Applications/Radiator",
                    login="fromontaline@orange.fr",
                    pswd="orange3310")
  testFtp.fetch('userInteraction.json')

