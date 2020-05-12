'''
Common utils for the messenger service
'''

# Core python
import logging
import logging.config

def configure_logging(log_level_param: str = None):
    """
    Retrofits a Python logging configuration on the current process
    """
    if log_level_param is None:
        log_level_name = "INFO"
    else:
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

            },
            'file_handler': {
                'class': 'logging.FileHandler',
                'filename': 'pigeon.log',
                'formatter': 'standard'
            }
        },
        'loggers': {
            'root': {
                'handlers': ['stderr_handler', 'file_handler'],
                'level': f'{log_level_name}',
                'propagate': True
            }
        }
    })
