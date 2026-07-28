# from socket import *
import os

from src import canbus as can
from src.can.can_listeners import DashInfoListener, UdpPayloadListener
from src.can.mock_can_sender import MockCanSender


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
            self.bus = can.Bus(channel="can0", interface="socketcan")
        self.dashInfoListener = DashInfoListener()
        self.udpPayloadListener = UdpPayloadListener()
        self.notifier = can.Notifier(
            self.bus, [self.dashInfoListener, self.udpPayloadListener]
        )

    def __del__(self) -> None:
        self.notifier.stop()
        self.bus.shutdown()

    dashMachineInfo = property(lambda self: self.dashInfoListener.snapshot())
