from enum import IntEnum
from typing import Any
import can
from time import sleep
import datetime

from src.machine.can_master_base import Battery, CanInfo, CanMasterBase, OilPress, OilTemp, Rpm


class CanMaster(CanMasterBase):

    canInfo: CanInfo

    ARBITRATION_IDS = [1520, 1521, 1522, 1523]

    DBS_RPM = [0, 1]
    DBS_OIL_TEMP = [20, 21]
    DBS_OIL_PRESS = [22, 23]
    DBS_BATTERY = [26, 27]

    def __init__(self) -> None:
        self.canInfo = CanInfo()
        self.bus = can.interface.Bus(channel="can0",
                                     bustype="socketcan_native")
        self.listener = can.BufferedReader()
        self.notifier = can.Notifier(self.bus, [self.listener])

    def __del__(self) -> None:
        self.notifier.stop()
        sleep(0.2)
        self.bus.shutdown()

    # def receiveData(self) -> dict:
    #     msg = self.listener.get_message()
    #     msg.data
    #     if msg is None:
    #         raise CanTimeoutException
    #     else:
    #         id, dlc, bdata = struct.unpack("IB3x8s", msg)
    #         # data = bdata.hex()

    #     # self.canInfo.rpm = 3333  # TODO fix

    def _receiveData(self) -> bytearray:
        values = bytearray(b'')

        retryLimit = 12
        for ai in CanMaster.ARBITRATION_IDS:
            for _ in range(retryLimit):
                msg = self.bus.recv(0.1)  #TODO 確認
                if msg != None or msg.arbitration_id == ai:
                    values = values + msg.data
                    break
        return values

    def updateCanInfo(self):
        data = self._receiveData()
        self.canInfo.rpm = Rpm(data[CanMaster.DBS_RPM[0]] * 256 +
                               data[CanMaster.DBS_RPM[1]])
        self.canInfo.oilTemp = OilTemp(
            round(
                data[CanMaster.DBS_OIL_TEMP[0]] * 2.56 +
                data[CanMaster.DBS_OIL_TEMP[1]] * 0.1, 2))
        self.canInfo.oilPress = OilPress(data[CanMaster.DBS_OIL_PRESS[0]] *
                                         256 +
                                         data[CanMaster.DBS_OIL_PRESS[1]])
        self.canInfo.battery = Battery(
            round(
                data[CanMaster.DBS_BATTERY[0]] * 2.56 +
                data[CanMaster.DBS_BATTERY[1]] * 0.01, 3))
