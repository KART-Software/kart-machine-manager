# from socket import *
from typing import List
import can
import os

from src.can.mock_can_sender import MockCanSender
from src.models.models import DashMachineInfo
from src.can.can_listeners import DashInfoListener, UdpPayloadListener


class CanMaster:
    bus: can.BusABC
    dashInfoListener: DashInfoListener
    udpPayloadListener: UdpPayloadListener

    def __init__(self) -> None:
        if os.getenv("DEBUG", "False").lower() == "true":
            mockCanSender = MockCanSender()
            mockCanSender.start()
            self.bus = can.Bus(channel="debug", interface="virtual")
        else:
            os.system("sudo ip link set can0 down")
            os.system("sudo ip link set can0 type can bitrate 500000")
            os.system("sudo ip link set can0 up")
            self.bus = can.Bus(channel="can0", interface="socketcan")
        self.dashInfoListener = DashInfoListener()
        self.udpPayloadListener = UdpPayloadListener()
        self.notifier = can.Notifier(
            self.bus, [self.dashInfoListener, self.udpPayloadListener]
        )

    def __del__(self) -> None:
        self.notifier.stop()
        self.bus.shutdown()

    dashMachineInfo = property(lambda self: self.dashInfoListener.dashMachineInfo)
