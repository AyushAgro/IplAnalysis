import logging
import functools
import os
import sys
import yaml
from yaml.loader import SafeLoader


# To print log we simply create a log_decorator.
# which take function as argument.
def log_decorator(_func=None):
    global logger_obj  # accessing logger_obj

    def log_decorator_info(_func=None):  # wrapper function

        @functools.wraps(_func)  # for docs, name
        def log_decorator_wrapper(*args, **kwargs):

            logger_obj.info(f"Begin function {_func.__name__}")  # To add function
            value = None

            try:
                value = _func(*args, **kwargs)  # passing all arguments and keywords arguments
                # if function is finished with no exception
                logger_obj.info(f"Ended function : {_func.__name__}")

            except Exception as e:  # if something goes wrong it won't stop the program but will simple add it to log
                logger_obj.error(f"Exception: {str(sys.exc_info()[1])}")
                pass

            return value

        return log_decorator_wrapper  # just return wrapper function

    if not _func:  # if function is not specify
        return log_decorator_info
    else:
        return log_decorator_info(_func)


# User Format of how each log will be return in log file
class CustomFormatter(logging.Formatter):
    def format(self, record):
        return super(CustomFormatter, self).format(record)


# First we need to create a logger_obj which we use to write into our log file
# it will be called just onces and create a log file we not present or if present it will delete it content
def get_logger(log_file_name, log_sub_dir="log"):
    log_dir = os.path.join(os.getcwd(), log_sub_dir)

    # check if log directory is present or not
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # you can use datetime.now()to write log file current time as filename
    log_file_name = os.path.join(log_dir, (str(log_file_name)))

    # this was write so that if there is any data present in log file before hand it will be erase
    f = open(log_file_name, "w")
    f.truncate()
    f.close()

    # creating log_obj with some configuration.
    logger = logging.Logger(log_file_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_file_name, "a+")
    handler.setFormatter(
        CustomFormatter("%(asctime)s - %(levelname)-10s  - %(message)s")
    )
    logger.addHandler(handler)
    return logger


# just checking for config file
if os.path.exists(os.path.join(os.getcwd(), 'config.yaml')):
    with open("config.yaml") as f:
        data = yaml.load(f, Loader=SafeLoader)
        log_file = data["File"]["log_file"]
else:
    log_file = 'std.log'

# creating our logger_obj
logger_obj = get_logger(log_file)
