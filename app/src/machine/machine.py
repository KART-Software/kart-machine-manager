import os
from enum import IntEnum
from threading import Thread
import datetime
import time
import csv

from src.machine.can_master_base import (
    FrontArduinoData,
    GearType,
    MotecInfo,
    RearArduinoData,
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
    FrontArduinoData: FrontArduinoData
    rearArduinoData: RearArduinoData

    def __init__(self) -> None:
        self.rpm = Rpm(0)
        self.waterTemp = WaterTemp(0)
        self.lapTime = LapTime(microseconds=0)
        self.oilTemp = OilTemp(0.0)
        self.oilPress = OilPress(0.0)
        self.fuelRemain = FuelRemain(0.0)
        self.battery = Battery(0.0)
        self.gearType = GearType(0)
        self.frontArduinoData = FrontArduinoData()
        self.rearArduinoData = RearArduinoData()


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
        self.log_Interval = 1.0 / self.log_Frequency
        now = datetime.datetime.now()
        self.logFilePath = 'log/data_{}.csv'.format(
            now.strftime('%Y%m%d_%H%M%S'))

    def initialise(self) -> None:
        if os.getenv('DEBUG', 'False').lower() == 'true':
            self.canMaster = CanMasterMock()
        else:
            self.canMaster = CanMaster()

        self.updateMachineInfo()
        self.loggerInit()
        t = Thread(target=self.logStart)
        t.setDaemon(True)
        t.start()

    def updateMachineInfo(self):
        self.canMaster.updateCanInfo()
        self.machineInfo.rpm = self.canMaster.canInfo.motecInfo.rpm
        self.machineInfo.waterTemp = self.canMaster.canInfo.motecInfo.waterTemp
        self.machineInfo.oilTemp = self.canMaster.canInfo.motecInfo.oilTemp
        self.machineInfo.oilPress = self.canMaster.canInfo.motecInfo.oilPress
        self.machineInfo.oilPress.setRequiredOilPress(self.machineInfo.rpm)
        self.machineInfo.battery = self.canMaster.canInfo.motecInfo.battery
        self.machineInfo.gearType = self.canMaster.canInfo.motecInfo.gearType
        self.machineInfo.frontArduinoData = self.canMaster.canInfo.frontArduinoData
        self.machineInfo.rearArduinoData = self.canMaster.canInfo.rearArduinoData

    def loggerInit(self):
        self.log_rows = []
        with open(self.logFilePath, 'a') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            firstLine = [
                "Date Time", "RPM", "Water Temp", "Oil Temp", "Oil Press",
                "Battery"
            ] + [
                "MoTeC {}".format(i)
                for i in range(MotecInfo.PROPERTY["converted length"])
            ] + [
                "Front Arduino {}".format(i)
                for i in range(FrontArduinoData.PROPERTY["converted length"])
            ] + [
                "Rear Arduino {}".format(i)
                for i in range(RearArduinoData.PROPERTY["converted length"])
            ]
            writer.writerow(firstLine)

        self.base_time = int(time.time()) + 1.0
        time.sleep(-1 * time.time() % 1.0)

    def _logMachineInfo(self):
        self.log_rows.append([
            str(datetime.datetime.now()), self.machineInfo.rpm,
            self.machineInfo.waterTemp, self.machineInfo.oilTemp,
            self.machineInfo.oilPress, self.machineInfo.battery
        ] + self.canMaster.canInfo.motecInfo +
                             self.machineInfo.frontArduinoData +
                             self.machineInfo.rearArduinoData)
        if len(self.log_rows) == 10:
            with open(self.logFilePath, 'a') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
                writer.writerows(self.log_rows)
            self.log_rows = []

    def logStart(self):
        while True:
            self._logMachineInfo()
            time.sleep((self.base_time - time.time()) % self.log_Interval)
