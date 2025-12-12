import logging
from logging.handlers import RotatingFileHandler

class Full_Log:
    """
        setup  full logging in a single call using a kind-of Façade pattern
    """
    def __init__(self, name=None, level=None):
        #
        # Get the root logger
        #
        logger = logging.getLogger()
        #
        #
        #
        if level is None:
            level = "INFO"
        level = level.strip().upper()
        level = logging.getLevelName(level)
        logger.setLevel(level)
        debug = logger.level == logging.DEBUG
        #
        # avoid to mention the module name in the log unless we are debugging
        #
        if debug:
            formatter = logging.Formatter('%(asctime)s *%(levelname)s* %(module)s %(message)s', "%Y-%m-%d %H:%M:%S")
        else:
            formatter = logging.Formatter('%(asctime)s *%(levelname)s* %(message)s', "%Y-%m-%d %H:%M:%S")
        file_handler = RotatingFileHandler(name + '.log', 'a', 100000, 3)
        #
        # Direct log messages to a file
        # 3 log files, 100K each, rotated
        #
        file_handler = RotatingFileHandler(name + '.log', 'a', 100000, 3)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        #
        # Direct the same log messages to stdout
        #
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
