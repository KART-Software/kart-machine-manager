# from socket import *
import logging
import os
import subprocess

from src.can.can_listeners import DashInfoListener, UdpPayloadListener
from src.can.mock_can_sender import MockCanSender
from src.models.models import DashMachineInfo

import can


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
            r = subprocess.run("sudo ip link set can0 down", shell=True)
            if r.returncode == 0:
                logging.info("CAN interface can0 down succeeded!")
            else:
                logging.error("CAN interface can0 down failed!")
            r = subprocess.run(
                "sudo ip link set can0 type can bitrate 500000", shell=True
            )
            if r.returncode == 0:
                logging.info("CAN interface can0 setting succeeded!")
            else:
                logging.error("CAN interface can0 setting failed!")
            r = subprocess.run("sudo ip link set can0 up", shell=True)
            if r.returncode == 0:
                logging.info("CAN interface can0 up succeeded!")
            else:
                logging.error("CAN interface can0 up failed!")
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
