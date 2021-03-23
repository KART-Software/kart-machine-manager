from src.machine.can_master_base import Battery, CanInfo, CanMasterBase, OilPress, OilTemp, Rpm, WaterTemp


class CanMasterMock(CanMasterBase):

    canInfo: CanInfo

    def __init__(self) -> None:
        self.canInfo = CanInfo()
        self.p_Rpm = 1
        self.p_WaterTemp = 1
        self.p_OilTemp = 1
        self.p_OilTemp = 1
        self.p_OilPress = 1
        self.p_Battery = 1

    def updateCanInfo(self):
        # self.canInfo.rpm = Rpm(15)
        # self.canInfo.oilTemp = OilTemp(80.0)
        # self.canInfo.oilPress = OilPress(13)
        # self.canInfo.battery = Battery(10.6)

        if self.canInfo.rpm >= Rpm.MAX:
            self.p_Rpm = -1
        elif self.canInfo.rpm < 1:
            self.p_Rpm = 1
        self.canInfo.rpm = Rpm(self.canInfo.rpm + self.p_Rpm * 87)

        if self.canInfo.waterTemp >= 180:
            self.p_WaterTemp = -1
        elif self.canInfo.waterTemp < 1:
            self.p_WaterTemp = 1
        self.canInfo.waterTemp = WaterTemp(self.canInfo.waterTemp +
                                           self.p_WaterTemp * 3)

        if self.canInfo.oilTemp >= 200:
            self.p_OilTemp = -1
        elif self.canInfo.oilTemp < 1:
            self.p_OilTemp = 1
        self.canInfo.oilTemp = OilTemp(self.canInfo.oilTemp +
                                       self.p_OilTemp * 2)

        if self.canInfo.oilPress >= 5.0:
            self.p_OilPress = -1
        elif self.canInfo.oilPress < 1.0:
            self.p_OilPress = 1
        self.canInfo.oilPress = OilPress(
            round(self.canInfo.oilPress + self.p_OilPress * 0.3, 2))

        if self.canInfo.battery >= 14.0:
            self.p_Battery = -1
        elif self.canInfo.battery < 6.0:
            self.p_Battery = 1
        self.canInfo.battery = Battery(
            round(self.canInfo.battery + self.p_Battery * 0.6, 2))
