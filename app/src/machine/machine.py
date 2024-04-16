import os
from enum import IntEnum
from threading import Thread
import datetime
import time
import csv

from src.machine.can_master_base import (
    GearType,
    MotecInfo,
    Rpm,
    WaterTemp,
    OilTemp,
    OilPress,
    FuelRemain,
    Battery,
    LapTime,
)
from src.machine.can_master_mock import CanMasterMock
from src.machine.can_master import CanMaster


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
    gearType: GearType

    def __init__(self) -> None:
        self.rpm = Rpm(0)
        self.waterTemp = WaterTemp(0)
        self.lapTime = LapTime(microseconds=0)
        self.oilTemp = OilTemp(0.0)
        self.oilPress = OilPress(0.0)
        self.fuelRemain = FuelRemain(0.0)
        self.battery = Battery(0.0)
        self.gearType = GearType(0)

class Machine:

    canMaster: CanMaster or CanMasterMock
    machineInfo: MachineInfo
   
    def __init__(self) -> None:
        self.machineInfo = MachineInfo()
       
    def initialise(self) -> None:
        if os.getenv('DEBUG', 'False').lower() == 'true':
            self.canMaster = CanMasterMock()
        else:
            self.canMaster = CanMaster()

        self.updateMachineInfo()

    def updateMachineInfo(self):
        self.canMaster.updateCanInfo()
        self.machineInfo.rpm = self.canMaster.canInfo.motecInfo.rpm
        self.machineInfo.waterTemp = self.canMaster.canInfo.motecInfo.waterTemp
        self.machineInfo.oilTemp = self.canMaster.canInfo.motecInfo.oilTemp
        self.machineInfo.oilPress = self.canMaster.canInfo.motecInfo.oilPress
        self.machineInfo.oilPress.setRequiredOilPress(self.machineInfo.rpm)
        self.machineInfo.battery = self.canMaster.canInfo.motecInfo.battery
        self.machineInfo.gearType = self.canMaster.canInfo.motecInfo.gearType
   