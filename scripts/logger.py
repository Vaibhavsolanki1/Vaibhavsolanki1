"""
GitHub Profile 2.0 - Standard Logger

Configures structured console logging across engine modules.
"""

import logging
import sys


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Instantiate or retrieve a named logger configured with a standard formatter."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, level.upper(), logging.INFO))

        formatter = logging.Formatter(
            "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
