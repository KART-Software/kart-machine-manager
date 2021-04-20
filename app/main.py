import os

from src.application import Application
import logging
import logging.config
import datetime

if __name__ == "__main__":
    log_file_path = 'log/app_{}.log'.format(
        datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    file_path = os.path.dirname(log_file_path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'common': {
                'format':
                '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'logFileHandler': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'common',
                'filename': log_file_path,
                'mode': 'w',
                'encoding': 'utf-8'
            },
            'info': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'common',
                'stream': 'ext://sys.stdout'
            },
            'error': {
                'class': 'logging.StreamHandler',
                'level': 'ERROR',
                'formatter': 'common',
                'stream': 'ext://sys.stderr'
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['logFileHandler', 'info', 'error']
        },
        'disable_existing_loggers': False
    })
    logging.info("App started!")
    app = Application()
    app.initialize()
