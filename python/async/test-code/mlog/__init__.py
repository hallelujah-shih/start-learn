import logging
from typing import Optional


def get_logger(name: Optional[str] = None) -> logging.Logger:
    if name is None:
        name = __name__
    return logging.getLogger(name)
