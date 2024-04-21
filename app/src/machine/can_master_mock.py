from src.machine.can_master_base import (Battery, CanInfo, CanMasterBase,
                                         GearType, MotecInfo, OilPress,
                                         OilTemp, Rpm, WaterTemp)


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
        self.p_GearType = 1

    def updateCanInfo(self):
        if self.canInfo.motecInfo.rpm >= Rpm.MAX:
            self.p_Rpm = -1
        elif self.canInfo.motecInfo.rpm < 1:
            self.p_Rpm = 1
        self.canInfo.motecInfo[MotecInfo.INDEX_RPM] += self.p_Rpm * 87

        if self.canInfo.motecInfo.waterTemp >= 180:
            self.p_WaterTemp = -1
        elif self.canInfo.motecInfo.waterTemp < 1:
            self.p_WaterTemp = 1
        self.canInfo.motecInfo[
            MotecInfo.INDEX_WATER_TEMP] += self.p_WaterTemp * 30

        if self.canInfo.motecInfo.oilTemp >= 200:
            self.p_OilTemp = -1
        elif self.canInfo.motecInfo.oilTemp < 1:
            self.p_OilTemp = 1
        self.canInfo.motecInfo[MotecInfo.INDEX_OIL_TEMP] += self.p_OilTemp * 20

        if self.canInfo.motecInfo.oilPress >= 200.0:
            self.p_OilPress = -1
        elif self.canInfo.motecInfo.oilPress < 1.0:
            self.p_OilPress = 1
        self.canInfo.motecInfo[MotecInfo.INDEX_OIL_PRESS] += int(
            self.p_OilPress * 3)

        if self.canInfo.motecInfo.battery >= 14.0:
            self.p_Battery = -1
        elif self.canInfo.motecInfo.battery < 6.0:
            self.p_Battery = 1
        self.canInfo.motecInfo[MotecInfo.INDEX_BATTERY] += self.p_Battery * 60

        if self.canInfo.motecInfo.gearType >= 6:
            self.p_GearType = -1
        elif self.canInfo.motecInfo.gearType <= 0:
            self.p_GearType = 1
        self.canInfo.motecInfo[
            MotecInfo.INDEX_GEAR_SENSOR_VOLTAGE] += self.p_GearType * 30
