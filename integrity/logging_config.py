import logging
import os
from datetime import datetime

def setup_logger(name='file_intergrity_checker', log_dir="logs", log_level=logging.INFO):
    """
    Configures and returns a logger that logs both to console and a file.

    Parameters:
    - name (str): The name of the logger instance.
    - log_dir (str): Directory where the log file will be stored.
    - log_level (int): Logging level (e.g., logging.INFO, logging.DEBUG).

    Returns:
    - logging.Logger: Configured logger instance.
    """

    # Ensure that the directory for storing logs exists
    os.makedirs(log_dir, exist_ok=True)

    # Define the log file path
    log_filename = f"{log_dir}/activity.log"

    # Create a logger instance (or get existing one)
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Avoid adding handlers multiple times if the logger is reused
    if not logger.handlers:
        # Create a console handler to show logs in terminal
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Create a file handler to save logs in a file
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(log_level)

        # Define a consistent log message format
        formatter = logging.Formatter(
            '%(asctime)s — %(levelname)s — %(name)s — %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Attach formatter to both handlers
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add both handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
