import can
from time import sleep
import os

from src.machine.can_master_base import (Battery, CanInfo, CanMasterBase,
                                         WaterTemp, OilPress, OilTemp, Rpm)


class CanMaster(CanMasterBase):

    canInfo: CanInfo

    ARBITRATION_IDS = [1520, 1521, 1522, 1523]
    DBS_FROM = [0, 8, 16, 24]

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
        self.receiveValues = bytearray(range(28))

    def __del__(self) -> None:
        # self.notifier.stop()
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
        retryLimit = 12
        for (ai, df) in zip(CanMaster.ARBITRATION_IDS, CanMaster.DBS_FROM):
            self.bus.set_filters([{
                "can_id": ai,
                "can_mask": 2047,
                "extended": False
            }])
            for _ in range(retryLimit):
                msg = self.bus.recv(0.2)
                # print(msg)
                if msg is not None and msg.arbitration_id == ai:
                    for i, value in enumerate(msg.data):
                        self.receiveValues[df + i] = value
                    break
        return self.receiveValues

    def updateCanInfo(self):
        data = self._receiveData()

        self.canInfo.rpm = Rpm(data[CanMaster.DBS_RPM[0]] * 256 +
                               data[CanMaster.DBS_RPM[1]])
        self.canInfo.waterTemp = WaterTemp(
            round(
                data[CanMaster.DBS_WATER_TEMP[0]] * 25.6 +
                data[CanMaster.DBS_WATER_TEMP[1]] * 0.1, 2))
        self.canInfo.oilTemp = OilTemp(
            round(
                data[CanMaster.DBS_OIL_TEMP[0]] * 25.6 +
                data[CanMaster.DBS_OIL_TEMP[1]] * 0.1, 2))
        self.canInfo.oilPress = OilPress(data[CanMaster.DBS_OIL_PRESS[0]] *
                                         256 +
                                         data[CanMaster.DBS_OIL_PRESS[1]])
        self.canInfo.battery = Battery(
            round(
                data[CanMaster.DBS_BATTERY[0]] * 2.56 +
                data[CanMaster.DBS_BATTERY[1]] * 0.01, 3))
