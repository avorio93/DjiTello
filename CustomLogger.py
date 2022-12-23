import logging


class CustomLogger(logging.Formatter):

    LOG_COL_GREY = "\x1b[37;20m"
    LOG_COL_CYANO = "\x1b[36;20m"
    LOG_COL_YELLOW = "\x1b[33;20m"
    LOG_COL_RED = "\x1b[31;20m"
    LOG_COL_BOLD_RED = "\x1b[31;1m"
    LOG_COL_RESET = "\x1b[0m"
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    format = "%(name)s - %(asctime)s - [%(levelname)s] --> %(message)s"

    FORMATS = {
        logging.DEBUG: LOG_COL_GREY + format + LOG_COL_RESET,
        logging.INFO: LOG_COL_CYANO + format + LOG_COL_RESET,
        logging.WARNING: LOG_COL_YELLOW + format + LOG_COL_RESET,
        logging.ERROR: LOG_COL_RED + format + LOG_COL_RESET,
        logging.CRITICAL: LOG_COL_BOLD_RED + format + LOG_COL_RESET
    }

    def __init__(self, log_name: str):
        super().__init__()

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(self)
        self.logger.addHandler(console_handler)

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
