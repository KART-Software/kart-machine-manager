from socket import *
from typing import Any
import can
from time import sleep
import os

from can.interface import Bus
from can.message import Message

from src.machine.can_master_base import CanInfo
from src.models.models import DashMachineInfo, UDPMachineInfo

class CanMaster:

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

class DashInfoListener(can.Listener):
    dashMachineInfo: DashMachineInfo

    def __init__(self) -> None:
        super().__init__()
        self.dashMachineInfo = DashMachineInfo()

    def on_message_received(self, msg: Message) -> None:
        if msg.arbitration_id == 0x5F0:
            self.dashMachineInfo.rpm =  msg.data[0:1]
            self.dashMachineInfo.waterTemp = msg.data[2:3]
            self.dashMachineInfo.oilTemp = msg.data[4:5]
            self.dashMachineInfo.oilPress = msg.data[6:7]
        elif msg.arbitration_id == 0x5F1:
            self.dashMachineInfo.gearVoltage = msg.data[0:1]
        # ここの数字は後で変更

class UdpLister(can.Listener):
    udpInfo: UDPMachineInfo

    def __init__(self) -> None:
        super().__init__()
        self.udpInfo = UDPMachineInfo()
