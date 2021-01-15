import sys
import logging

from functools import wraps


def log_control(func):
    @wraps
    def wrapper(*args, **kwargs):
        c = kwargs.get("log")
        if c:
            init_log()

        func()

    return wrapper


def init_log():
    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s %(levelname)s:%(lineno)d:%(process)d:%(message)s",
        datefmt="%m/%d %H:%M:%S",
        level=logging.INFO
    )
