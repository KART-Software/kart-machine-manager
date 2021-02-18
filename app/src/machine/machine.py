from enum import IntEnum

from threading import Thread

from src.machine.can_master import CanInfo, CanMaster

import json


class MachineException(BaseException):
    pass


class GearType(IntEnum):
    NEUTRAL = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3


class Machine:

    canMaster: CanMaster
    canMasterThread: Thread
    isInitialised: bool

    def __init__(self) -> None:
        # self.canMaster = CanMaster()
        pass

    def initialise(self) -> None:
        """self.canMasterThread = Thread(
            target=self.canMaster, name = "canMaster"
        )
        self.canMasterThread.start()
        self.isInitialised = True"""

    def updateMachineInfo(self):
        # self.canMaster.receiveData()

        # return self.canMaster.canInfo
        pass

    def machineInfo(self):
        return {
            vars(self.canMaster.canInfo),
        }
