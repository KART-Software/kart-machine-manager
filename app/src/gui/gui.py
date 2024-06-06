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

        self.dashboardTitleFontSmall = QFont("Calibri", 18)
        self.dashboardTitleFont = QFont("Calibri", 20)
        self.dashboardTitleFont.setBold(True)
        self.dashboardValueFont = QFont("Calibri", 40)
        self.dashboardValueFont.setBold(True)
        self.borderColor = "#666"
        self.labelBackgroundColor = "#666"

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

    # region new RPM light--------------------------------------
    def createTopGroupBox(self):
        self.topGroupBox = QGroupBox()
        self.topGroupBox.setFlat(True)
        self.topGroupBox.setStyleSheet("border:0;")
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

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.topGroupBox.setLayout(layout)

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
        self.leftGroupBox.setStyleSheet(
            "border: 1px solid; border-color:" + self.borderColor
        )
        # self.leftGroupBox.setGeometry(1, 81, 200, 320)
        self.leftGroupBox.setFixedSize(300, 380)

        layout = QGridLayout()
        # layout = QVBoxLayout()

        self.createWaterTempGroupBox()
        self.createOilTempGroupBox()
        self.createOilPressGroupBox()
        self.createFuelPressGroupBox()

        layout.addWidget(self.waterTempGroupBox, 0, 0)
        layout.addWidget(self.oilTempGroupBox, 1, 0)
        layout.addWidget(self.oilPressGroupBox, 1, 1)
        layout.addWidget(self.fuelPressGroupBox, 0, 1)
        # layout.setRowStretch(1, 3)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.leftGroupBox.setLayout(layout)

    def createCenterGroupBox(self):
        self.centerGroupBox = QGroupBox()
        self.centerGroupBox.setFlat(True)
        self.centerGroupBox.setStyleSheet(
            "border: 2px solid; border-color:" + self.borderColor
        )
        # self.centerGroupBox.setGeometry(301, 81, 200, 320)
        self.centerGroupBox.setFixedSize(200, 380)

        layout = QGridLayout()

        self.rpmLabel = QLabel(self)
        # self.rpmLabel.setText("3454")
        self.rpmLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rpmLabel.setFont(QFont("Calibri", 50))
        self.rpmLabel.setStyleSheet("color : #FFF; background-color: #000")

        self.gearLabel = QLabel(self)
        # gearLabel.setText("2")
        self.gearLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.gearLabel.setFont(QFont("Calibri", 180))
        self.gearLabel.setStyleSheet("color : #FFF; background-color: #000")

        self.kartLogoIcon = QPixmap("src\gui\icons\kart_logo.png")
        self.kartLogoIconLable = QLabel(self)
        self.kartLogoIconLable.setPixmap(self.kartLogoIcon)
        self.kartLogoIconLable.setStyleSheet("background-color: #000")
        self.kartLogoIconLable.setFixedSize(196, 50)
        self.kartLogoIconLable.setAlignment(QtCore.Qt.AlignCenter)
        self.kartLogoIconLable.setScaledContents(True)

        # self.carLabel = QLabel(self)
        # self.carLabel.setText("KZ-R20")
        # self.carLabel.setAlignment(QtCore.Qt.AlignCenter)
        # self.carLabel.setFont(QFont("Times New Roman", 25))
        # self.carLabel.setStyleSheet("color : #000; background-color: #FFF")

        # speedLabel = QLabel(self)
        # speedLabel.setText("16")
        # speedLabel.setAlignment(QtCore.Qt.AlignCenter)
        # speedLabel.setFont(QFont("Arial", 50))
        # speedLabel.setStyleSheet("QLabel { color : #FFF; }")
        # 速度表示なし#

        layout.addWidget(self.rpmLabel, 0, 0, 1, 2)
        layout.addWidget(self.gearLabel, 1, 0, 1, 2)
        layout.addWidget(self.kartLogoIconLable, 2, 0, 1, 2)
        # layout.addWidget(self.carLabel, 2, 1, 1, 1)
        # layout.addWidget(speedLabel, 2, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.centerGroupBox.setLayout(layout)

    def createRightGroupBox(self):
        self.rightGroupBox = QGroupBox()
        self.rightGroupBox.setFlat(True)
        self.rightGroupBox.setStyleSheet(
            "border: 1px solid; border-color:" + self.borderColor
        )
        # self.rightGroupBox.setGeometry(501, 81, 200, 320)
        self.rightGroupBox.setFixedSize(300, 380)

        layout = QGridLayout()

        # self.createFuelRemainGroupBox()
        self.createThrottlePositionGroupBox()
        self.createBrakePressGroupBox()
        self.createFanStateGroupBox()
        self.createWaterPumpStateGroupBox()
        # self.createTpsBar()
        # self.createBpsBar()

        # layout.addWidget(self.fuelRemainGroupBox, 0, 0)
        layout.addWidget(self.throttlePositionGroupBox, 0, 0)
        layout.addWidget(self.brakePressGroupBox, 1, 0)
        layout.addWidget(self.fanStateGroupBox, 0, 1)
        layout.addWidget(self.waterPumpStateGroupBox, 1, 1)
        # layout.addWidget(self.tpsBar, 0, 1)
        # layout.addWidget(self.bpsBar, 0, 2)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.rightGroupBox.setLayout(layout)

    def createBottomGroupBox(self):
        self.bottomGroupBox = QGroupBox()
        self.bottomGroupBox.setFlat(True)
        # self.bottomGroupBox.setStyleSheet("border: 1px solid; border-color:#AAA")
        # self.bottomGroupBox.setGeometry(1, 401, 800, 80)
        self.bottomGroupBox.setFixedSize(800, 50)
        self.bottomGroupBox.setStyleSheet(
            "border: 0px solid; border-color:" + self.borderColor
        )

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
        else:
            self.gearLabel.setText(str(int(gearType)))

    # ---Water tempreture---
    def createWaterTempGroupBox(self):
        self.waterTempGroupBox = QGroupBox()
        self.waterTempGroupBox.setFlat(True)

        layout = QGridLayout()

        waterTempTitleLabel = QLabel(self)
        waterTempTitleLabel.setText("Water T(°C)")
        waterTempTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        waterTempTitleLabel.setFont(self.dashboardTitleFont)
        waterTempTitleLabel.setStyleSheet(
            "color : #FFF; background-color:" + self.labelBackgroundColor
        )

        self.waterTempLabel = QLabel(self)
        # self.waterTempLabel.setText("114")
        self.waterTempLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.waterTempLabel.setFont(self.dashboardValueFont)
        self.waterTempLabel.setStyleSheet("QLabel { color : #FFF; }")

        layout.addWidget(waterTempTitleLabel, 0, 0)
        layout.addWidget(self.waterTempLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)

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
        oilTempTitleLabel.setText("Oil T. (°C)")
        oilTempTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        oilTempTitleLabel.setFont(self.dashboardTitleFont)
        oilTempTitleLabel.setStyleSheet(
            "color : #FFF; background-color:" + self.labelBackgroundColor
        )

        self.oilTempLabel = QLabel(self)
        # self.oilTempLabel.setText("114")
        self.oilTempLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.oilTempLabel.setFont(self.dashboardValueFont)
        self.oilTempLabel.setStyleSheet("QLabel { color : #FFF; }")

        layout.addWidget(oilTempTitleLabel, 0, 0)
        layout.addWidget(self.oilTempLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)

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
        oilPressTitleLabel.setText("Oil P. (kPa)")
        oilPressTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        oilPressTitleLabel.setFont(self.dashboardTitleFont)
        oilPressTitleLabel.setStyleSheet(
            "color : #FFF; background-color:" + self.labelBackgroundColor
        )

        self.oilPressLabel = QLabel(self)
        # self.oilPressLabel.setText("114")
        self.oilPressLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.oilPressLabel.setFont(self.dashboardValueFont)
        self.oilPressLabel.setStyleSheet("QLabel { color : #FFF; }")

        layout.addWidget(oilPressTitleLabel, 0, 0)
        layout.addWidget(self.oilPressLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)

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
        fuelPressTitleLabel.setText("Fuel P. (kPa)")
        fuelPressTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        fuelPressTitleLabel.setFont(self.dashboardTitleFont)
        fuelPressTitleLabel.setStyleSheet(
            "color : #FFF; background-color:" + self.labelBackgroundColor
        )

        self.fuelPressLabel = QLabel(self)
        self.fuelPressLabel.setText("400")
        self.fuelPressLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fuelPressLabel.setFont(self.dashboardValueFont)
        self.fuelPressLabel.setStyleSheet("QLabel { color : #FFF; }")

        layout.addWidget(fuelPressTitleLabel, 0, 0)
        layout.addWidget(self.fuelPressLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.fuelPressGroupBox.setLayout(layout)

    #     self.oilPressGroupBox.setStyleSheet("background-color: " + color + ";")

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
        throttlePositionTitleLabel.setText("TPS (%)")
        throttlePositionTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        throttlePositionTitleLabel.setFont(self.dashboardTitleFont)
        throttlePositionTitleLabel.setStyleSheet(
            "color : #FFF; background-color:" + self.labelBackgroundColor
        )

        self.throttlePositionLabel = QLabel(self)
        self.throttlePositionLabel.setText("100.0")
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
        self.tpsBar.setFixedSize(50, 300)
        self.tpsBar.setMaximum(Rpm.MAX)
        self.tpsBar.setValue(0)
        self.tpsBar.setTextVisible(1)
        self.tpsBar.setOrientation(2)
        self.tpsBar.setStyleSheet(
            """
            QProgressBar
                {
                    background-color: #0F0;
                    border-radius: 5px;
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
        # self.tpsBar.setFixedHeight(30)

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

    # ---Brake pressure---
    def createBrakePressGroupBox(self):
        self.brakePressGroupBox = QGroupBox()
        self.brakePressGroupBox.setFlat(True)
        # self.brakePressGroupBox.setFixedSize(150, 190)

        layout = QGridLayout()

        brakePressTitleLabel = QLabel(self)
        brakePressTitleLabel.setText("BPS (kPa)")
        brakePressTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        brakePressTitleLabel.setFont(self.dashboardTitleFont)
        brakePressTitleLabel.setStyleSheet(
            "color : #FFF; background-color:" + self.labelBackgroundColor
        )

        self.brakePressLabel = QLabel(self)
        self.brakePressLabel.setText("300.3")
        self.brakePressLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.brakePressLabel.setFont(self.dashboardValueFont)
        self.brakePressLabel.setStyleSheet("QLabel { color : #FFF; }")

        layout.addWidget(brakePressTitleLabel, 0, 0)
        layout.addWidget(self.brakePressLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.brakePressGroupBox.setLayout(layout)

    def createBpsBar(self):
        self.bpsBar = QProgressBar(self)
        self.bpsBar.setFixedSize(50, 300)
        self.bpsBar.setMaximum(Rpm.MAX)
        self.bpsBar.setValue(0)
        self.bpsBar.setTextVisible(1)
        self.bpsBar.setOrientation(2)
        self.bpsBar.setStyleSheet(
            """
            QProgressBar
                {
                    background-color: #F00;
                    border-radius: 5px;
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
        # self.bpsBar.setFixedHeight(30)

    # def setBpsBar(self, bps: Rpm):
    #     self.bpsBar.setValue(int(bps))
    #     if bps.status == RpmStatus.LOW:
    #         color = "#0F0"
    #     elif bps.status == RpmStatus.MIDDLE:
    #         color = "#FF0"
    #     elif bps.status == RpmStatus.HIGH:
    #         color = "#F00"
    #     elif bps.status == RpmStatus.SHIFT:
    #         color = "#00F"
    #     self.bpsBar.setStyleSheet(
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

    # ---Fans state---
    def createFanStateGroupBox(self):
        self.fanStateGroupBox = QGroupBox()
        self.fanStateGroupBox.setFlat(True)
        # self.fanStateGroupBox.setFixedSize(150, 190)
        layout = QGridLayout()

        fanStateTitleLabel = QLabel(self)
        fanStateTitleLabel.setText("Fan")
        fanStateTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        fanStateTitleLabel.setFont(self.dashboardTitleFont)
        fanStateTitleLabel.setStyleSheet(
            "color : #FFF; background-color:" + self.labelBackgroundColor
        )

        self.fanStateLabel = QLabel(self)
        self.fanStateLabel.setText("ON")
        self.fanStateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fanStateLabel.setFont(self.dashboardValueFont)
        self.fanStateLabel.setStyleSheet("color : #FFF; background-color: #0F0")

        layout.addWidget(fanStateTitleLabel, 0, 0)
        layout.addWidget(self.fanStateLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.fanStateGroupBox.setLayout(layout)

    # ---Fans state---
    def createWaterPumpStateGroupBox(self):
        self.waterPumpStateGroupBox = QGroupBox()
        self.waterPumpStateGroupBox.setFlat(True)
        # self.waterPumpStateGroupBox.setFixedSize(150, 190)
        layout = QGridLayout()

        waterPumpStateTitleLabel = QLabel(self)
        waterPumpStateTitleLabel.setText("Water Pump")
        waterPumpStateTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        waterPumpStateTitleLabel.setFont(self.dashboardTitleFont)
        waterPumpStateTitleLabel.setStyleSheet(
            "color : #FFF; background-color:" + self.labelBackgroundColor
        )

        self.waterPumpStateLabel = QLabel(self)
        self.waterPumpStateLabel.setText("ON")
        self.waterPumpStateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.waterPumpStateLabel.setFont(self.dashboardValueFont)
        self.waterPumpStateLabel.setStyleSheet("color : #FFF; background-color: #0F0")

        layout.addWidget(waterPumpStateTitleLabel, 0, 0)
        layout.addWidget(self.waterPumpStateLabel, 1, 0)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.waterPumpStateGroupBox.setLayout(layout)

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
