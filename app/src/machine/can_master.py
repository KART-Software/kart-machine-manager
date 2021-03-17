from enum import IntEnum
from typing import Any
import can
import struct
from time import sleep
import datetime


class CanTimeoutException(Exception):
    pass


class RpmStatus(IntEnum):
    LOW = 0
    MIDDLE = 1
    HIGH = 2


class Rpm(int):
    LOW_THRESHOLD = 5000
    HIGH_THRESHOLD = 12000
    MAX = 15000

    @property
    def status(self) -> RpmStatus:
        if self < self.LOW_THRESHOLD:
            return RpmStatus.LOW
        elif self < self.HIGH_THRESHOLD:
            return RpmStatus.MIDDLE
        else:
            return RpmStatus.HIGH


class WaterTempStatus(IntEnum):
    LOW = 0
    MIDDLE = 1
    HIGH = 2


class WaterTemp(int):
    LOW_THRESHOLD = 50
    HIGH_THRESHOLD = 100

    @property
    def status(self) -> WaterTempStatus:
        if self < self.LOW_THRESHOLD:
            return WaterTempStatus.LOW
        elif self < self.HIGH_THRESHOLD:
            return WaterTempStatus.MIDDLE
        else:
            return WaterTempStatus.HIGH


class OilTempStatus(IntEnum):
    LOW = 0
    MIDDLE = 1
    HIGH = 2


class OilTemp(int):
    LOW_THRESHOLD = 50
    HIGH_THRESHOLD = 120

    @property
    def status(self) -> OilTempStatus:
        if self < self.LOW_THRESHOLD:
            return OilTempStatus.LOW
        elif self < self.HIGH_THRESHOLD:
            return OilTempStatus.MIDDLE
        else:
            return OilTempStatus.HIGH


class OilPressStatus(IntEnum):
    LOW = 0
    HIGH = 1


class OilPress(float):
    THRESHOLD = 3.0

    @property
    def status(self) -> OilPressStatus:
        if self < self.THRESHOLD:
            return OilPressStatus.LOW
        else:
            return OilPressStatus.HIGH


class FuelRemainStatus(IntEnum):
    LOW = 0
    HIGH = 1


class FuelRemain(float):
    THRESHOLD = 1.0

    @property
    def status(self) -> FuelRemainStatus:
        if self < self.THRESHOLD:
            return FuelRemainStatus.LOW
        else:
            return FuelRemainStatus.HIGH


class BatteryStatus(IntEnum):
    LOW = 0
    HIGH = 1


class Battery(float):
    THRESHOLD = 11.0

    @property
    def status(self) -> BatteryStatus:
        if self < self.THRESHOLD:
            return BatteryStatus.LOW
        else:
            return BatteryStatus.HIGH


class LapTime(datetime.timedelta):
    pass


class CanInfo:
    rpm: Rpm
    oilTemp: OilTemp
    oilPress: OilPress
    battery: Battery

    def __init__(self) -> None:
        self.rpm = Rpm(0)
        self.oilTemp = OilTemp(0.0)
        self.oilPress = OilPress(0)
        self.battery = Battery(0.0)


class CanMaster:

    canInfo: CanInfo

    def __init__(self) -> None:
        self.canInfo = CanInfo()
        self.bus = can.interface.Bus(channel="can0",
                                     bustype="socketcan_native")
        self.listener = can.BufferedReader()
        self.notifier = can.Notifier(self.bus, [self.listener])

    def __del__(self) -> None:
        self.notifier.stop()
        sleep(0.2)
        self.bus.shutdown()

    # def receiveData(self) -> dict:
    #     msg = self.listener.get_message()
    #     msg.data
    #     if msg is None:
    #         raise CanTimeoutException
    #     else:
    #         id, dlc, bdata = struct.unpack("IB3x8s", msg)
    #         # data = bdata.hex()

    #     # self.canInfo.rpm = 3333  # TODO fix

    def receiveData(self) -> bytearray:
        values = bytearray(b'')

        retryLimit = 60
        for i in range(4):
            while 1:
                msg = self.bus.recv(1.0)
                if msg.arbitration_id == 1520 + i:
                    values = values + msg.data
                    break
        return values

    def updateCanInfo(self):
        data = self.receiveData()
        self.canInfo.rpm = Rpm(data[0] * 256 + data[1])
        self.canInfo.oilTemp = OilTemp(round(data[20] * 2.56 + data[21] * 0.1, 2))
        self.canInfo.oilPress = OilPress(data[22] * 256 + data[23])
        self.canInfo.battery = Battery(round(data[26] * 2.56 + data[27] * 0.01, 3))