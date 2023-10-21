# -*- coding: utf-8 -*-
import json
import logging
import threading
from .ActionSequencer import Action, ActionSequencer
from .DecisionMaker import DecisionMaker
from .CloudManager import CloudManager
from .Rolling import Rolling
from .CST import CST
from .RGB_Displayer import RGB_Displayer
from . import WatchFile

# import Log_to_html #this will start html interface to log file

CST.DEBUG_STATUS = "debug.json"
CST.DEBUG_KEY = "debug_mode"
""" a file may contain a debug_mode boolean to activate debug logging
   this file is not under git conf to allow local overwriting of the status, debug will be false if no file available
"""
sequencer = ActionSequencer()  # must be global to remain alive at the end of main
decider: DecisionMaker = None


def main(app):
    print("=== radiator main() started")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    level = logging.DEBUG if _get_debug_status() else logging.INFO
    logging.basicConfig(filename=CST.LOG_FILE, level=level, format='%(asctime)s %(message)s')
    logging.info('!!!!! Started !!!!!!')
    print("!!!!! Started !!!!!!")
    global decider  # must be global to remain alive at the end of main
    decider = DecisionMaker()
    global cloudManager  # must be global to remain alive at the end of main
    cloudManager = CloudManager()
    makeDecision = Action(action=decider.make_decision, duration=CST.MAIN_TIMING)
    print("===TIMING ", CST.MAIN_TIMING)
    mainSeq = Rolling([makeDecision])
    global sequencer  # must be global to remain alive at the end of main
    logging.debug("ready to start maln sequencer")
    sequencer.start(mainSeq)
    print("Main sequenceur started")


def _get_debug_status():
    """
      :return: debug status  from the file
      if file opening fails, return false
    """
    # ouvrir le fichier
    try:
        with open(CST.DEBUG_STATUS) as debug_load:
            debug = json.load(debug_load)
            res = debug[CST.DEBUG_KEY]
    except Exception as err:
        # soit le fichier n'a pu être lu, soit le dictionnaire n'est pas complet
        logging.error(err)
        res = False
    return res


def start_radiator(app, avoid_flash: bool = False):
    global s
    # display flashing sequence to confirm reboot
    if avoid_flash:
        print("staring without flash")
        main(app)
    else:
        displayer = RGB_Displayer()
        seq = Rolling([Action(displayer.setColorGreen, 2),
                       Action(displayer.turnOff, 2)])
        s = ActionSequencer()
        s.start(seq)

        # start main sequencer and stop flashing
        def go():
            s.cancel()
            main(app)

        timer = threading.Timer(12, go)
        timer.start()


if __name__ == '__main__':
    start_radiator()

    # start WatchFile (will reboot if wifi connexion lost)
    WatchFile.configure(fileName=CST.USER_JSON)
    WatchFile.start()
