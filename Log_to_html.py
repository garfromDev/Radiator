# -*- coding: utf-8 -*-
import logging
import SimpleHTTPServer
import SocketServer
import os
import threading

class CST:
    pass

CST.HTTP_PORT = 8000

"""
This module will (upon import, no configuration needed):
- launch a simple HTTP server to serve index.html from current directory
- provide a function to convert Radiator log file to index.html file
- perform conversion upon timer
"""

def convert_to_html(line_nb):
    try:
        with open(log_file) as f:
            with open(CST.HTML_FILE) as h:
                back_x_lines(f, line_nb)
                write_header(h)
                for line in f.readlines():
                    h.write(to_html(line))
    except IOError as err:
      logging.error("convert_to_html fails to convert %s to %s",
                    log_file,
                    CST.HTML_FILE) 
            
      
def back_x_lines(f, lines):
    f.readline()
    f.seek(-2, os.SEEK_CUR)
    for _ in xrange(lines):
        if not back_one_line(f):
            break

def back_one_line(f):
    try:
        while f.read(1) != b"\n":   # Until EOL is found...
            f.seek(-2, os.SEEK_CUR)
    except IOError:
        return False
    else:
        return True


threading.timer(CST.MAIN_TIMING, 
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", CST.HTTP_PORT), Handler)
logging.info("starting HTTP server on port %s",CST.HTTP_PORT)
httpd.serve_forever()
