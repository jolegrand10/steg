import os
import sys
from view import View
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from stegano import Stegano
import logging

logger = logging.getLogger(__name__)

class Controller:

    def __init__(self):
        self.stegano = Stegano()
        self.view = View(self, self.stegano)

    def run(self):
        self.view.run()


if __name__ == '__main__':
    from util.fullog import Full_Log
    Full_Log(name="Controller")
    logger.info("Starting interactive test with the Controller")
    Controller().run()
    logger.info("Ending interactive test with the Controller")
