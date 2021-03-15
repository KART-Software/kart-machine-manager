from enum import IntEnum

from threading import Thread

from src.machine.can_master import (
    CanInfo,
    CanMaster,
    Rpm,
    WaterTemp,
    OilTemp,
    OilPress,
    FuelRemain,
    Battery,
    LapTime,
)

import datetime


class MachineException(BaseException):
    pass


class MachineInfo:
    rpm: Rpm
    waterTemp: WaterTemp
    lapTime: LapTime
    oilTemp: OilTemp
    oilPress: OilPress
    fuelRemain: FuelRemain
    battery: Battery

    def __init__(self) -> None:
        self.rpm = Rpm(0)
        self.waterTemp = WaterTemp(0)
        self.lapTime = LapTime(microseconds=0)
        self.oilTemp = OilTemp(0.0)
        self.oilPress = OilPress(0.0)
        self.fuelRemain = FuelRemain(0.0)
        self.battery = Battery(0.0)


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
        self.canMaster = CanMaster()
        """self.canMasterThread = Thread(
            target=self.canMaster, name = "canMaster"
        )
        self.canMasterThread.start()
        self.isInitialised = True"""
        pass

    # def updateMachineInfo(self):
    #     # self.canMaster.receiveData()
    #     # return self.canMaster.canInfo
    #     if self.machineInfo.rpm >= Rpm.MAX:
    #         self.p = -1
    #     elif self.machineInfo.rpm < 1:
    #         self.p = 1

    #     self.machineInfo.rpm = Rpm(self.machineInfo.rpm + self.p * 100)

    #     self.machineInfo.waterTemp = WaterTemp(self.machineInfo.waterTemp + 1)

    #     self.machineInfo.oilTemp = OilTemp(self.machineInfo.oilTemp + 1)
    #     self.machineInfo.oilPress = OilPress(self.machineInfo.oilPress + 0.1)
    #     self.machineInfo.fuelRemain = FuelRemain(self.machineInfo.fuelRemain +
    #                                              0.1)
    #     self.machineInfo.battery = Battery(self.machineInfo.battery + 0.1)
    #     # TO DO CHECK TYPE OF LAPTIME OBJECT
    #     self.machineInfo.lapTime = self.machineInfo.lapTime + LapTime(
    #         microseconds=20000)

    def updateMachineInfo(self):
        self.canMaster.updateCanInfo()
        self.machineInfo.rpm = self.canMaster.canInfo.rpm
        self.machineInfo.oilTemp = self.canMaster.canInfo.oilTemp
        self.machineInfo.oilPress = self.canMaster.canInfo.oilPress
        self.machineInfo.battery = self.canMaster.canInfo.battery
