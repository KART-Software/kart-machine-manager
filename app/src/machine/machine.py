import os
from enum import IntEnum
from threading import Thread
import datetime
import time
import signal
import csv

from src.machine.can_master_base import (
    CanMasterBase,
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

    canMaster: CanMaster or CanMasterMock
    machineInfo: MachineInfo
    canMasterThread: Thread
    isInitialised: bool
    logFileName: str

    def __init__(self, parent=None) -> None:
        self.dummyRpm = 1
        self.p = 1
        self.machineInfo = MachineInfo()
        self.log_Frequency = 20
        now = datetime.datetime.now()
        self.logFilePath = 'log/data-{}.csv'.format(
            now.strftime('%Y%m%d_%H%M%S'))

        # self.canMaster = CanMaster()

    def initialise(self) -> None:
        if os.getenv('DEBUG', 'False').lower() == 'true':
            self.canMaster = CanMasterMock()
        else:
            self.canMaster = CanMaster()

        self.updateMachineInfo()
        self.logger_init()
        signal.signal(signal.SIGALRM, self.logMachineInfo)
        now = time.time()
        signal.setitimer(signal.ITIMER_REAL,
                         int(now) + 1 - now, 1.0 / self.log_Frequency)
        """self.canMasterThread = Thread(
            target=self.canMaster, name = "canMaster"
        )
        self.canMasterThread.start()
        self.isInitialised = True"""

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
        self.machineInfo.waterTemp = self.canMaster.canInfo.waterTemp
        self.machineInfo.oilTemp = self.canMaster.canInfo.oilTemp
        self.machineInfo.oilPress = self.canMaster.canInfo.oilPress
        self.machineInfo.battery = self.canMaster.canInfo.battery

    def logger_init(self):
        self.log_rows = []
        with open(self.logFilePath, 'a') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow([
                "Date Time", "RPM", "Water Temp", "Oil Temp", "Oil Press",
                "Battery"
            ])

    def logMachineInfo(self, signum, frame):
        self.log_rows.append([
            str(datetime.datetime.now()), self.machineInfo.rpm,
            self.machineInfo.waterTemp, self.machineInfo.oilTemp,
            self.machineInfo.oilPress, self.machineInfo.battery
        ])
        if len(self.log_rows) == self.log_Frequency:
            with open(self.logFilePath, 'a') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
                writer.writerows(self.log_rows)
            self.log_rows = []
