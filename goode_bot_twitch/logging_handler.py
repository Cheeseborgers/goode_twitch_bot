"""This module handles all logging throughout the application"""
import logging
import logging.handlers
import os
from copy import copy

from dotenv import load_dotenv

load_dotenv()

MAPPING = {
    "DEBUG": 37,  # white
    "INFO": 36,  # cyan
    "WARNING": 33,  # yellow
    "ERROR": 31,  # red
    "CRITICAL": 41,  # white on red bg
}

PREFIX = "\033["
SUFFIX = "\033[0m"


class ColoredFormatter(logging.Formatter):
    """
    Coloured Logging formatter.
    """

    def __init__(self, pattern):
        logging.Formatter.__init__(self, pattern)

    def format(self, record):
        colored_record = copy(record)
        levelname = colored_record.levelname
        seq = MAPPING.get(levelname, 37)  # default white
        colored_levelname = f"{PREFIX}{seq}m{levelname}{SUFFIX}"
        colored_record.levelname = colored_levelname
        return logging.Formatter.format(self, colored_record)


def get_logger(name):
    """
    Returns the instance of the logger.

    @param: name: The app name given to the logger
    :return: The logger instance
    """

    file_formatter = logging.Formatter(os.environ.get("FILE_LOG_FORMAT"))
    console_formatter = ColoredFormatter(os.environ.get("CONSOLE_LOG_FORMAT"))

    # File handler - https://docs.python.org/3/howto/logging.html -------------
    # DEBUG: Detailed information, typically of interest only when
    # diagnosing problems.

    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.environ.get("TWITCH_BOT_LOG_FILENAME"),
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )

    if os.environ.get("DEBUG"):
        file_handler.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(logging.WARN)

    file_handler.setFormatter(file_formatter)

    # Console Handler - stdout ---------------------------------------------
    console_handler = logging.StreamHandler()

    if os.environ.get("DEBUG"):
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.WARN)

    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

    return logger
