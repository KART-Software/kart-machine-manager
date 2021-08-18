import can
from time import sleep
import os

from can.interface import Bus

from src.machine.can_master_base import (
    CanInfo,
    CanMasterBase,
    MotecInfo,
    RearArduinoData,
    FrontArduinoData,
)


class CanMaster(CanMasterBase):

    canInfo: CanInfo
    bus: Bus

    def __init__(self) -> None:
        self.canInfo = CanInfo()
        os.system('sudo ip link set can0 down')
        os.system('sudo ip link set can0 type can bitrate 500000')
        os.system('sudo ip link set can0 up')
        self.bus = can.interface.Bus(channel="can0",
                                     bustype="socketcan_native")
        # self.listener = can.BufferedReader()
        # self.notifier = can.Notifier(self.bus, [self.listener])

    def __del__(self) -> None:
        # self.notifier.stop()
        sleep(0.2)
        self.bus.shutdown()

    def _receiveData(self, info: dict) -> bytearray:
        receiveValues = bytearray(0 for _ in range(info["length"]))
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
        dataFromMotec = self._receiveData(MotecInfo.PROPERTY)
        # dataFromFrontArduino = self._receiveData(FrontArduinoData.PROPERTY)
        # dataFromRearArduino = self._receiveData(RearArduinoData.PROPERTY)

        self.canInfo.motecInfo.update(dataFromMotec)

        # self.canInfo.frontArduinoData.update(dataFromFrontArduino)
        # self.canInfo.rearArduinoData.update(dataFromRearArduino)

        # # self.canInfo.frontArduinoData = FrontArduinoData([
        # #     dataFromFrontArduino[2 * i] * 256 + dataFromFrontArduino[2 * i + 1]
        # #     for i in range(FrontArduinoData.INFO["converted length"])
        # # ])

        # # self.canInfo.rearArduinoData = RearArduinoData([
        # #     dataFromRearArduino[2 * i] * 256 + dataFromRearArduino[2 * i + 1]
        # #     for i in range(RearArduinoData.INFO["converted length"])
        # # ])