"""
Logging utilities for the feature extraction system.
"""

import logging
import os


def setup_logging(
    log_file: str = "feature_extraction.log", console_level: int = logging.INFO
) -> logging.Logger:
    """
    Set up the logging system with both file and console handlers.

    Args:
        log_file: Path to the log file
        console_level: Logging level for the console output

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.handlers = []  # Clear any existing handlers

    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create file handler
    try:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)  # Always capture detailed logs in file
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except (IOError, PermissionError) as e:
        logger.error(f"Failed to create log file: {e}")
        logger.warning("Continuing without file logging")

    return logger


def get_console_level(verbose: bool = False, quiet: bool = False) -> int:
    """
    Determine the appropriate console logging level based on flags.

    Args:
        verbose: Whether to enable verbose logging (DEBUG level)
        quiet: Whether to enable quiet logging (ERROR level only)

    Returns:
        Appropriate logging level constant
    """
    if quiet:
        return logging.ERROR
    elif verbose:
        return logging.DEBUG
    else:
        return logging.INFO
