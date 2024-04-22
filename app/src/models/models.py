from datetime import timedelta
from enum import IntEnum


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
    requiredOilPress: float = 0.0

    COEFFICIENT = 0.00000241088030949

    def setRequiredOilPress(self, rpm: Rpm):
        self.requiredOilPress = OilPress.COEFFICIENT * rpm * rpm

    @property
    def status(self) -> OilPressStatus:
        if self < self.requiredOilPress:
            return OilPressStatus.LOW
        else:
            return OilPressStatus.HIGH


class LapTime(timedelta):
    pass


class GearType(IntEnum):
    NEUTRAL = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
    TOP = 4
    FIFTH = 5
    SIXTH = 6


class GearVoltage(float):
    EACH_VOLTAGES = [3.86, 4.20, 3.52, 2.84, 2.16, 1.50, 0.81]

    @property
    def gearType(self) -> GearType:
        deviations = [
            abs(self - eachVoltage) for eachVoltage in GearVoltage.EACH_VOLTAGES
        ]
        gearNum = deviations.index(min(deviations))
        return GearType(gearNum)

    @property
    def gearTypeString(self) -> str:
        g = self.gearType
        if g == GearType.NEUTRAL:
            return "N"
        else:
            return str(g)


def getGearType(voltage: float) -> GearType:
    EACH_VOLTAGES = [3.86, 4.20, 3.52, 2.84, 2.16, 1.50, 0.81]

    deviations = [abs(voltage - eachVoltage) for eachVoltage in EACH_VOLTAGES]
    gearNum = deviations.index(min(deviations))
    return GearType(gearNum)


class DashMachineInfo:
    rpm: Rpm
    throttlePosition: float
    waterTemp: WaterTemp
    oilTemp: OilTemp
    oilPress: OilPress
    gearVoltage: GearVoltage

    def __init__(self) -> None:
        self.rpm = Rpm(0)
        self.throttlePosition = 0.0
        self.waterTemp = WaterTemp(0)
        self.oilTemp = OilTemp(0)
        self.oilPress = OilPress(0)
        self.gearVoltage = GearVoltage(GearVoltage.EACH_VOLTAGES[GearType.NEUTRAL])


class Message:
    text: str
    lap: int

    def __init__(self) -> None:
        self.text = ""
        self.lap = 0
