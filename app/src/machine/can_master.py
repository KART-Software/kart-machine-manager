from enum import IntEnum
from typing import Any
import can
import struct
from time import sleep


class CanTimeoutException(Exception):
    pass


class RpmStatus(IntEnum):
    LOW = 0
    HIGH = 2


class Rpm(int):
    THRESHOLD = 8000

    @property
    def status(self) -> RpmStatus:
        if self < self.THRESHOLD:
            return RpmStatus.LOW
        else:
            return RpmStatus.HIGH


class CanInfo:
    rpm: Rpm

    def __init__(self) -> None:
        self.rpm = 0


class CanMaster:

    canInfo: CanInfo

    def __init__(self) -> None:
        self.canInfo = CanInfo()
        self.bus = can.interface.Bus(channel="can0", bustype="socketcan_native")
        self.listener = can.BufferedReader()
        self.notifier = can.Notifier(self.bus, [self.listener])

    def __del__(self) -> None:
        self.notifier.stop()
        sleep(0.2)
        self.bus.shutdown()

    def receiveData(self) -> Any:
        msg = self.listener.get_message()
        msg.data
        if msg is None:
            raise CanTimeoutException
        else:
            id, dlc, bdata = struct.unpack("IB3x8s", msg)
            # data = bdata.hex()

        self.canInfo.rpm = 3333  # TODO fix
