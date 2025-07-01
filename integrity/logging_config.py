import logging
import os
from datetime import datetime


def setup_logger(name='file_intergrity_checker', log_dir="logs", log_level=logging.INFO):

    # ensure the logs directory exists
    os.makedirs(log_dir, exist_ok=True)

    log_filename = f"{log_dir}/activity.log"

    # create and configure the logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # prevent adding multiple handlers if setup_logger is called again
    if not logger.handlers:
        # console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # file handler
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(log_level)

        # formatter
        formatter = logging.Formatter(
            '%(asctime)s — %(levelname)s — %(name)s — %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # add handlers to logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
