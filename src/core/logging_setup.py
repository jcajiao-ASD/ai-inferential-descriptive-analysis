"""
Logging setup module for the application.

This module configures the logging system with console and file handlers,
each with different logging levels and formats.
"""

import logging
import sys

from src.core.config import settings


def setup_logging():
    """
    Configure the application's logging system.

    Set up console and file handlers with different logging levels.
    Avoid re-adding handlers on reload.
    """
    root_logger = logging.getLogger()

    if root_logger.handlers:
        return

    root_logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    file_handler = logging.FileHandler(settings.logs_file_name)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
