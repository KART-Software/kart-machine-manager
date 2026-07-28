import logging
import threading
from typing import Iterable, Optional

from src.canbus.bus import CanBus
from src.canbus.message import Message


class Listener:
    """Base class mirroring python-can's Listener."""

    def on_message_received(self, msg: Message) -> None:
        raise NotImplementedError


class Notifier:
    """Reader thread dispatching received frames to listeners.

    Mirrors python-can's Notifier(bus, listeners) / .stop().
    A listener exception is logged and does not kill the reader thread.
    """

    _POLL_TIMEOUT = 0.5  # allows stop() to take effect promptly

    def __init__(self, bus: CanBus, listeners: Iterable[Listener]) -> None:
        self._bus = bus
        self._listeners = list(listeners)
        self._stopped = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        while not self._stopped.is_set():
            msg: Optional[Message] = self._bus.recv(timeout=self._POLL_TIMEOUT)
            if msg is None:
                continue
            for listener in self._listeners:
                try:
                    listener.on_message_received(msg)
                except Exception:
                    logging.exception("CAN listener raised; continuing")

    def stop(self) -> None:
        self._stopped.set()
        self._thread.join(timeout=2 * self._POLL_TIMEOUT)
