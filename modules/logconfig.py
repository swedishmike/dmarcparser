import logging
import sys
from logging.config import dictConfig


def set_up_logging():
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] (%(module)s): %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'standard',
                'filename': 'dmarcparser.log',
                'maxBytes': 10485760,
                'backupCount': 5,
                'encoding': "utf8",
            },
        },
        'loggers': {
            '': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True
            }
        }
    })
    return logging


if __name__ == '__main__':
    print("Exiting - this should only be called from the main program.")
    sys.exit(1)