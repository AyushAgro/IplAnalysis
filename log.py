import logging
import functools
import os
import sys
import yaml
from yaml.loader import SafeLoader

orig_stdout = sys.stdout

def log_decorator(_func=None):
    global logger
    def log_decorator_info(_func=None):  # wrapper function
        @functools.wraps(_func)
        def log_decorator_wrapper(*args, **kwargs):

            logger.info(f"Begin function {_func.__name__}")  # To add function
            value = None
            try:
                value = _func(*args, **kwargs)
                logger.info(f"Ended function : {_func.__name__}")
            except KeyboardInterrupt:
                print('Hello user you have pressed ctrl-c button. So we are quiting Program')
                sys.exit()
            except Exception as e:  # if something goes wrong it won't stop the program but will simple add it to log
                logger.error(f"Exception: was raise during execution of {_func.__name__} and error is {str(e)}")

            return value
        return log_decorator_wrapper

    if not _func:
        return log_decorator_info
    else:
        return log_decorator_info(_func)


# User Format of how each log will be return in log file
class CustomFormatter(logging.Formatter):
    def format(self, record):
        return super(CustomFormatter, self).format(record)

# First we need to create a logger which we use to write into our log file
# it will be called just onces and create a log file if not created.
def get_logger(logFileName, log_sub_dir="log"):
    logDir = os.path.join(os.getcwd(), log_sub_dir)

    # check if log directory is present or not
    if not os.path.exists(logDir):
        os.makedirs(logDir)

    # you can use datetime.now()to write log file current time as filename
    logFileName = os.path.join(logDir, (str(logFileName)))

    # this was write so that if there is any data present in log file before hand it will be erase
    f = open(logFileName, "w")
    f.truncate()
    f.close()

    # creating log_obj with some configuration.
    logger = logging.getLogger(__name__)
    fileHandler = logging.FileHandler(logFileName, "a+")
    fileHandler.setLevel(logging.INFO)
    fileHandler.setFormatter(CustomFormatter("%(asctime)s - %(levelname)-10s  - %(message)s"))
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(orig_stdout)
    consoleHandler.setLevel(logging.WARNING)
    simple_format = logging.Formatter('%(levelname)s - %(message)s')
    consoleHandler.setFormatter(simple_format)
    logger.addHandler(consoleHandler)

    return logger


# just checking for config file
if os.path.exists(os.path.join(os.getcwd(), "config.yaml")):
    try:
        with open("config.yaml") as f:
            data = yaml.load(f, Loader=SafeLoader)
            logFile = data["File"]["log_file"]
    except:
        print("Please Check Log File path in config.yaml, We have used  std.log if not specify")
        logFile = "std.log"
# creating our logger
logger = get_logger(logFile)
