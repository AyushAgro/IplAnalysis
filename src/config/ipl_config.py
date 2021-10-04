import yaml
from yaml.loader import SafeLoader
import os
from utils import ipl_exception
import logging.config


def read_yaml():  # To read Config YAML

    # reading file with open
    with open("src/config/config.yaml") as f:
        data = yaml.load(f, Loader=SafeLoader)

    data_dir = os.path.join(os.getcwd(), data["File"]["data_dir"])
    output_dir = os.path.join(os.getcwd(), data["File"]["output_dir"])
    log_dir = os.path.join(os.getcwd(), data["File"]["log_dir"])
    allowed_filetype = data["FileType"]

    # Checking if data directory is present or not
    if not os.path.isdir(data_dir):
        raise ipl_exception.DirectoryNotFound(data_dir)

    # output_dir
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # log_dir
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    logging.config.dictConfig(data['loggers'])
    logger = logging.getLogger('root')
    return data_dir,output_dir,allowed_filetype,logger
