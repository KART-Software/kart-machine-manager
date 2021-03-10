from enum import IntEnum

from threading import Thread

from src.machine.can_master import CanMaster, Rpm, WaterTemp, LapTime


class MachineException(BaseException):
    pass


class MachineInfo:
    rpm: Rpm
    waterTemp: WaterTemp
    lapTime: LapTime

    def __init__(self) -> None:
        self.rpm = Rpm(0)
        self.waterTemp = WaterTemp(0)
        self.lapTime = LapTime(0)


class GearType(IntEnum):
    NEUTRAL = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3


class Machine:

    canMaster: CanMaster
    machineInfo: MachineInfo
    _machineInfo: MachineInfo
    canMasterThread: Thread
    isInitialised: bool

    def __init__(self, parent=None) -> None:
        self.dummyRpm = 1
        self.p = 1
        self.machineInfo = MachineInfo()

        # self.canMaster = CanMaster()

    def initialise(self) -> None:
        """self.canMasterThread = Thread(
            target=self.canMaster, name = "canMaster"
        )
        self.canMasterThread.start()
        self.isInitialised = True"""
        pass

    def updateMachineInfo(self):
        # self.canMaster.receiveData()
        # return self.canMaster.canInfo
        if self.machineInfo.rpm >= Rpm.MAX:
            self.p = -1
        elif self.machineInfo.rpm < 1:
            self.p = 1

        self.machineInfo.rpm = Rpm(self.machineInfo.rpm + self.p * 100)

        self.machineInfo.waterTemp = WaterTemp(self.machineInfo.waterTemp + 1)

        self.machineInfo.lapTime = LapTime(self.machineInfo.lapTime + 0.03)
