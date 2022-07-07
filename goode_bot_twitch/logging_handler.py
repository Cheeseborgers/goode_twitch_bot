"""This module handles all logging throughout the application"""
import logging
import os

from dotenv import load_dotenv

load_dotenv()


def get_bot_logger(name):
    """
    Returns the instance of the logger.

    :param name: The app name given to the logger
    :return: The logger instance
    """
    file_formatter = logging.Formatter(os.environ.get("FILE_LOG_FORMAT"))
    console_formatter = logging.Formatter(os.environ.get("CONSOLE_LOG_FORMAT"))

    # File handler -------------------------------------------------------------
    file_handler = logging.FileHandler(os.environ.get("MAIN_LOG_FILENAME"))

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
