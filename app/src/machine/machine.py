from enum import IntEnum

from threading import Thread
from time import sleep

from src.machine.can_master import CanInfo, CanMaster, Rpm

import json


class MachineException(BaseException):
    pass

class MachineInfo:
    rpm: Rpm

    def __init__(self) -> None:
        self.rpm = Rpm(0)

class GearType(IntEnum):
    NEUTRAL = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3


class Machine():

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
        
