from enum import IntEnum


class MachineException(BaseException):
    pass


class CanTimeoutException(MachineException):
    pass


class GearType(IntEnum):
    NEUTRAL = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3


class RpmStatus(IntEnum):
    LOW = 0
    MIDDLE = 1
    HIGH = 2


class Rpm(int):
    HIGH_THRESHOLD = 8000
    LOW_THRESHOLD = 3000

    @property
    def status(self) -> RpmStatus:
        if self < self.LOW_THRESHOLD:
            return RpmStatus.LOW
        elif self < self.HIGH_THRESHOLD:
            return RpmStatus.MIDDLE
        else:
            return RpmStatus.HIGH
