# -*- coding: utf-8 -*-
import logging
import SimpleHTTPServer
import SocketServer

from CST import CST

CST.HTTP_PORT = 8000

"""
This module will (upon import, no configuration needed):
- launch a simple HTTP server to serve index.html from current directory
- provide a function to convert Radiator log file to index.html file
- perform conversion upon timer
"""

def convert_to_html( log_file, line_nb):
  

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", CST.HTTP_PORT), Handler)
Logging.info("starting HTTP server on port %s",CST.HTTP_PORT)
httpd.serve_forever()
