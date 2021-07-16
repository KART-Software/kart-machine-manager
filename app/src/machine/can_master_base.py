from abc import ABCMeta, abstractmethod
from enum import IntEnum
import datetime


class CanTimeoutException(Exception):
    pass


class RpmStatus(IntEnum):
    LOW = 0
    MIDDLE = 1
    HIGH = 2


class Rpm(int):
    LOW_THRESHOLD = 3200
    HIGH_THRESHOLD = 6400
    MAX = 9600

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
    def threshold(self, rpm: Rpm) -> float:
        return 0.00000241088030949 * rpm * rpm

    def status(self, rpm: Rpm) -> OilPressStatus:
        if self < self.threshold(rpm):
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


class FrontArduinoData(list):
    pass


class CanInfo:
    rpm: Rpm
    waterTemp: WaterTemp
    oilTemp: OilTemp
    oilPress: OilPress
    battery: Battery

    frontArduinoData: FrontArduinoData

    def __init__(self) -> None:
        self.rpm = Rpm(0)
        self.waterTemp = WaterTemp(0)
        self.oilTemp = OilTemp(0)
        self.oilPress = OilPress(0.0)
        self.battery = Battery(0.0)
        self.frontArduinoData = FrontArduinoData(range(2))


class CanMasterBase(metaclass=ABCMeta):

    canInfo: CanInfo

    @abstractmethod
    def updateCanInfo(self):
        pass
