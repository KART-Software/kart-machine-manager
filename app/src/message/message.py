import logging
import threading
import time

import requests  # type: ignore

from src.models.models import Message
from src.util import config


class Messenger:
    GET_INTERVAL_TIME = 5

    thread: threading.Thread
    message: Message

    def __init__(self) -> None:
        self.message = Message()
        self._lock = threading.Lock()

    def tryGetMessage(self):
        text: str | None = None
        laptime: float | None = None
        try:
            res = requests.get(config.cloudMessageApiEndpoint, timeout=(3, 5))
            text = str(res.json()["message"]["text"])
        except BaseException:
            logging.warning("Get message failed!")
        try:
            res = requests.get(config.cloudLaptimeApiEndpoint, timeout=(3, 5))
            laptime = float(res.json()["laptime"])
        except BaseException:
            logging.warning("Get laptime failed!")
        with self._lock:
            if text is not None:
                self.message.text = text
            if laptime is not None:
                self.message.laptime = laptime

    def getMessageSnapshot(self) -> Message:
        with self._lock:
            snapshot = Message()
            snapshot.text = self.message.text
            snapshot.laptime = self.message.laptime
            return snapshot

    def getEvery(self):
        while True:
            self.tryGetMessage()
            time.sleep(self.GET_INTERVAL_TIME)
            logging.info(f"message: {self.message.text}")

    def start(self):
        self.thread = threading.Thread(target=self.getEvery)
        self.thread.setDaemon(True)
        self.thread.start()
