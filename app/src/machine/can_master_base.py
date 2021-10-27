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


class GearType(IntEnum):
    NEUTRAL = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
    TOP = 4
    FIFTH = 5
    SIXTH = 6


def getGearType(voltage: float) -> GearType:
    EACH_VOLTAGES = [3.86, 4.20, 3.52, 2.84, 2.16, 1.50, 0.81]

    deviations = [abs(voltage - eachVoltage) for eachVoltage in EACH_VOLTAGES]
    gearNum = deviations.index(min(deviations))
    return GearType(gearNum)


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
        "arbitration id": [1520, 1521, 1522, 1523, 1524],
        "length": 34,
        "dbs head": [0, 8, 16, 24, 32],
        "converted length": 17
    }


class CanData(List[int]):
    rawData: bytearray
    PROPERTY: Dict[str, Any]

    def __init__(self):
        super().__init__(
            [0 for _ in range(type(self).PROPERTY["converted length"])])

    def update(self, rawData: bytearray):
        self.rawData = rawData
        self.umbinarize(rawData)

    def umbinarize(self, rawData: bytearray):
        for i in range(type(self).PROPERTY["converted length"]):
            self[i] = rawData[2 * i] * 256 + rawData[2 * i + 1]


class FrontArduinoData(CanData):
    PROPERTY = Can_Properties.FRONT_ARDUINO


class RearArduinoData(CanData):
    PROPERTY = Can_Properties.REAR_ARDUINO


class MotecInfo(CanData):

    PROPERTY = Can_Properties.MOTEC

    INDEX_RPM = 0
    INDEX_WATER_TEMP = 4
    INDEX_GEAR_SENSOR_VOLTAGE = 8
    INDEX_OIL_TEMP = 10
    INDEX_OIL_PRESS = 11
    INDEX_BATTERY = 13

    def __init__(self):
        super().__init__()
        self.rawData = bytearray(
            [0 for _ in range(MotecInfo.PROPERTY["length"])])

    @property
    def rpm(self) -> Rpm:
        return Rpm(self[MotecInfo.INDEX_RPM])

    @property
    def waterTemp(self) -> WaterTemp:
        return WaterTemp(round(self[MotecInfo.INDEX_WATER_TEMP] / 10.0, 2))

    @property
    def oilTemp(self) -> OilTemp:
        return OilTemp(round(self[MotecInfo.INDEX_OIL_TEMP] / 10.0, 2))

    @property
    def oilPress(self) -> OilPress:
        return OilPress(self[MotecInfo.INDEX_OIL_PRESS])

    @property
    def battery(self) -> Battery:
        return Battery(round(self[MotecInfo.INDEX_BATTERY] / 100.0, 3))

    @property
    def gearType(self) -> GearType:
        gearSensorVoltage = self[MotecInfo.INDEX_GEAR_SENSOR_VOLTAGE] / 100.0
        return getGearType(gearSensorVoltage)


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
