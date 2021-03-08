from src.application import Application
import logging


if __name__ == "__main__":
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'common': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
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
            'handlers': ['info', 'error']
        },
        'disable_existing_loggers': False
    })
    logging.info("App started!")
    app = Application()
    app.initialize()
