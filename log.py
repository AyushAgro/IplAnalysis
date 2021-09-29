import logging
import functools
import os
import sys
from inspect import getframeinfo, stack
import yaml
from yaml.loader import SafeLoader


def log_decorator(_func=None):
    global logger_obj

    def log_decorator_info(_func=None):
        @functools.wraps(_func)
        def log_decorator_wrapper(*args, **kwargs):
            logger_obj.info(f"Begin function {_func.__name__}")
            value = None
            try:
                value = _func(*args, **kwargs)
                logger_obj.info(f"Ended function : {_func.__name__}")
            except:
                logger_obj.error(f"Exception: {str(sys.exc_info()[1])}")
                pass
            return value
        return log_decorator_wrapper

    if not _func:
        return log_decorator_info
    else:
        return log_decorator_info(_func)


class CustomFormatter(logging.Formatter):
    def format(self, record):
        return super(CustomFormatter, self).format(record)

def get_logger(log_file_name, log_sub_dir="log"):
    log_dir = os.path.join(os.getcwd(), log_sub_dir)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file_name = os.path.join(log_dir, (str(log_file_name)))

    f = open(log_file_name, "w")
    f.truncate()
    f.close()

    logger = logging.Logger(log_file_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_file_name, "a+")
    handler.setFormatter(
        CustomFormatter("%(asctime)s - %(levelname)-10s  - %(message)s")
    )
    logger.addHandler(handler)
    return logger


with open("config.yaml") as f:
    data = yaml.load(f, Loader=SafeLoader)
    log_file = data["File"]["log_file"]

logger_obj = get_logger(log_file)
