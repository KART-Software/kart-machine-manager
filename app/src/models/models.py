from datetime import timedelta
from enum import IntEnum


class RpmStatus(IntEnum):
    LOW = 0
    MIDDLE = 1
    HIGH = 2
    SHIFT = 3


class Rpm(int):
    LOW_THRESHOLD = 4000
    HIGH_THRESHOLD = 7000
    SHIFT_THRESHOLD = 9000
    MAX = 10000

    @property
    def status(self) -> RpmStatus:
        if self < self.LOW_THRESHOLD:
            return RpmStatus.LOW
        elif self < self.HIGH_THRESHOLD:
            return RpmStatus.MIDDLE
        elif self < self.SHIFT_THRESHOLD:
            return RpmStatus.HIGH
        else:
            return RpmStatus.SHIFT


class WaterTempStatus(IntEnum):
    LOW = 0
    MIDDLE = 1
    HIGH = 2


class WaterTemp(int):
    LOW_THRESHOLD = 50
    HIGH_THRESHOLD = 98

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


class OilPress:
    oilPress: float
    rpm: int

    COEFFICIENT = 0.00000241088030949

    def __init__(self):
        self.oilPress = 0.0
        self.rpm = 0

    @property
    def status(self) -> OilPressStatus:
        requiredOilPress = self.COEFFICIENT * self.rpm**2
        if self.oilPress < requiredOilPress:
            return OilPressStatus.LOW
        else:
            return OilPressStatus.HIGH


class FuelPressStatus(IntEnum):
    LOW = 0
    HIGH = 1


class FuelPress(float):
    THRESHOLD = 50.0

    @property
    def status(self) -> FuelPressStatus:
        if self < self.THRESHOLD:
            return FuelPressStatus.LOW
        else:
            return FuelPressStatus.HIGH


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


class BatteryStatus(IntEnum):
    LOW = 0
    HIGH = 1


class BatteryVoltage(int):
    THRESHOLD = 11

    @property
    def status(self) -> BatteryStatus:
        if self < self.THRESHOLD:
            return BatteryStatus.LOW
        else:
            return BatteryStatus.HIGH


class BrakePress:
    front: float
    rear: float

    def __init__(self):
        self.front = 0.0
        self.rear = 0.0

    @property
    def bias(self) -> float:
        if self.front <= 0.0 and self.rear <= 0.0:
            return 0.0
        else:
            front = max(0.0, self.front)
            rear = max(0.0, self.rear)
            return 100.0 * front / (front + rear)


class DashMachineInfo:
    rpm: Rpm
    throttlePosition: float
    waterTemp: WaterTemp
    oilTemp: OilTemp
    oilPress: OilPress
    gearVoltage: GearVoltage
    batteryVoltage: BatteryVoltage
    fanEnabled: bool
    fuelPress: FuelPress
    brakePress: BrakePress

    def __init__(self) -> None:
        self.rpm = Rpm(0)
        self.throttlePosition = 0.0
        self.waterTemp = WaterTemp(0)
        self.oilTemp = OilTemp(0)
        self.oilPress = OilPress()
        self.gearVoltage = GearVoltage(GearVoltage.EACH_VOLTAGES[GearType.NEUTRAL])
        self.batteryVoltage = BatteryVoltage(0)
        self.fanEnabled = False
        self.fuelPress = FuelPress(0.0)
        self.brakePress = BrakePress()

    def setRpm(self, rpm: int):
        self.rpm = Rpm(rpm)
        self.oilPress.rpm = rpm


class Message:
    text: str
    lap: int

    def __init__(self) -> None:
        self.text = ""
        self.lap = 0


# class LapTime(timedelta):
#     pass
