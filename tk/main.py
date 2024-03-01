from controller import Controller
from util.fullog import Full_Log
import logging


def main():
    """ main """
    Full_Log("tksteg")
    c = Controller()
    logging.info("Starting")
    c.run()
    logging.info("Stopping")


if __name__ == '__main__':
    main()
