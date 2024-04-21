from src.can.can_master import CanMaster
from src.udp.udp_transmitter import UdpTransmitter


class MachineException(BaseException):
    pass


class Machine:
    machineId: int

    canMaster: CanMaster
    udpTransmitter: UdpTransmitter

    def __init__(self) -> None:
        pass

    def initialise(self) -> None:
        self.canMaster = CanMaster()
        self.udpTransmitter = UdpTransmitter(self.canMaster.udpPayloadListener)
        self.udpTransmitter.start()
