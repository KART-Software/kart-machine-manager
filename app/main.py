import datetime
import logging
import logging.config
import os

from src.application.application import Application
from src.util import config

if __name__ == "__main__":
    log_file_path = "log/app_{}.log".format(
        datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    file_path = os.path.dirname(log_file_path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {
                "common": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "logFileHandler": {
                    "class": "logging.FileHandler",
                    "level": "DEBUG",
                    "formatter": "common",
                    "filename": log_file_path,
                    "mode": "w",
                    "encoding": "utf-8",
                },
                "info": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "common",
                    "stream": "ext://sys.stdout",
                },
                "error": {
                    "class": "logging.StreamHandler",
                    "level": "ERROR",
                    "formatter": "common",
                    "stream": "ext://sys.stderr",
                },
            },
            "root": {"level": "DEBUG", "handlers": ["logFileHandler", "info", "error"]},
            "disable_existing_loggers": False,
        }
    )
    if config.debug:
        logging.info("App started in DEBUG Mode!")
    else:
        logging.info("App started in PROD Mode!")
    app = Application()
    app.initialize()
