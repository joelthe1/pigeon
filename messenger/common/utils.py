'''
Common utils for the Pigeon messenger service
'''

# Core python
import logging.config
import os
import typing
import time
import multiprocessing
from dataclasses import fields

import messenger.exceptions as pigeon_exceptions

from messenger.config import Configuration

# logger
_LOGGER = logging.getLogger(__name__)


def configure_logging(filename: str, log_level_param: str):
    '''
    Retrofits a Python logging configuration on the current process
    '''
    log_level_name = str(log_level_param).upper()

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'stderr_handler': {
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stderr',
                'level': 'ERROR'
            },
            'file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': filename,
                'maxBytes': 3000000,
                'backupCount': 2,
                'formatter': 'standard'
            },
        },
        'root': {
                'handlers': ['file_handler', 'stderr_handler'],
                'level': f'{log_level_name}'
        }
    })


def configure_env_variables() -> Configuration:
    '''
    Parse the current environment variables to get your app's configuration
    '''
    _LOGGER.debug("Begin parsing env variables")
    configuration = Configuration()

    for config_field in fields(configuration):
        # Only attempt to set config fields from env vars
        # if such a metadata key exists
        if 'env_var_name' not in config_field.metadata:
            continue
        
        env_var_value = os.environ.get(config_field.metadata['env_var_name'], None)
        if env_var_value is None:
            raise pigeon_exceptions.ConfigException(
                f"Unable to get a value for environment variable "\
                f"{config_field.metadata['env_var_name']}")
        setattr(configuration, config_field.name, env_var_value)
    
    _LOGGER.debug("Finished parsing env variables")
    return configuration


def setup_adhoc_logger(name, log_file, formatter=None, level=logging.INFO):
    '''
    *** Test method. Not intended for production. ***
    To setup as many loggers as you want
    '''
    if formatter is None:
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def reader(queue):
    '''
    *** Test method. Not intended for production. ***
    Logs size of the queue every second
    '''
    logger = multiprocessing.get_logger()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    
    handler = logging.FileHandler('logs/reader.log')
    handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    while True:
        logger.debug(queue.qsize())
        time.sleep(1)

