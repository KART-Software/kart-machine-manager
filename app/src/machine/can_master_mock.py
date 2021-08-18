from src.machine.can_master_base import (Battery, CanInfo, CanMasterBase,
                                         OilPress, OilTemp, Rpm, WaterTemp)


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
        if self.canInfo.motecInfo.rpm >= Rpm.MAX:
            self.p_Rpm = -1
        elif self.canInfo.motecInfo.rpm < 1:
            self.p_Rpm = 1
        self.canInfo.motecInfo.rpm = Rpm(self.canInfo.motecInfo.rpm +
                                         self.p_Rpm * 87)

        if self.canInfo.motecInfo.waterTemp >= 180:
            self.p_WaterTemp = -1
        elif self.canInfo.motecInfo.waterTemp < 1:
            self.p_WaterTemp = 1
        self.canInfo.motecInfo.waterTemp = WaterTemp(
            self.canInfo.motecInfo.waterTemp + self.p_WaterTemp * 3)

        if self.canInfo.motecInfo.oilTemp >= 200:
            self.p_OilTemp = -1
        elif self.canInfo.motecInfo.oilTemp < 1:
            self.p_OilTemp = 1
        self.canInfo.motecInfo.oilTemp = OilTemp(
            self.canInfo.motecInfo.oilTemp + self.p_OilTemp * 2)

        if self.canInfo.motecInfo.oilPress >= 200.0:
            self.p_OilPress = -1
        elif self.canInfo.motecInfo.oilPress < 1.0:
            self.p_OilPress = 1
        self.canInfo.motecInfo.oilPress = OilPress(
            round(self.canInfo.motecInfo.oilPress + self.p_OilPress * 0.3, 2))

        if self.canInfo.motecInfo.battery >= 14.0:
            self.p_Battery = -1
        elif self.canInfo.motecInfo.battery < 6.0:
            self.p_Battery = 1
        self.canInfo.motecInfo.battery = Battery(
            round(self.canInfo.motecInfo.battery + self.p_Battery * 0.6, 2))
