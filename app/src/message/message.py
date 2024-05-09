import logging
import threading
import time

import requests  # type: ignore

from src.models.models import Message
from src.util import config


class Messenger:
    GET_INTERVAL_TIME = 2

    thread: threading.Thread
    message: Message

    def __init__(self) -> None:
        self.message = Message()

    def tryGetMessage(self):
        try:
            res = requests.get(config.cloudMessageApiEndpoint)
            self.message.text = str(res.json()["message"]["text"])
        except BaseException:
            logging.warning("Get message failed!")

    def getEvery(self):
        while True:
            self.tryGetMessage()
            time.sleep(self.GET_INTERVAL_TIME)
            logging.info(f"message: {self.message.text}")

    def start(self):
        self.thread = threading.Thread(target=self.getEvery)
        self.thread.setDaemon(True)
        self.thread.start()
