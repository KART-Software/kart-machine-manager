import can
from time import sleep
import os

from can.interface import Bus

from src.machine.can_master_base import (Battery, CanInfo, CanMasterBase,
                                         RearArduinoData, WaterTemp, OilPress,
                                         OilTemp, Rpm, FrontArduinoData)


class CanMaster(CanMasterBase):

    canInfo: CanInfo
    bus: Bus
    # receiveValuesFromMotec: bytearray
    # receiveValuesFromFrontArduino: bytearray

    # ARBITRATION_IDS_MOTEC = [1520, 1521, 1522, 1523]
    # DATA_LENGTH_FROM_MOTEC = 28
    # DBS_HEAD_MOTEC = [0, 8, 16, 24]

    # ARBITRATION_IDS_FRONT_ARDUINO = [1776]
    # DATA_LENGTH_FROM_FRONT_ARDUINO = 4
    # DBS_HEAD_FRONT_ARDUINO = [0]

    # ARBITRATION_IDS = ARBITRATION_IDS_MOTEC + ARBITRATION_IDS_FRONT_ARDUINO
    # DATA_LENGTH = DATA_LENGTH_FROM_MOTEC + DATA_LENGTH_FROM_FRONT_ARDUINO

    MOTEC_INFO = {
        "arbitration id": [1520, 1521, 1522, 1523],
        "length": 28,
        "dbs head": [0, 8, 16, 24],
    }

    # motec
    DBS_RPM = [0, 1]
    DBS_WATER_TEMP = [8, 9]
    DBS_OIL_TEMP = [20, 21]
    DBS_OIL_PRESS = [22, 23]
    DBS_BATTERY = [26, 27]

    def __init__(self) -> None:
        self.canInfo = CanInfo()
        os.system('sudo ip link set can0 down')
        os.system('sudo ip link set can0 type can bitrate 500000')
        os.system('sudo ip link set can0 up')
        self.bus = can.interface.Bus(channel="can0",
                                     bustype="socketcan_native")
        # self.listener = can.BufferedReader()
        # self.notifier = can.Notifier(self.bus, [self.listener])

        # self.receiveValuesFromMotec = bytearray(
        #     range(CanMaster.DATA_LENGTH_FROM_MOTEC))
        # self.receiveValuesFromFrontArduino = bytearray(
        #     range(CanMaster.DATA_LENGTH_FROM_FRONT_ARDUINO))

    def __del__(self) -> None:
        # self.notifier.stop()
        sleep(0.2)
        self.bus.shutdown()

    def _receiveData(self, info: dict) -> bytearray:
        receiveValues = bytearray(range(info["length"]))
        retryLimit = 12
        for (ai, dh) in zip(info["arbitration id"], info["dbs head"]):
            self.bus.set_filters([{
                "can_id": ai,
                "can_mask": 2047,
                "extended": False
            }])
            for _ in range(retryLimit):
                msg = self.bus.recv(0.2)
                if msg is not None and msg.arbitration_id == ai:
                    for i, value in enumerate(msg.data):
                        receiveValues[dh + i] = value
                    break
        return receiveValues

    def updateCanInfo(self):
        dataFromMotec = self._receiveData(CanMaster.MOTEC_INFO)
        # dataFromFrontArduino = self._receiveData(FrontArduinoData.INFO)
        # dataFromRearArduino = self._receiveData(RearArduinoData.INFO)

        self.canInfo.rpm = Rpm(dataFromMotec[CanMaster.DBS_RPM[0]] * 256 +
                               dataFromMotec[CanMaster.DBS_RPM[1]])
        self.canInfo.waterTemp = WaterTemp(
            round(
                dataFromMotec[CanMaster.DBS_WATER_TEMP[0]] * 25.6 +
                dataFromMotec[CanMaster.DBS_WATER_TEMP[1]] * 0.1, 2))
        self.canInfo.oilTemp = OilTemp(
            round(
                dataFromMotec[CanMaster.DBS_OIL_TEMP[0]] * 25.6 +
                dataFromMotec[CanMaster.DBS_OIL_TEMP[1]] * 0.1, 2))
        self.canInfo.oilPress = OilPress(
            dataFromMotec[CanMaster.DBS_OIL_PRESS[0]] * 256 +
            dataFromMotec[CanMaster.DBS_OIL_PRESS[1]])
        self.canInfo.battery = Battery(
            round(
                dataFromMotec[CanMaster.DBS_BATTERY[0]] * 2.56 +
                dataFromMotec[CanMaster.DBS_BATTERY[1]] * 0.01, 3))

        # self.canInfo.frontArduinoData = FrontArduinoData([
        #     dataFromFrontArduino[2 * i] * 256 + dataFromFrontArduino[2 * i + 1]
        #     for i in range(FrontArduinoData.INFO["converted length"])
        # ])

        # self.canInfo.rearArduinoData = RearArduinoData([
        #     dataFromRearArduino[2 * i] * 256 + dataFromRearArduino[2 * i + 1]
        #     for i in range(RearArduinoData.INFO["converted length"])
        # ])