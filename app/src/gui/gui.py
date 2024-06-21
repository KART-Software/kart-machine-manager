import sys
from abc import ABCMeta, abstractmethod

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QFont, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)

from src.models.models import (
    DashMachineInfo,
    GearType,
    Message,
    OilPress,
    OilPressStatus,
    OilTemp,
    OilTempStatus,
    Rpm,
    RpmStatus,
    WaterTemp,
    WaterTempStatus,
)


class WindowListener(metaclass=ABCMeta):
    @abstractmethod
    def onUpdate(self) -> None:
        pass


class MainWindow(QDialog):
    def __init__(self, listener: WindowListener):
        super(MainWindow, self).__init__(None)

        self.resize(800, 480)

        self.listener = listener

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.listener.onUpdate)
        self.timer.start(100)

        palette = QApplication.palette()
        palette.setColor(self.backgroundRole(), QColor("#000"))
        palette.setColor(self.foregroundRole(), QColor("#FFF"))
        self.setPalette(palette)

        self.dashboardTitleFontSmall = QFont("Arial", 18)
        self.dashboardTitleFont = QFont("Arial", 15)
        # self.dashboardTitleFont.setBold(True)
        self.dashboardValueFont = QFont("Arial", 40)
        # self.dashboardValueFont.setBold(True)
        self.borderColor = "#FFF"
        self.labelBackgroundColor = "#000"
        self.dashboardTitleColor = "#FD6"

        # self.createRpmBar()
        self.createTopGroupBox()
        self.createLeftGroupBox()
        self.createCenterGroupBox()
        self.createRightGroupBox()
        self.createBottomGroupBox()

        mainLayout = QGridLayout()

        # mainLayout.setContentsMargins(1, 1, 1, 1)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        self.setLayout(mainLayout)
        # mainLayout.addWidget(self.rpmBar, 0, 0, 1, 3)
        mainLayout.addWidget(self.topGroupBox, 0, 0, 1, 3)
        mainLayout.addWidget(self.leftGroupBox, 1, 0)
        mainLayout.addWidget(self.centerGroupBox, 1, 1)
        mainLayout.addWidget(self.rightGroupBox, 1, 2)
        mainLayout.addWidget(self.bottomGroupBox, 2, 0, 1, 3)

    def updateDashboard(self, dashMachineInfo: DashMachineInfo, message: Message):
        # self.setRpmBar(dashMachineInfo.rpm)
        self.setRpmLightBox1Color(dashMachineInfo.rpm)
        self.setRpmLightBox2Color(dashMachineInfo.rpm)
        self.setRpmLightBox3Color(dashMachineInfo.rpm)
        self.setRpmLightBox4Color(dashMachineInfo.rpm)
        self.setRpmLightBox5Color(dashMachineInfo.rpm)
        self.setRpmLightBox6Color(dashMachineInfo.rpm)
        self.setRpmLightBox7Color(dashMachineInfo.rpm)
        self.setRpmLightBox8Color(dashMachineInfo.rpm)
        self.setRpmLightBox9Color(dashMachineInfo.rpm)
        self.setRpmLightBox10Color(dashMachineInfo.rpm)
        self.setRpmLightBox11Color(dashMachineInfo.rpm)
        self.setRpmLightBox12Color(dashMachineInfo.rpm)
        self.setRpmLabel(dashMachineInfo.rpm)
        self.setWaterTempLabel(dashMachineInfo.waterTemp)
        self.setOilTempLabel(dashMachineInfo.oilTemp)
        self.setOilPressLabel(dashMachineInfo.oilPress)
        # self.setFuelRemainLabel(machineInfo.fuelRemain)
        # self.setBatteryLabel(dashMachineInfo.battery)
        # self.setLapTimeLabel(machineInfo.lapTime)
        self.setGearLabel(dashMachineInfo.gearVoltage.gearType)

    # ------------------------------Define Group Box------------------------

    def createRpmBar(self):
        self.rpmBar = QProgressBar(self)
        self.rpmBar.setMaximum(Rpm.MAX)
        self.rpmBar.setValue(0)
        self.rpmBar.setTextVisible(False)
        # self.rpmBar.setStyleSheet(
        #     """
        #     QProgressBar
        #         {
        #             background-color: #000;
        #             border-radius: 5px;
        #             height: 30px;
        #             padding: 0px;
        #         }
        #     QProgressBar::chunk
        #         {
        #             background-color: #0F0;
        #             width: 8px;
        #             margin: 1px;
        #         }
        # """
        # )
        self.rpmBar.setFixedHeight(50)

    def setRpmBar(self, rpm: Rpm):
        self.rpmBar.setValue(int(rpm))
        if rpm.status == RpmStatus.LOW:
            color = "#0F0"
        elif rpm.status == RpmStatus.MIDDLE:
            color = "#FF0"
        elif rpm.status == RpmStatus.HIGH:
            color = "#F00"
        elif rpm.status == RpmStatus.SHIFT:
            color = "#00F"
        self.rpmBar.setStyleSheet(
            """
            QProgressBar
                {
                    background-color: #000;
                    border-radius: 5px;
                    height: 30px;
                    padding: 0px;
                }
            QProgressBar::chunk
                {
                    background-color: %s;
                    width: 8px;
                    margin: 1px;
                }
        """
            % (color)
        )

    def createTopGroupBox(self):
        self.topGroupBox = QGroupBox()
        self.topGroupBox.setFlat(True)
        self.topGroupBox.setStyleSheet("border:0;")
        # self.topGroupBox.setStyleSheet(
        #     "border: 2px solid; border-color:" + self.borderColor
        # )
        # self.topGroupBox.setGeometry(1, 81, 200, 320)
        self.topGroupBox.setFixedSize(800, 50)

        self.rpmLightThreshold1 = 1000
        self.rpmLightThreshold2 = 2000
        self.rpmLightThreshold3 = 3000
        self.rpmLightThreshold4 = 4000
        self.rpmLightThreshold5 = 5000
        self.rpmLightThreshold6 = 5500
        self.rpmLightThreshold7 = 6000
        self.rpmLightThreshold8 = 6500
        self.rpmLightThreshold9 = 7000
        self.rpmLightThreshold10 = 7500
        self.rpmLightThreshold11 = 8000
        self.rpmLightThreshold12 = 8500
        self.rpmLightShiftPoint = 9000
        self.offLightColor = "#333"
        self.greenLightColor = "#0F0"
        self.yellowLightColor = "#FF0"
        self.redLightColor = "#F00"
        self.blueLightColor = "#22F"

        layout = QGridLayout()

        self.createRpmLightBox1()
        self.createRpmLightBox2()
        self.createRpmLightBox3()
        self.createRpmLightBox4()
        self.createRpmLightBox5()
        self.createRpmLightBox6()
        self.createRpmLightBox7()
        self.createRpmLightBox8()
        self.createRpmLightBox9()
        self.createRpmLightBox10()
        self.createRpmLightBox11()
        self.createRpmLightBox12()

        layout.addWidget(self.rpmLightBox1, 0, 0)
        layout.addWidget(self.rpmLightBox2, 0, 1)
        layout.addWidget(self.rpmLightBox3, 0, 2)
        layout.addWidget(self.rpmLightBox4, 0, 3)
        layout.addWidget(self.rpmLightBox5, 0, 4)
        layout.addWidget(self.rpmLightBox6, 0, 5)
        layout.addWidget(self.rpmLightBox7, 0, 6)
        layout.addWidget(self.rpmLightBox8, 0, 7)
        layout.addWidget(self.rpmLightBox9, 0, 8)
        layout.addWidget(self.rpmLightBox10, 0, 9)
        layout.addWidget(self.rpmLightBox11, 0, 10)
        layout.addWidget(self.rpmLightBox12, 0, 11)

        # layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(0)

        self.topGroupBox.setLayout(layout)

    # region new RPM light--------------------------------------

    def createRpmLightBox1(self):
        self.rpmLightBox1 = QGroupBox()
        self.rpmLightBox1.setFlat(True)
        self.rpmLightBox1.setStyleSheet("border:0;")
        self.rpmLightBox1.setFixedSize(50, 50)
        # self.rpmLightBox1.setStyleSheet("background-color: " + "#0F0" + ";")

    def setRpmLightBox1Color(self, rpm: Rpm):
        if rpm < self.rpmLightThreshold1:
            color = self.offLightColor
        elif rpm < self.rpmLightShiftPoint:
            color = self.greenLightColor
        else:
            color = self.blueLightColor
        self.rpmLightBox1.setStyleSheet("background-color: " + color + ";")

    def createRpmLightBox2(self):
        self.rpmLightBox2 = QGroupBox()
        self.rpmLightBox2.setFlat(True)
        self.rpmLightBox2.setStyleSheet("border:0;")
        self.rpmLightBox2.setFixedSize(50, 50)
        # self.rpmLightBox2.setStyleSheet("background-color: " + "#0F0" + ";")

    def setRpmLightBox2Color(self, rpm: Rpm):
        if rpm < self.rpmLightThreshold2:
            color = self.offLightColor
        elif rpm < self.rpmLightShiftPoint:
            color = self.greenLightColor
        else:
            color = self.blueLightColor
        self.rpmLightBox2.setStyleSheet("background-color: " + color + ";")

    def createRpmLightBox3(self):
        self.rpmLightBox3 = QGroupBox()
        self.rpmLightBox3.setFlat(True)
        self.rpmLightBox3.setStyleSheet("border:0;")
        self.rpmLightBox3.setFixedSize(50, 50)
        # self.rpmLightBox3.setStyleSheet("background-color: " + "#0F0" + ";")

    def setRpmLightBox3Color(self, rpm: Rpm):
        if rpm < self.rpmLightThreshold3:
            color = self.offLightColor
        elif rpm < self.rpmLightShiftPoint:
            color = self.greenLightColor
        else:
            color = self.blueLightColor
        self.rpmLightBox3.setStyleSheet("background-color: " + color + ";")

    def createRpmLightBox4(self):
        self.rpmLightBox4 = QGroupBox()
        self.rpmLightBox4.setFlat(True)
        self.rpmLightBox4.setStyleSheet("border:0;")
        self.rpmLightBox4.setFixedSize(50, 50)
        # self.rpmLightBox4.setStyleSheet("background-color: " + "#0F0" + ";")

    def setRpmLightBox4Color(self, rpm: Rpm):
        if rpm < self.rpmLightThreshold4:
            color = self.offLightColor
        elif rpm < self.rpmLightShiftPoint:
            color = self.greenLightColor
        else:
            color = self.blueLightColor
        self.rpmLightBox4.setStyleSheet("background-color: " + color + ";")

    def createRpmLightBox5(self):
        self.rpmLightBox5 = QGroupBox()
        self.rpmLightBox5.setFlat(True)
        self.rpmLightBox5.setStyleSheet("border:0;")
        self.rpmLightBox5.setFixedSize(50, 50)
        # self.rpmLightBox5.setStyleSheet("background-color: " + "#FF0" + ";")

    def setRpmLightBox5Color(self, rpm: Rpm):
        if rpm < self.rpmLightThreshold5:
            color = self.offLightColor
        elif rpm < self.rpmLightShiftPoint:
            color = self.yellowLightColor
        else:
            color = self.blueLightColor
        self.rpmLightBox5.setStyleSheet("background-color: " + color + ";")

    def createRpmLightBox6(self):
        self.rpmLightBox6 = QGroupBox()
        self.rpmLightBox6.setFlat(True)
        self.rpmLightBox6.setStyleSheet("border:0;")
        self.rpmLightBox6.setFixedSize(50, 50)
        # self.rpmLightBox6.setStyleSheet("background-color: " + "#FF0" + ";")

    def setRpmLightBox6Color(self, rpm: Rpm):
        if rpm < self.rpmLightThreshold6:
            color = self.offLightColor
        elif rpm < self.rpmLightShiftPoint:
            color = self.yellowLightColor
        else:
            color = self.blueLightColor
        self.rpmLightBox6.setStyleSheet("background-color: " + color + ";")

    def createRpmLightBox7(self):
        self.rpmLightBox7 = QGroupBox()
        self.rpmLightBox7.setFlat(True)
        self.rpmLightBox7.setStyleSheet("border:0;")
        self.rpmLightBox7.setFixedSize(50, 50)
        # self.rpmLightBox7.setStyleSheet("background-color: " + "#FF0" + ";")

    def setRpmLightBox7Color(self, rpm: Rpm):
        if rpm < self.rpmLightThreshold7:
            color = self.offLightColor
        elif rpm < self.rpmLightShiftPoint:
            color = self.yellowLightColor
        else:
            color = self.blueLightColor
        self.rpmLightBox7.setStyleSheet("background-color: " + color + ";")

    def createRpmLightBox8(self):
        self.rpmLightBox8 = QGroupBox()
        self.rpmLightBox8.setFlat(True)
        self.rpmLightBox8.setStyleSheet("border:0;")
        self.rpmLightBox8.setFixedSize(50, 50)
        # self.rpmLightBox8.setStyleSheet("background-color: " + "#FF0" + ";")

    def setRpmLightBox8Color(self, rpm: Rpm):
        if rpm < self.rpmLightThreshold8:
            color = self.offLightColor
        elif rpm < self.rpmLightShiftPoint:
            color = self.yellowLightColor
        else:
            color = self.blueLightColor
        self.rpmLightBox8.setStyleSheet("background-color: " + color + ";")

    def createRpmLightBox9(self):
        self.rpmLightBox9 = QGroupBox()
        self.rpmLightBox9.setFlat(True)
        self.rpmLightBox9.setStyleSheet("border:0;")
        self.rpmLightBox9.setFixedSize(50, 50)
        # self.rpmLightBox9.setStyleSheet("background-color: " + "#F00" + ";")

    def setRpmLightBox9Color(self, rpm: Rpm):
        if rpm < self.rpmLightThreshold9:
            color = self.offLightColor
        elif rpm < self.rpmLightShiftPoint:
            color = self.redLightColor
        else:
            color = self.blueLightColor
        self.rpmLightBox9.setStyleSheet("background-color: " + color + ";")

    def createRpmLightBox10(self):
        self.rpmLightBox10 = QGroupBox()
        self.rpmLightBox10.setFlat(True)
        self.rpmLightBox10.setStyleSheet("border:0;")
        self.rpmLightBox10.setFixedSize(50, 50)
        # self.rpmLightBox10.setStyleSheet("background-color: " + "#F00" + ";")

    def setRpmLightBox10Color(self, rpm: Rpm):
        if rpm < self.rpmLightThreshold10:
            color = self.offLightColor
        elif rpm < self.rpmLightShiftPoint:
            color = self.redLightColor
        else:
            color = self.blueLightColor
        self.rpmLightBox10.setStyleSheet("background-color: " + color + ";")

    def createRpmLightBox11(self):
        self.rpmLightBox11 = QGroupBox()
        self.rpmLightBox11.setFlat(True)
        self.rpmLightBox11.setStyleSheet("border:0;")
        self.rpmLightBox11.setFixedSize(50, 50)
        # self.rpmLightBox11.setStyleSheet("background-color: " + "#00F" + ";")

    def setRpmLightBox11Color(self, rpm: Rpm):
        if rpm < self.rpmLightThreshold11:
            color = self.offLightColor
        elif rpm < self.rpmLightShiftPoint:
            color = self.blueLightColor
        else:
            color = self.blueLightColor
        self.rpmLightBox11.setStyleSheet("background-color: " + color + ";")

    def createRpmLightBox12(self):
        self.rpmLightBox12 = QGroupBox()
        self.rpmLightBox12.setFlat(True)
        self.rpmLightBox12.setStyleSheet("border:0;")
        self.rpmLightBox12.setFixedSize(50, 50)
        # self.rpmLightBox12.setStyleSheet("background-color: " + "#00F" + ";")

    def setRpmLightBox12Color(self, rpm: Rpm):
        if rpm < self.rpmLightThreshold12:
            color = self.offLightColor
        elif rpm < self.rpmLightShiftPoint:
            color = self.blueLightColor
        else:
            color = self.blueLightColor
        self.rpmLightBox12.setStyleSheet("background-color: " + color + ";")

    # endregion new RPM light ---------------------------------------

    def createLeftGroupBox(self):
        self.leftGroupBox = QGroupBox()
        self.leftGroupBox.setFlat(True)
        self.leftGroupBox.setStyleSheet("border:0;")
        # self.leftGroupBox.setStyleSheet(
        #     "border: 1px solid; border-color:" + self.borderColor
        # )
        # self.leftGroupBox.setGeometry(1, 81, 200, 320)
        self.leftGroupBox.setFixedSize(300, 380)

        layout = QGridLayout()
        # layout = QVBoxLayout()

        self.createWaterTempGroupBox()
        self.createOilTempGroupBox()
        self.createOilPressGroupBox()
        self.createFuelPressGroupBox()
        self.createFanSwitchStateGroupBox()
        self.createBrakeBiasGroupBox()

        layout.addWidget(self.waterTempGroupBox, 0, 0)
        layout.addWidget(self.oilTempGroupBox, 1, 0)
        layout.addWidget(self.oilPressGroupBox, 1, 1)
        layout.addWidget(self.fuelPressGroupBox, 0, 1)
        layout.addWidget(self.fanSwitchStateGroupBox, 2, 0)
        layout.addWidget(self.brakeBiasGroupBox, 2, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.leftGroupBox.setLayout(layout)

    def createCenterGroupBox(self):
        self.centerGroupBox = QGroupBox()
        self.centerGroupBox.setFlat(True)
        self.centerGroupBox.setStyleSheet("border: 0px;")
        # self.centerGroupBox.setStyleSheet(
        #     "border: 1px solid; border-color:" + self.borderColor
        # )
        # self.centerGroupBox.setGeometry(301, 81, 200, 320)
        self.centerGroupBox.setFixedSize(200, 380)

        layout = QGridLayout()

        self.rpmLabel = QLabel(self)
        # self.rpmLabel.setText("3454")
        self.rpmLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rpmLabel.setFont(QFont("Arial", 30))
        self.rpmLabel.setStyleSheet("color : #FFF; background-color: #000")

        self.gearLabel = QLabel(self)
        # gearLabel.setText("2")
        self.gearLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.gearLabel.setFont(QFont("Arial", 180))
        self.gearLabel.setStyleSheet("color : #FFF; background-color: #000")

        # self.kartLogoIcon = QPixmap("src\gui\icons\kart_logo.png")
        # self.kartLogoIconLable = QLabel(self)
        # self.kartLogoIconLable.setPixmap(self.kartLogoIcon)
        # self.kartLogoIconLable.setStyleSheet("background-color: #000")
        # self.kartLogoIconLable.setFixedSize(196, 50)
        # self.kartLogoIconLable.setAlignment(QtCore.Qt.AlignCenter)
        # self.kartLogoIconLable.setScaledContents(True)

        self.timeLabel = QLabel(self)
        self.timeLabel.setText("15:40:39")
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setFont(QFont("Times New Roman", 35))
        self.timeLabel.setStyleSheet("color : #FFF; background-color: #000")

        # speedLabel = QLabel(self)
        # speedLabel.setText("16")
        # speedLabel.setAlignment(QtCore.Qt.AlignCenter)
        # speedLabel.setFont(QFont("Arial", 50))
        # speedLabel.setStyleSheet("QLabel { color : #FFF; }")
        # 速度表示なし#

        layout.addWidget(self.rpmLabel, 0, 0, 1, 2)
        layout.addWidget(self.gearLabel, 1, 0, 1, 2)
        # layout.addWidget(self.kartLogoIconLable, 2, 0, 1, 2)
        layout.addWidget(self.timeLabel, 2, 0, 1, 2)
        # layout.addWidget(speedLabel, 2, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.centerGroupBox.setLayout(layout)

    def createRightGroupBox(self):
        self.rightGroupBox = QGroupBox()
        self.rightGroupBox.setFlat(True)
        self.rightGroupBox.setStyleSheet("border:0;")
        # self.rightGroupBox.setStyleSheet(
        #     "border: 1px solid; border-color:" + self.borderColor
        # )
        self.rightGroupBox.setGeometry(501, 81, 200, 320)
        self.rightGroupBox.setFixedSize(300, 380)

        layout = QGridLayout()

        # self.createFuelRemainGroupBox()
        self.createThrottlePositionGroupBox()
        self.createTpsBar()
        self.createAccelerationPedalPositionGroupBox()
        self.createAppsBar()
        self.createBrakePressFrontGroupBox()
        self.createBpsFrontBar()
        self.createBrakePressRearGroupBox()
        self.createBpsRearBar()

        # layout.addWidget(self.fuelRemainGroupBox, 0, 0)
        layout.addWidget(self.throttlePositionGroupBox, 0, 0)
        layout.addWidget(self.tpsBar, 0, 1)
        layout.addWidget(self.appsBar, 0, 2)
        layout.addWidget(self.accelerationPedalPositionGroupBox, 0, 3)
        layout.addWidget(self.BrakePressFrontGroupBox, 1, 0)
        layout.addWidget(self.bpsFrontBar, 1, 1)
        layout.addWidget(self.bpsRearBar, 1, 2)
        layout.addWidget(self.brakePressRGroupBox, 1, 3)

        # layout.setColumnStretch(0, 2)
        # layout.setColumnStretch(1, 1)
        # layout.setColumnStretch(2, 1)
        # layout.setColumnStretch(3, 2)
        # layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(2)

        self.rightGroupBox.setLayout(layout)

    def createBottomGroupBox(self):
        self.bottomGroupBox = QGroupBox()
        self.bottomGroupBox.setFlat(True)
        self.bottomGroupBox.setStyleSheet("border: 0px;")
        # self.bottomGroupBox.setStyleSheet(
        #     "border: 1px solid; border-color:" + self.borderColor
        # )
        # self.bottomGroupBox.setGeometry(1, 401, 800, 80)
        self.bottomGroupBox.setFixedSize(800, 50)

        layout = QGridLayout()

        self.createBatteryGroupBox()
        self.createMessageGroupBox()
        self.createLapTimeGroupBox()

        layout.addWidget(self.messageGroupBox, 0, 0)
        layout.addWidget(self.lapTimeGroupBox, 0, 1)
        layout.addWidget(self.batteryGroupBox, 0, 2)
        layout.setColumnStretch(0, 10)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 3)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.bottomGroupBox.setLayout(layout)

    # ------------------------- Define Variable Group Box or Label -------------------

    # ---RPM---
    def setRpmLabel(self, rpm: Rpm):
        self.rpmLabel.setText(str(rpm))

    # ---Gear---
    def setGearLabel(self, gearType: GearType):
        if int(gearType) == GearType.NEUTRAL:
            self.gearLabel.setText("N")
            self.gearLabel.setStyleSheet("color : #FD6;")
        else:
            self.gearLabel.setText(str(int(gearType)))
            self.gearLabel.setStyleSheet("color : #FFF;")

    # ---Water tempreture---
    def createWaterTempGroupBox(self):
        self.waterTempGroupBox = QGroupBox()
        self.waterTempGroupBox.setFlat(True)

        layout = QGridLayout()

        waterTempTitleLabel = QLabel(self)
        waterTempTitleLabel.setText("Water Temp")
        waterTempTitleLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        waterTempTitleLabel.setFont(self.dashboardTitleFont)
        waterTempTitleLabel.setStyleSheet(
            "color :"
            + self.dashboardTitleColor
            + "; background-color:"
            + self.labelBackgroundColor
        )

        self.waterTempLabel = QLabel(self)
        # self.waterTempLabel.setText("114")
        self.waterTempLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.waterTempLabel.setFont(self.dashboardValueFont)
        self.waterTempLabel.setStyleSheet("QLabel { color : #FFF; }")

        layout.addWidget(waterTempTitleLabel, 0, 0)
        layout.addWidget(self.waterTempLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.waterTempGroupBox.setLayout(layout)

    def setWaterTempLabel(self, waterTemp: WaterTemp):
        self.waterTempLabel.setText(str(waterTemp))

        if waterTemp.status == WaterTempStatus.LOW:
            color = "#00F"
        elif waterTemp.status == WaterTempStatus.MIDDLE:
            color = "#000"
        elif waterTemp.status == WaterTempStatus.HIGH:
            color = "#F00"

        self.waterTempLabel.setStyleSheet(
            "color : #FFF; background-color:" + color + ";"
        )

    # ---Oil tempreture---
    def createOilTempGroupBox(self):
        self.oilTempGroupBox = QGroupBox()
        self.oilTempGroupBox.setFlat(True)

        layout = QGridLayout()

        oilTempTitleLabel = QLabel(self)
        oilTempTitleLabel.setText("Oil Temp")
        oilTempTitleLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        oilTempTitleLabel.setFont(self.dashboardTitleFont)
        oilTempTitleLabel.setStyleSheet(
            "color :"
            + self.dashboardTitleColor
            + "; background-color:"
            + self.labelBackgroundColor
        )

        self.oilTempLabel = QLabel(self)
        # self.oilTempLabel.setText("114")
        self.oilTempLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.oilTempLabel.setFont(self.dashboardValueFont)
        self.oilTempLabel.setStyleSheet("QLabel { color : #FFF; }")

        layout.addWidget(oilTempTitleLabel, 0, 0)
        layout.addWidget(self.oilTempLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.oilTempGroupBox.setLayout(layout)

    def setOilTempLabel(self, oilTemp: OilTemp):
        self.oilTempLabel.setText(str(oilTemp))

        if oilTemp.status == OilTempStatus.LOW:
            color = "#00F"
        elif oilTemp.status == OilTempStatus.MIDDLE:
            color = "#000"
        elif oilTemp.status == OilTempStatus.HIGH:
            color = "#F00"

        self.oilTempLabel.setStyleSheet("color : #FFF; background-color:" + color + ";")

    # ---Oil pressure---
    def createOilPressGroupBox(self):
        self.oilPressGroupBox = QGroupBox()
        self.oilPressGroupBox.setFlat(True)

        layout = QGridLayout()

        oilPressTitleLabel = QLabel(self)
        oilPressTitleLabel.setText("Oil Press")
        oilPressTitleLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        oilPressTitleLabel.setFont(self.dashboardTitleFont)
        oilPressTitleLabel.setStyleSheet(
            "color :"
            + self.dashboardTitleColor
            + "; background-color:"
            + self.labelBackgroundColor
        )

        self.oilPressLabel = QLabel(self)
        # self.oilPressLabel.setText("114")
        self.oilPressLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.oilPressLabel.setFont(self.dashboardValueFont)
        self.oilPressLabel.setStyleSheet("QLabel { color : #FFF; }")

        layout.addWidget(oilPressTitleLabel, 0, 0)
        layout.addWidget(self.oilPressLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.oilPressGroupBox.setLayout(layout)

    def setOilPressLabel(self, oilPress: OilPress):
        self.oilPressLabel.setText(str(round(oilPress, 2)))

        if oilPress.status == OilPressStatus.LOW:
            color = "#F00"
        elif oilPress.status == OilPressStatus.HIGH:
            color = "#000"

        # self.oilPressGroupBox.setStyleSheet("background-color: " + color + ";")
        self.oilPressLabel.setStyleSheet(
            "color : #FFF; background-color:" + color + ";"
        )

    # ---Fuel pressure---
    def createFuelPressGroupBox(self):
        self.fuelPressGroupBox = QGroupBox()
        self.fuelPressGroupBox.setFlat(True)

        layout = QGridLayout()

        fuelPressTitleLabel = QLabel(self)
        fuelPressTitleLabel.setText("Fuel Press")
        fuelPressTitleLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        fuelPressTitleLabel.setFont(self.dashboardTitleFont)
        fuelPressTitleLabel.setStyleSheet(
            "color :"
            + self.dashboardTitleColor
            + "; background-color:"
            + self.labelBackgroundColor
        )

        self.fuelPressLabel = QLabel(self)
        self.fuelPressLabel.setText("400")
        self.fuelPressLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fuelPressLabel.setFont(self.dashboardValueFont)
        self.fuelPressLabel.setStyleSheet("QLabel { color : #FFF; }")

        layout.addWidget(fuelPressTitleLabel, 0, 0)
        layout.addWidget(self.fuelPressLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.fuelPressGroupBox.setLayout(layout)

    # ---Fans switch state---
    def createFanSwitchStateGroupBox(self):
        self.fanSwitchStateGroupBox = QGroupBox()
        self.fanSwitchStateGroupBox.setFlat(True)
        # self.fanStateGroupBox.setFixedSize(150, 190)
        layout = QGridLayout()

        fanSwitchStateTitleLabel = QLabel(self)
        fanSwitchStateTitleLabel.setText("Fan Switch")
        fanSwitchStateTitleLabel.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom
        )
        fanSwitchStateTitleLabel.setFont(self.dashboardTitleFont)
        fanSwitchStateTitleLabel.setStyleSheet(
            "color :"
            + self.dashboardTitleColor
            + "; background-color:"
            + self.labelBackgroundColor
        )

        self.fanSwitchStateLabel = QLabel(self)
        self.fanSwitchStateLabel.setText("ON")
        self.fanSwitchStateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fanSwitchStateLabel.setFont(self.dashboardValueFont)
        self.fanSwitchStateLabel.setStyleSheet("color : #FFF; background-color: #0F0")

        layout.addWidget(fanSwitchStateTitleLabel, 0, 0)
        layout.addWidget(self.fanSwitchStateLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.fanSwitchStateGroupBox.setLayout(layout)

    # ---Brake Bias---
    def createBrakeBiasGroupBox(self):
        self.brakeBiasGroupBox = QGroupBox()
        self.brakeBiasGroupBox.setFlat(True)
        # self.fanStateGroupBox.setFixedSize(150, 190)
        layout = QGridLayout()

        brakeBiasTitleLabel = QLabel(self)
        brakeBiasTitleLabel.setText("Brk Bias(F%)")
        brakeBiasTitleLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        brakeBiasTitleLabel.setFont(self.dashboardTitleFont)
        brakeBiasTitleLabel.setStyleSheet(
            "color :"
            + self.dashboardTitleColor
            + "; background-color:"
            + self.labelBackgroundColor
        )

        self.brakeBiasLabel = QLabel(self)
        self.brakeBiasLabel.setText("0.61")
        self.brakeBiasLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.brakeBiasLabel.setFont(self.dashboardValueFont)
        self.brakeBiasLabel.setStyleSheet("color : #FFF; background-color: #000")

        layout.addWidget(brakeBiasTitleLabel, 0, 0)
        layout.addWidget(self.brakeBiasLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.brakeBiasGroupBox.setLayout(layout)

    # def createBatteryGroupBox(self):
    #     self.batteryGroupBox = QGroupBox()
    #     self.batteryGroupBox.setFlat(True)
    #     self.batteryGroupBox.setStyleSheet("border:0;")
    #     self.batteryGroupBox.setFixedSize(300, 80)

    #     layout = QGridLayout()

    #     batteryTitleLabel = QLabel(self)
    #     batteryTitleLabel.setText("Battery")
    #     batteryTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
    #     batteryTitleLabel.setFont(self.dashboardTitleFont)
    #     batteryTitleLabel.setStyleSheet("QLabel { color : #FFF; }")

    #     self.batteryLabel = QLabel(self)
    #     # self.batteryLabel.setText("114")
    #     self.batteryLabel.setAlignment(QtCore.Qt.AlignCenter)
    #     self.batteryLabel.setFont(self.dashboardValueFont)
    #     self.batteryLabel.setStyleSheet("QLabel { color : #FFF; }")

    #     layout.addWidget(batteryTitleLabel, 1, 0)
    #     layout.addWidget(self.batteryLabel, 1, 1)
    #     layout.setRowStretch(1, 3)

    #     layout.setContentsMargins(0, 0, 0, 0)
    #     layout.setSpacing(1)

    #     self.batteryGroupBox.setLayout(layout)

    # def createFuelRemainGroupBox(self):

    #     self.fuelRemainGroupBox = QGroupBox()
    #     self.fuelRemainGroupBox.setFlat(True)
    #     self.fuelRemainGroupBox.setStyleSheet("border:0;")

    #     layout = QGridLayout()

    #     fuelRemainTitleLabel = QLabel(self)
    #     fuelRemainTitleLabel.setText("Fuel Remain")
    #     fuelRemainTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
    #     fuelRemainTitleLabel.setFont(self.dashboardTitleFont)
    #     fuelRemainTitleLabel.setStyleSheet("QLabel { color : #FFF; }")

    #     self.fuelRemainLabel = QLabel(self)
    #     # self.fuelRemainLabel.setText("30")
    #     # self.fuelRemainLabel.setAlignment(QtCore.Qt.AlignCenter)
    #     # self.fuelRemainLabel.setFont(self.dashboardValueFont)
    #     # self.fuelRemainLabel.setStyleSheet("QLabel { color : #FFF; }")

    #     layout.addWidget(fuelRemainTitleLabel, 0, 0)
    #     # layout.addWidget(self.fuelRemainLabel, 1, 0)
    #     layout.setRowStretch(1, 3)

    #     layout.setContentsMargins(0, 0, 0, 0)
    #     layout.setSpacing(1)

    #     self.fuelRemainGroupBox.setLayout(layout)

    # def setFuelRemainLabel(self, fuelRemain: FuelRemain):
    #     self.fuelRemainLabel.setText(str(round(fuelRemain, 2)))

    #     if fuelRemain.status == FuelRemainStatus.LOW:
    #         color = "red"
    #     elif fuelRemain.status == FuelRemainStatus.HIGH:
    #         color = "#000"

    #     self.fuelRemainGroupBox.setStyleSheet("background-color: " + color +
    #                                           ";")

    # ---Throttle position---
    def createThrottlePositionGroupBox(self):
        self.throttlePositionGroupBox = QGroupBox()
        self.throttlePositionGroupBox.setFlat(True)
        # self.throttlePositionGroupBox.setFixedSize(150, 190)

        layout = QGridLayout()

        throttlePositionTitleLabel = QLabel(self)
        throttlePositionTitleLabel.setText("TPS")
        throttlePositionTitleLabel.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom
        )
        throttlePositionTitleLabel.setFont(self.dashboardTitleFont)
        throttlePositionTitleLabel.setStyleSheet(
            "color :"
            + self.dashboardTitleColor
            + "; background-color:"
            + self.labelBackgroundColor
        )

        self.throttlePositionLabel = QLabel(self)
        self.throttlePositionLabel.setText("100")
        self.throttlePositionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.throttlePositionLabel.setFont(self.dashboardValueFont)
        self.throttlePositionLabel.setStyleSheet("QLabel { color : #FFF; }")

        layout.addWidget(throttlePositionTitleLabel, 0, 0)
        layout.addWidget(self.throttlePositionLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.throttlePositionGroupBox.setLayout(layout)

    def createTpsBar(self):
        self.tpsBar = QProgressBar(self)
        self.tpsBar.setFixedSize(30, 150)
        self.tpsBar.setMaximum(Rpm.MAX)
        self.tpsBar.setValue(0)
        self.tpsBar.setTextVisible(1)
        self.tpsBar.setOrientation(1)
        self.tpsBar.setStyleSheet(
            """
            QProgressBar
                {
                    border: 2px solid;
                    border-color: #FFF;
                    background-color: #0F0;
                    border-radius: 0px;
                    height: 30px;
                    padding: 0px;
                }
            QProgressBar::chunk
                {
                    background-color: #0F0;
                    width: 8px;
                    margin: 1px;
                }
        """
        )

    # def setTpsBar(self, tps: Rpm):
    #     self.tpsBar.setValue(int(tps))
    #     if tps.status == RpmStatus.LOW:
    #         color = "#0F0"
    #     elif tps.status == RpmStatus.MIDDLE:
    #         color = "#FF0"
    #     elif tps.status == RpmStatus.HIGH:
    #         color = "#F00"
    #     elif tps.status == RpmStatus.SHIFT:
    #         color = "#00F"
    #     self.tpsBar.setStyleSheet(
    #     """
    #     QProgressBar
    #         {
    #             background-color: #000;
    #             border-radius: 5px;
    #             height: 30px;
    #             padding: 0px;
    #         }
    #     QProgressBar::chunk
    #         {
    #             background-color: %s;
    #             width: 8px;
    #             margin: 1px;
    #         }
    # """
    #     % (color)
    # )

    # ---Throttle position---
    def createAccelerationPedalPositionGroupBox(self):
        self.accelerationPedalPositionGroupBox = QGroupBox()
        self.accelerationPedalPositionGroupBox.setFlat(True)
        # self.accelerationPedalPositionGroupBox.setFixedSize(150, 190)

        layout = QGridLayout()

        accelerationPedalPositionTitleLabel = QLabel(self)
        accelerationPedalPositionTitleLabel.setText("APPS")
        accelerationPedalPositionTitleLabel.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom
        )
        accelerationPedalPositionTitleLabel.setFont(self.dashboardTitleFont)
        accelerationPedalPositionTitleLabel.setStyleSheet(
            "color :"
            + self.dashboardTitleColor
            + "; background-color:"
            + self.labelBackgroundColor
        )

        self.accelerationPedalPositionLabel = QLabel(self)
        self.accelerationPedalPositionLabel.setText("100")
        self.accelerationPedalPositionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.accelerationPedalPositionLabel.setFont(self.dashboardValueFont)
        self.accelerationPedalPositionLabel.setStyleSheet("QLabel { color : #FFF; }")

        layout.addWidget(accelerationPedalPositionTitleLabel, 0, 0)
        layout.addWidget(self.accelerationPedalPositionLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.accelerationPedalPositionGroupBox.setLayout(layout)

    def createAppsBar(self):
        self.appsBar = QProgressBar(self)
        self.appsBar.setFixedSize(30, 150)
        self.appsBar.setMaximum(Rpm.MAX)
        self.appsBar.setValue(0)
        self.appsBar.setTextVisible(1)
        self.appsBar.setOrientation(1)
        self.appsBar.setStyleSheet(
            """
            QProgressBar
                {
                    border: 2px solid;
                    border-color: #FFF;
                    background-color: #0F0;
                    border-radius: 0px;
                    height: 30px;
                    padding: 0px;
                }
            QProgressBar::chunk
                {
                    background-color: #0F0;
                    width: 8px;
                    margin: 1px;
                }
        """
        )

    # def setAppsBar(self, tps: Rpm):
    #     self.AppsBar.setValue(int(tps))
    #     if Apps.status == RpmStatus.LOW:
    #         color = "#0F0"
    #     elif Apps.status == RpmStatus.MIDDLE:
    #         color = "#FF0"
    #     elif Apps.status == RpmStatus.HIGH:
    #         color = "#F00"
    #     elif Apps.status == RpmStatus.SHIFT:
    #         color = "#00F"
    #     self.AppsBar.setStyleSheet(
    #     """
    #     QProgressBar
    #         {
    #             background-color: #000;
    #             border-radius: 5px;
    #             height: 30px;
    #             padding: 0px;
    #         }
    #     QProgressBar::chunk
    #         {
    #             background-color: %s;
    #             width: 8px;
    #             margin: 1px;
    #         }
    # """
    #     % (color)
    # )

    # ---Brake pressure---
    def createBrakePressFrontGroupBox(self):
        self.BrakePressFrontGroupBox = QGroupBox()
        self.BrakePressFrontGroupBox.setFlat(True)
        # self.BrakePressFrontGroupBox.setFixedSize(150, 190)

        layout = QGridLayout()

        BrakePressFrontTitleLabel = QLabel(self)
        BrakePressFrontTitleLabel.setText("BPS F")
        BrakePressFrontTitleLabel.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom
        )
        BrakePressFrontTitleLabel.setFont(self.dashboardTitleFont)
        BrakePressFrontTitleLabel.setStyleSheet(
            "color :"
            + self.dashboardTitleColor
            + "; background-color:"
            + self.labelBackgroundColor
        )

        self.BrakePressFrontLabel = QLabel(self)
        self.BrakePressFrontLabel.setText("300")
        self.BrakePressFrontLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.BrakePressFrontLabel.setFont(self.dashboardValueFont)
        self.BrakePressFrontLabel.setStyleSheet("QLabel { color : #FFF; }")

        layout.addWidget(BrakePressFrontTitleLabel, 0, 0)
        layout.addWidget(self.BrakePressFrontLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.BrakePressFrontGroupBox.setLayout(layout)

    def createBpsFrontBar(self):
        self.bpsFrontBar = QProgressBar(self)
        self.bpsFrontBar.setFixedSize(30, 150)
        self.bpsFrontBar.setMaximum(Rpm.MAX)
        self.bpsFrontBar.setValue(0)
        self.bpsFrontBar.setTextVisible(1)
        self.bpsFrontBar.setOrientation(2)
        self.bpsFrontBar.setStyleSheet(
            """
            QProgressBar
                {
                    border: 2px solid;
                    border-color: #FFF;
                    background-color: #F00;
                    border-radius: 0px;
                    height: 30px;
                    padding: 0px;
                }
            QProgressBar::chunk
                {
                    background-color: #0F0;
                    width: 8px;
                    margin: 1px;
                }
        """
        )
        # self.bpsFrontBar.setFixedHeight(30)

    # def setbpsFrontBar(self, bps: Rpm):
    #     self.bpsFrontBar.setValue(int(bps))
    #     if bpsF.status == RpmStatus.LOW:
    #         color = "#0F0"
    #     elif bpsF.status == RpmStatus.MIDDLE:
    #         color = "#FF0"
    #     elif bpsF.status == RpmStatus.HIGH:
    #         color = "#F00"
    #     elif bpsF.status == RpmStatus.SHIFT:
    #         color = "#00F"
    #     self.bpsFrontBar.setStyleSheet(
    #     """
    #     QProgressBar
    #         {
    #             background-color: #000;
    #             border-radius: 5px;
    #             height: 30px;
    #             padding: 0px;
    #         }
    #     QProgressBar::chunk
    #         {
    #             background-color: %s;
    #             width: 8px;
    #             margin: 1px;
    #         }
    # """
    #     % (color)
    # )

    def createBrakePressRearGroupBox(self):
        self.brakePressRGroupBox = QGroupBox()
        self.brakePressRGroupBox.setFlat(True)
        # self.brakePressRGroupBox.setFixedSize(150, 190)

        layout = QGridLayout()

        brakePressRTitleLabel = QLabel(self)
        brakePressRTitleLabel.setText("BPS R")
        brakePressRTitleLabel.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom
        )
        brakePressRTitleLabel.setFont(self.dashboardTitleFont)
        brakePressRTitleLabel.setStyleSheet(
            "color :"
            + self.dashboardTitleColor
            + "; background-color:"
            + self.labelBackgroundColor
        )

        self.brakePressRLabel = QLabel(self)
        self.brakePressRLabel.setText("270")
        self.brakePressRLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.brakePressRLabel.setFont(self.dashboardValueFont)
        self.brakePressRLabel.setStyleSheet("QLabel { color : #FFF; }")

        layout.addWidget(brakePressRTitleLabel, 0, 0)
        layout.addWidget(self.brakePressRLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.brakePressRGroupBox.setLayout(layout)

    def createBpsRearBar(self):
        self.bpsRearBar = QProgressBar(self)
        self.bpsRearBar.setFixedSize(30, 150)
        self.bpsRearBar.setMaximum(Rpm.MAX)
        self.bpsRearBar.setValue(0)
        self.bpsRearBar.setTextVisible(1)
        self.bpsRearBar.setOrientation(2)
        self.bpsRearBar.setStyleSheet(
            """
            QProgressBar
                {
                    border: 2px solid;
                    border-color: #FFF;
                    background-color: #F00;
                    border-radius: 0px;
                    height: 30px;
                    padding: 0px;
                }
            QProgressBar::chunk
                {
                    background-color: #0F0;
                    width: 8px;
                    margin: 1px;
                }
        """
        )
        # self.bpsRearBar.setFixedHeight(30)

    # def setbpsRearBar(self, bps: Rpm):
    #     self.bpsRearBar.setValue(int(bps))
    #     if bpsR.status == RpmStatus.LOW:
    #         color = "#0F0"
    #     elif bpsR.status == RpmStatus.MIDDLE:
    #         color = "#FF0"
    #     elif bpsR.status == RpmStatus.HIGH:
    #         color = "#F00"
    #     elif bpsR.status == RpmStatus.SHIFT:
    #         color = "#00F"
    #     self.bpsRearBar.setStyleSheet(
    #     """
    #     QProgressBar
    #         {
    #             background-color: #000;
    #             border-radius: 5px;
    #             height: 30px;
    #             padding: 0px;
    #         }
    #     QProgressBar::chunk
    #         {
    #             background-color: %s;
    #             width: 8px;
    #             margin: 1px;
    #         }
    # """
    #     % (color)
    # )

    # ---Message---
    def createMessageGroupBox(self):
        self.messageGroupBox = QGroupBox()
        self.messageGroupBox.setFlat(True)
        # self.messageGroupBox.setFixedSize(500, 50)

        layout = QGridLayout()

        # messageTitleLabel = QLabel(self)
        # messageTitleLabel.setText("M")
        # # messageTitleLabel.setFixedSize(50, 50)
        # messageTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        # messageTitleLabel.setFont(self.dashboardTitleFontSmall)
        # messageTitleLabel.setStyleSheet("QLabel { color : #FFF; }")

        self.messageIcon = QPixmap("src\gui\icons\MeesageIcon.png")
        messageIconLabel = QLabel(self)
        messageIconLabel.setPixmap(self.messageIcon)
        messageIconLabel.setFixedSize(50, 50)
        messageIconLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.messageLabel = QLabel(self)
        # self.messageLabel.setText("AHHH! GP2 ENGING!   ")
        self.messageLabel.setText("Messages are shown here.")
        # self.messageLabel.setFixedSize(450, 50)
        self.messageLabel.setAlignment(QtCore.Qt.AlignVCenter)
        self.messageLabel.setFont(self.dashboardTitleFontSmall)
        self.messageLabel.setStyleSheet("QLabel { color : #FFF; }")

        # layout.addWidget(messageTitleLabel, 0, 0)
        layout.addWidget(messageIconLabel, 0, 0)
        layout.addWidget(self.messageLabel, 0, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 5)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.messageGroupBox.setLayout(layout)

    # ---Laptime---
    def createLapTimeGroupBox(self):
        self.lapTimeGroupBox = QGroupBox()
        self.lapTimeGroupBox.setFlat(True)
        # self.lapTimeGroupBox.setFixedSize(150, 50)
        # self.lapTimeGroupBox.setStyleSheet(
        #     "border:0; background-color: " + "#000" + ";"
        # )

        layout = QGridLayout()

        # lapTimeTitleLabel = QLabel(self)
        # lapTimeTitleLabel.setText("L")
        # lapTimeTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        # # lapTimeTitleLabel.setFixedSize(50, 50)
        # lapTimeTitleLabel.setFont(self.dashboardTitleFontSmall)
        # lapTimeTitleLabel.setStyleSheet("QLabel { color : #FFF; }")

        self.laptimeIcon = QPixmap("src\gui\icons\LaptimeIcon.png")
        laptimeIconLabel = QLabel(self)
        laptimeIconLabel.setPixmap(self.laptimeIcon)
        laptimeIconLabel.setFixedSize(50, 50)
        laptimeIconLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.lapTimeLabel = QLabel(self)
        self.lapTimeLabel.setText("55.83s")
        self.lapTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        # self.lapTimeLabel.setFixedSize(100, 50)
        self.lapTimeLabel.setFont(self.dashboardTitleFontSmall)
        self.lapTimeLabel.setStyleSheet("QLabel { color : #FFF; }")

        # layout.addWidget(lapTimeTitleLabel, 0, 0)
        layout.addWidget(laptimeIconLabel, 0, 0)
        layout.addWidget(self.lapTimeLabel, 0, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.lapTimeGroupBox.setLayout(layout)

    # def setLapTimeLabel(self, lapTime: LapTime):
    #     minute = lapTime.seconds // 60
    #     second = lapTime.seconds % 60
    #     aftersecond = lapTime.microseconds // 10000
    #     self.lapTimeLabel.setText(
    #         str(minute) + "." + str(second) + "." + str(aftersecond))

    # ---Battery---
    def createBatteryGroupBox(self):
        self.batteryGroupBox = QGroupBox()
        self.batteryGroupBox.setFlat(True)
        # self.batteryGroupBox.setFixedSize(149, 50)
        # self.batteryGroupBox.setStyleSheet(
        #     "border:1; background-color: " + "#000" + ";"
        # )

        layout = QGridLayout()

        # batteryTitleLabel = QLabel(self)
        # batteryTitleLabel.setText("B")
        # batteryTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        # batteryTitleLabel.setFont(self.dashboardTitleFontSmall)
        # batteryTitleLabel.setStyleSheet("QLabel { color : #FFF; }")

        self.batteryIcon = QPixmap("src\gui\icons\BatteryIcon.png")
        batteryIconLable = QLabel(self)
        batteryIconLable.setPixmap(self.batteryIcon)
        # batteryIconLable.setFixedSize(40, 40)
        batteryIconLable.setAlignment(QtCore.Qt.AlignCenter)
        # batteryIconLable.setScaledContents(True)

        self.batteryLabel = QLabel(self)
        self.batteryLabel.setText("12.4 V")
        # self.batteryLabel.setFixedSize(100, 50)
        self.batteryLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.batteryLabel.setFont(self.dashboardTitleFontSmall)
        self.batteryLabel.setStyleSheet("QLabel { color : #FFF; }")

        # layout.addWidget(batteryTitleLabel, 0, 0)
        layout.addWidget(batteryIconLable, 0, 0)
        layout.addWidget(self.batteryLabel, 0, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.batteryGroupBox.setLayout(layout)

    # def setBatteryLabel(self, battery: Battery):
    #     self.batteryLabel.setText(str(round(battery, 2)))

    #     if battery.status == BatteryStatus.LOW:
    #         color = "#F00"
    #     elif battery.status == BatteryStatus.HIGH:
    #         color = "#000"

    #     self.batteryGroupBox.setStyleSheet("background-color: " + color + ";")
