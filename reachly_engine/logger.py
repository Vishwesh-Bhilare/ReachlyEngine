import logging
import sys
from reachly_engine.config import LOG_LEVEL

LOG_FORMAT = (
    "[%(asctime)s] "
    "[%(levelname)s] "
    "%(name)s: %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False
    return logger

