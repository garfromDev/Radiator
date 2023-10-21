# -*- coding: utf-8 -*-
import threading
import logging
#  import inspect


# this object is an elementary couple action + time before next action (in sec.) to use with the Sequencer
# action : a function
# duration : in sec.
class Action:
    def __init__(self, action, duration):
        self.action = action
        self.duration = duration

    def __repr__(self):
        return f"{self.action and self.action.__name__ or ''} every {self.duration}"

# the sequencer will repeat each action, then wait for duration, rolling through the sequence of Action
class ActionSequencer:
    # sequence : a Rolling() collection of Action()
    def __init__(self, sequence=None):
        logging.debug("initialising sequencer %s with sequence %s", self, sequence)
        self.sequence = sequence
        self.timer = None

    # print("init sequencer ")

    # start the sequencer if a sequence is given, or shoot the next action (called by the timer from previous call)
    def start(self, sequence=None):
        logging.debug("start sequencer %s", self)
        # print("start sequencer ")
        # curframe = inspect.currentframe()
        # calframe = inspect.getouterframes(curframe, 2)
        # self._caller= calframe[1][3]
        # print("called by ", self._caller)
        if sequence is not None:
            self.cancel()  # Setting a new sequence cancel the previous one if there was one
            self.sequence = sequence
            # print("with new sequence")
        try:
            currentAction = self.sequence.get()
        except:
            logging.debug("sequencer %s did not find next action", self)
            self.timer = None  # not a Rolling we stop
            # print("unable to get next action -> timer stopped")
            return
        # print("will perform action",self._caller)
        try:
            logging.debug("perform action %s", currentAction.action.__name__)
            # print("perform action "+currentAction.action.__name__)
            currentAction.action()  # perform the first action
        except Exception as e:
            logging.debug("action failed : %s %s", currentAction, e)
            # print("action failed", self._caller)
            pass  # None or crashy, maybe next action will behave better

        # print("preparing next action", self._caller)
        try:
            dur = currentAction.duration
            self.timer = threading.Timer(dur, self.start)
            self.timer.start()  # this will call start() again after duration, which will perform the next action
            logging.debug("sequencer %s next action %s in %s", self, currentAction.action.__name__, dur)
            # print("next action in ")
            # print(currentAction.duration)
        except:
            # print("next action not launched", self._caller)
            self.timer = None  # duration not valid


    # stop the sequencer
    def cancel(self):
        # print("cancel sequencer")
        try:  # because timer may not exist
            self.timer.cancel()
        except:
            pass
