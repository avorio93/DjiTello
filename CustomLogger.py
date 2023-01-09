####################################################################################################################
# IMPORTS
import logging
import sys
from logging.handlers import TimedRotatingFileHandler


class CustomLogger(logging.Formatter):
    ####################################################################################################################
    # GLOBALS

    # ---> Constants
    LOG_COL_GREY = "\x1b[37;20m"
    LOG_COL_CYANO = "\x1b[36;20m"
    LOG_COL_YELLOW = "\x1b[33;20m"
    LOG_COL_RED = "\x1b[31;20m"
    LOG_COL_BOLD_RED = "\x1b[31;1m"
    LOG_COL_RESET = "\x1b[0m"

    # ---> Attributes
    format = "%(asctime)s - [%(name)s] - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: LOG_COL_GREY + format + LOG_COL_RESET,
        logging.INFO: LOG_COL_CYANO + format + LOG_COL_RESET,
        logging.WARNING: LOG_COL_YELLOW + format + LOG_COL_RESET,
        logging.ERROR: LOG_COL_RED + format + LOG_COL_RESET,
        logging.CRITICAL: LOG_COL_BOLD_RED + format + LOG_COL_RESET
    }

    ####################################################################################################################
    # CORE

    # ---> Functions
    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self)
        return console_handler

    def get_file_handler(self):
        file_handler = TimedRotatingFileHandler(self.log_name, when='midnight')
        file_handler.setFormatter(self)
        return file_handler

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

    # ---> Constructor
    def __init__(self, log_name: str, write_file: bool):
        super().__init__()

        self.log_name = log_name
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)

        self.logger.addHandler(self.get_console_handler())
        if write_file:
            self.logger.addHandler(self.get_file_handler())
