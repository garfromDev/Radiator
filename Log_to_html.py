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
CST.HTML_FOOTER = 'footer.html'
CST.HTML_FILE = 'index.html'  # default file served by simple HTTP server
CST.NB_OF_LOG_LINES = 10 #nb of status log lines served as HTML

"""
This module will (upon import, no configuration needed):
- launch a simple HTTP server to serve index.html from current directory
- provide a function to convert Radiator log file to index.html file
- perform conversion upon timer
"""

def convert_to_html(log_file, line_nb):
    """
    The log file is made of line with input value and line with decision made,
    in debug mode there could be other lines intercaled
    """
    try:
        with open(log_file) as f:
            with open(CST.HTML_FILE, 'w') as h:
                back_x_lines(f, line_nb)
                write_header(header=CST.HTML_HEADER, to=h)
                line=f.readline()
                while line != '':  # end of file reached
                    line = find_input_value_line(f)
                    h.write(to_html_from_input_value(line))
                    line = find_decision_taken_line(f)
                    h.write(to_html_from_decision_made(line)+"\n")
                write_header(header=CST.HTML_FOOTER, to=h)
    except IOError as err:
        logging.error("convert_to_html fails to convert %s to %s",
                      log_file,
                      CST.HTML_FILE)


def write_header(header, to):
    with open(header) as hdr:
        to.write(hdr.read())


def find_input_value_line(f):
    """find the next line in file f that match the expression
    and return it
    :param f: the file object
    :return: the line, empty string if end of file reached"""
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
    return find_line_matching(f, inp_val)


def find_decision_taken_line(f):
    """ find the line explaining which decision has been taken
    :return: the line, empty string if end of file reached
    """
    dec = re.compile(r".+Heating mode applied \:")
    return find_line_matching(f, dec)


def find_line_matching(f, expr):
    reached = False
    while not reached:
        l = f.readline() #empty string if EOF
        reached = (l == '') or expr.match(l)
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
    output = "<p>"
    if not dict:
      return output
    print("Dictionaire from log ------------>  ", dict)
    if dict['feltcold']:
        dict['felt'] = 'cold'
    if dict['felthot']:
        dict['felt'] = 'hot'
    if dict['feltsuperhot']:
        dict['felt'] = 'super hot'
    if dict['overruled']:
        if dict['bonus']:
            dict['user_action'] = 'user cold'
        elif dict['userdown']:
            dict['user_action'] = 'user hot'
        else:
            dict['user_action'] = dict['overMode']
    for k, pad in [('metamode', 8),
                   ('temp', 4),
                   ('light', 5),
                   ('user_action', 10),
                   ('felt', 6)]:
        output += "  " + format(dict[k], "<{}".format(pad))
    return output


def to_html_from_decision_made(line):
    mode_exp = re.compile(r"applied : (\w+)")
    found = mode_exp.search(line)
    mode = found.groups()[0] if found else ""
    return format(mode, "<{}".format(8)) + "</p>"


def get_dict_from_log_line(line):
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
    threading.timer(CST.MAIN_TIMING, start_generating).start()


start_generating()
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", CST.HTTP_PORT), Handler)
logging.info("starting HTTP server on port %s", CST.HTTP_PORT)
httpd.serve_forever()

""" idea to have graph served through HTML :
https://pythonspot.com/flask-and-great-looking-charts-using-chart-js/
to have scrollable table:
 https://forum.alsacreations.com/topic-4-62439-1-TABLE--Scrollable-TBODY-and-fixed-THEAD-reloaded.html
"""
