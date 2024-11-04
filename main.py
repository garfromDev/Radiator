# -*- coding: utf-8 -*-
import json
import logging
import threading
from flask_apscheduler import APScheduler
from Radiator.UserInteractionManager import UserInteractionManager
from app import models
from .ActionSequencer import Action, ActionSequencer
from .DecisionMaker import DecisionMaker
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
scheduler = APScheduler()


@scheduler.task('interval', id='make_decision', seconds=5, misfire_grace_time=900)
def periodic_make_decision()-> None:
    print("periodic_make_decision")
    with scheduler.app.app_context():
        decider = DecisionMaker(user_manager=UserInteractionManager(user_interaction_provider=models.UserInteraction()))
        print("décision prise : ", decider.make_decision())


def main(app):
    scheduler.init_app(app)
    scheduler.start()
    print("=== radiator main() started")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    level = logging.DEBUG if _get_debug_status() else logging.INFO
    logging.basicConfig(filename=CST.LOG_FILE, level=level, format='%(asctime)s %(message)s')
    logging.info('!!!!! Started !!!!!!')
    print("!!!!! Started !!!!!!")



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
        print("starting without flash")
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
