# -*-coding: utf-8 -*-
"""
This module will (upon import, no configuration needed):
- launch a simple HTTP server to serve index.html from current directory                                                                                                                  - provide a function to convert Radiator log file to index.html file
- perform conversion upon timer
"""

import logging
from os.path import getmtime
import os
import re
import SimpleHTTPServer
import SocketServer
import threading
import time

from CST import CST


CST.HTTP_PORT = 8000
CST.HTML_HEADER = 'header.html'
CST.HTML_FOOTER = 'footer.html'
CST.HTML_FILE = 'index.html'  # default file served by simple HTTP server
CST.NB_OF_LOG_LINES = 30 #nb of status log lines served as HTML (not all lines are lines with value)


def convert_to_html(log_file, line_nb):
    """
    The log file is made of line with input value and line with decision made,
    in debug mode there could be other lines intercaled
    """
    try:
        with open(log_file) as f:
            with open(CST.HTML_FILE, 'w') as h:
                _back_x_lines(f, line_nb)
                _write_header(header=CST.HTML_HEADER, to=h)
                h.write("<p>last update : {}</p>".format( _get_date_of(log_file) ))
                line=_find_input_value_line(f)
                line_completed = False
                while line != '':  # end of file reached
                    if _is_input_value(line):
                        if not line_completed:
                            h.write("<td> </td></tr>\n")
                        h.write(_to_html_from_input_value(line))
                        line_completed = False
                    elif _is_decision_taken(line):
                        h.write(_to_html_from_decision_made(line)+"\n")
                        line_completed = True
                    line=f.readline()
                _write_header(header=CST.HTML_FOOTER, to=h)
    except IOError as err:
        logging.error("convert_to_html fails to convert %s to %s",
                      log_file,
                      CST.HTML_FILE)


def _write_header(header, to):
    with open(header) as hdr:
        to.write(hdr.read())

def _get_date_of(file):
    """ :return: the date of last file access in local time as string
    crash if file do not exist, this shall not be the case in this module
    """
    t = getmtime(file)
    return time.ctime(t)

def _find_input_value_line(f):
    """find the next line in file f that match the expression
    and return it
    :param f: the file object
    :return: the line, empty string if end of file reached"""
    line=f.readline()
    while not (_is_input_value(line) or line==''):
        line=f.readline()
    return line


def _is_input_value(line):
    """check if the line in match the expression
    wiche means it is a log line about decision made
    :param line: the line to check as string
    :return: True or False"""
    inp_val = re.compile(r"""
        ^\S+ #début de ligne suivi de quelque chose (la date)
        \s+  #un ou des espaces
        \S+  #l'heure
        \s+  #un ou des espaces
        makeDecision
        \s+  #un ou des espaces
        metamode
        \s+  #un ou des espaces
        =""", re.VERBOSE)
    return True if inp_val.search(line) else False


def _is_decision_taken(line):
    """ check if the line is explaining which decision has been taken
    :return: True or False
    """
    dec = re.compile(r".+Heating mode applied \:")
    return True if dec.search(line) else False


def _find_line_matching(f, expr):
    reached = False
    while not reached:
        l = f.readline() #empty string if EOF
        reached = (l == '') or expr.match(l)
    return l

def _back_x_lines(f, lines):
    f.seek(0, os.SEEK_END)
    for _ in xrange(lines):
        if not _back_one_line(f):
            break


def _back_one_line(f):
    try:
        f.seek(-2, os.SEEK_CUR)
        while f.read(1) != b"\n":   # Until EOL is found...
            f.seek(-2, os.SEEK_CUR)
    except IOError:
        return False
    else:
        return True


def _to_html_from_input_value(line):
    dict = _get_dict_from_log_line(line)
    output = "<tr>"
    if not dict:
      return output
    logging.debug("Dictionaire from log ------------> %s ", dict)
    dict['felt'] = 'normal'
    if eval(dict['feltcold']):
        dict['felt'] = 'cold'
    if eval(dict['felthot']):
        dict['felt'] = 'hot'
    if eval(dict['feltsuperhot']):
        dict['felt'] = 'super hot'
    dict['user_action']='' #default value
    if eval(dict['overruled']):
        if eval(dict['bonus']):
            dict['user_action'] = 'user cold'
        elif eval(dict['userdown']):
            dict['user_action'] = 'user hot'
        else:
            dict['user_action'] = dict['overMode']
    for k, pad in [('metamode', 8),
                   ('temp', 4),
                   ('light', 5),
                   ('user_action', 10),
                   ('felt', 6)]:
        output += "<td>" + dict[k]+ "</td>"
    return output


def _to_html_from_decision_made(line):
    mode_exp = re.compile(r"applied : (\w+)")
    found = mode_exp.search(line)
    mode = found.groups()[0] if found else ""
    return "<td>"+mode+"</td></tr>"


def _get_dict_from_log_line(line):
    r = re.compile(r"[\S]+ = [\S]+")
    k = [x.split()[0].lower() for x in r.findall(line)] #all keys are lowered
    v = [x.split()[2] for x in r.findall(line)]
    d = dict(zip(k,v))
    return d if len(d)>1 else None


"""
line = "2019-03-09 11:47:37,962 makeDecision metamode = confort temp = 20.1
Bonus = False feltCold = False feltHot = True feltSuperHot = False userDown = False overruled = False overMode = confort"
import re
r = re.compile(r"[\S]+ = [\S]+")
print(r.findall(line))
k = [ x.split()[0] for x in r.findall(line) ]
v = [ x.split()[2] for x in r.findall(line) ]
d = dict(zip(k,v))
print(d)
"""

def update_html():
    convert_to_html(log_file=CST.LOG_FILE, line_nb=CST.NB_OF_LOG_LINES)

def start_generating():
    update_html()
    threading.Timer(CST.MAIN_TIMING, start_generating).start()

if __name__ == '__main__':
    print("converting log file to html, server and timer will not be started...")
    update_html()
else:
    start_generating()
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", CST.HTTP_PORT), Handler)
    logging.info("starting HTTP server on port %s", CST.HTTP_PORT)
    threading.Thread(target=httpd.serve_forever).start()

""" idea to have graph served through HTML :
https://pythonspot.com/flask-and-great-looking-charts-using-chart-js/
to have scrollable table:
 https://forum.alsacreations.com/topic-4-62439-1-TABLE--Scrollable-TBODY-and-fixed-THEAD-reloaded.html
"""
