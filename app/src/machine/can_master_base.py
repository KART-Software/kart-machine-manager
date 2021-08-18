from abc import ABCMeta, abstractmethod
from enum import IntEnum
import datetime
from typing import Any, Dict, List


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
    requiredOilPress: float

    COEFFICIENT = 0.00000241088030949

    def setRequiredOilPress(self, rpm: Rpm):
        self.requiredOilPress = OilPress.COEFFICIENT * rpm * rpm

    @property
    def status(self) -> OilPressStatus:
        if self < self.requiredOilPress:
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


class Can_Properties:
    FRONT_ARDUINO = {
        "arbitration id": [1776],
        "length": 8,
        "dbs head": [0],
        "converted length": 4
    }

    REAR_ARDUINO = {
        "arbitration id": [1792],
        "length": 8,
        "dbs head": [0],
        "converted length": 4
    }

    MOTEC = {
        "arbitration id": [1520, 1521, 1522, 1523],
        "length": 28,
        "dbs head": [0, 8, 16, 24],
    }


class CanData(List[int]):
    PROPERTY: Dict[str, Any]

    def __init__(self):
        super().__init__(
            [0 for _ in range(type(self).PROPERTY["converted length"])])

    def update(self, rawData: bytearray):
        for i in range(type(self).PROPERTY["converted length"]):
            self[i] = rawData[2 * i] * 256 + rawData[2 * i + 1]


class FrontArduinoData(CanData):
    PROPERTY = Can_Properties.FRONT_ARDUINO


class RearArduinoData(CanData):
    PROPERTY = Can_Properties.REAR_ARDUINO


class MotecInfo:
    rawData: bytearray
    rpm: Rpm
    waterTemp: WaterTemp
    oilTemp: OilTemp
    oilPress: OilPress
    battery: Battery

    PROPERTY = Can_Properties.MOTEC

    DBS_RPM = [0, 1]
    DBS_WATER_TEMP = [8, 9]
    DBS_OIL_TEMP = [20, 21]
    DBS_OIL_PRESS = [22, 23]
    DBS_BATTERY = [26, 27]

    def __init__(self):
        self.rpm = Rpm(0)
        self.waterTemp = WaterTemp(0)
        self.oilTemp = OilTemp(0)
        self.oilPress = OilPress(0.0)
        self.battery = Battery(0.0)

    def update(self, rawData: bytearray):
        if len(rawData) != MotecInfo.PROPERTY["length"]:
            pass
            # TODO エラー処理
        else:
            self.rawData = rawData
            self.rpm = Rpm(rawData[MotecInfo.DBS_RPM[0]] * 256 +
                           rawData[MotecInfo.DBS_RPM[1]])
            self.waterTemp = WaterTemp(
                round(
                    rawData[MotecInfo.DBS_WATER_TEMP[0]] * 25.6 +
                    rawData[MotecInfo.DBS_WATER_TEMP[1]] * 0.1, 2))
            self.oilTemp = OilTemp(
                round(
                    rawData[MotecInfo.DBS_OIL_TEMP[0]] * 25.6 +
                    rawData[MotecInfo.DBS_OIL_TEMP[1]] * 0.1, 2))
            self.oilPress = OilPress(rawData[MotecInfo.DBS_OIL_PRESS[0]] *
                                     256 + rawData[MotecInfo.DBS_OIL_PRESS[1]])
            self.battery = Battery(
                round(
                    rawData[MotecInfo.DBS_BATTERY[0]] * 2.56 +
                    rawData[MotecInfo.DBS_BATTERY[1]] * 0.01, 3))

    def updateByConvetedValues(
        self,
        rpm: Rpm,
        waterTemp: WaterTemp,
        oilTemp: OilTemp,
        oilPress: OilPress,
        battery: Battery,
    ):
        self.rpm = rpm
        self.waterTemp = waterTemp
        self.oilTemp = oilTemp
        self.oilPress = oilPress
        self.battery = battery


class CanInfo:
    motecInfo: MotecInfo
    frontArduinoData: FrontArduinoData
    rearArduinoData: RearArduinoData

    def __init__(self) -> None:
        self.motecInfo = MotecInfo()
        self.frontArduinoData = FrontArduinoData()
        self.rearArduinoData = RearArduinoData()


class CanMasterBase(metaclass=ABCMeta):

    canInfo: CanInfo

    @abstractmethod
    def updateCanInfo(self):
        pass
