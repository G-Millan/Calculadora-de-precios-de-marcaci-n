"""
Logging configuration module.

Provides centralized logging setup for the entire application.
"""

import logging
from pathlib import Path
from typing import Optional

import config


def setup_logger(
    name: str,
    log_file: Optional[Path] = None,
    level: str = "INFO",
) -> logging.Logger:
    """
    Set up a logger with both file and console handlers.

    Args:
        name: Logger name (typically __name__)
        log_file: Path to log file (defaults to config.LOG_FILE)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    if log_file is None:
        log_file = config.LOG_FILE

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # File handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(getattr(logging, level.upper()))
    file_formatter = logging.Formatter(
        config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT,
    )
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_formatter = logging.Formatter(
        "%(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Global logger instance
logger = setup_logger(__name__, level=config.LOG_LEVEL)
