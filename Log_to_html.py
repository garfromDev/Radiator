# -*- coding: utf-8 -*-
import logging
import os
import re
import SimpleHTTPServer
import SocketServer
import threading

import CST as CST

CST.HTTP_PORT = 8000
CST.HTML_HEADER = 'header.html'
CST.HTML_FILE = 'index.html' #default file served by simple HTTP server

"""
This module will (upon import, no configuration needed):
- launch a simple HTTP server to serve index.html from current directory
- provide a function to convert Radiator log file to index.html file
- perform conversion upon timer
"""

def convert_to_html(line_nb):
    """
    The log file is made of line with input value and line with decision made,
    in debug mode there could be other lines intercaled
    """
    try:
        with open(log_file) as f:
            with open(CST.HTML_FILE) as h:
                back_x_lines(f, line_nb)
                write_header(h)
                line = find_input_value_line(f)
                while line != '' #end of file reached
                    h.write(to_html_from_input_value(line))
                    line = find_decision_taken_kine(f)
                    h.write(to_html_from_decision_made(line))         
    except IOError as err:
      logging.error("convert_to_html fails to convert %s to %s",
                    log_file,
                    CST.HTML_FILE) 
            
def write_header(html_file):
    with open(CST.HTML_HEADER) as hdr:
        html_file.write(hdr.read())
        
def find_input_value_line(f):
    """find the next line in file f that match the expression
    and return it
    :param f: the file object
    :return: the line, empty string if end of line reached"""
    inp_val = re.compile("""
        ^\S+ #début de ligne suivi de quelque chose (la date)
        \s+  #un ou des espaces
        \S+  #l'heure
        \s+  #un ou des espaces
        makeDecision
        \s+  #un ou des espaces
        metamode
        \s+  #un ou des espaces
        =""", re.VERBOSE)
    reached = false
    while not reached:
        l = f.readline()
        reached = (l =='') or  inp_val.match(l)
    return l


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

    
def to_html_from_input_value(line):
    dict = get_dict_from_log_line(line)
    if dict['feltCold'] : 
        dict['felt'] = 'cold'
    if dict['feltHot'] : 
        dict['felt'] = 'hot' 
    if dict['feltSuperHot'] : 
        dict['felt'] = 'super hot'
    
    for k in ['metamode', 'temp', 'light', 'user_action', 'felt' ]:
        pass
    
"""
line = "2019-03-09 11:47:37,962 makeDecision metamode = confort temp = 20.1 Bonus = False feltCold = False feltHot = True feltSuperHot = False userDown = False overruled = False overMode = confort"
import re
r = re.compile("[\S]+ = [\S]+")
print(r.findall(line))
k = [ x.split()[0] for x in r.findall(line) ]
v = [ x.split()[2] for x in r.findall(line) ]
d = dict(zip(k,v))
print(d)
"""


threading.timer(CST.MAIN_TIMING, 
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", CST.HTTP_PORT), Handler)
logging.info("starting HTTP server on port %s",CST.HTTP_PORT)
httpd.serve_forever()
