from src.machine.can_master_base import Battery, CanInfo, CanMasterBase, OilPress, OilTemp, Rpm


class CanMasterMock(CanMasterBase):

    canInfo: CanInfo

    def __init__(self) -> None:
        self.canInfo = CanInfo()

    def updateCanInfo(self):
        self.canInfo.rpm = Rpm(15)
        self.canInfo.oilTemp = OilTemp(80.0)
        self.canInfo.oilPress = OilPress(13)
        self.canInfo.battery = Battery(10.6)