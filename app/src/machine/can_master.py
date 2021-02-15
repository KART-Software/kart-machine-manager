from app.src.machine.machine import CanTimeoutException
from typing import Any
import can
import struct
from time import sleep


class CanMaster:
    def __init__(self) -> None:
        self.bus = can.interface.Bus(
            channel="can0",
            bustype="socketcan_native"
        )
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




