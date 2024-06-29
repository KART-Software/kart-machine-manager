import time
from abc import ABCMeta, abstractmethod

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QGridLayout,
    QGroupBox,
)

from src.gui.self_defined_widgets import (
    GearLabel,
    IconValueBox,
    PedalBar,
    RpmLabel,
    RpmLightBar,
    TimeLabel,
    TitleValueBox,
)
from src.models.models import (
    DashMachineInfo,
    Message,
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

        self.createTopGroupBox()
        self.createLeftGroupBox()
        self.createCenterGroupBox()
        self.createRightGroupBox()
        self.createBottomGroupBox()

        mainLayout = QGridLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)
        mainLayout.addWidget(self.topGroupBox, 0, 0, 1, 3)
        mainLayout.addWidget(self.leftGroupBox, 1, 0)
        mainLayout.addWidget(self.centerGroupBox, 1, 1)
        mainLayout.addWidget(self.rightGroupBox, 1, 2)
        mainLayout.addWidget(self.bottomGroupBox, 2, 0, 1, 3)

    def updateDashboard(self, dashMachineInfo: DashMachineInfo, message: Message):
        self.topGroupBox.light_1.updateRpmLightColor(dashMachineInfo.rpm)
        self.topGroupBox.light_2.updateRpmLightColor(dashMachineInfo.rpm)
        self.topGroupBox.light_3.updateRpmLightColor(dashMachineInfo.rpm)
        self.topGroupBox.light_4.updateRpmLightColor(dashMachineInfo.rpm)
        self.topGroupBox.light_5.updateRpmLightColor(dashMachineInfo.rpm)
        self.topGroupBox.light_6.updateRpmLightColor(dashMachineInfo.rpm)
        self.topGroupBox.light_7.updateRpmLightColor(dashMachineInfo.rpm)
        self.topGroupBox.light_8.updateRpmLightColor(dashMachineInfo.rpm)
        self.topGroupBox.light_9.updateRpmLightColor(dashMachineInfo.rpm)
        self.topGroupBox.light_10.updateRpmLightColor(dashMachineInfo.rpm)
        self.topGroupBox.light_11.updateRpmLightColor(dashMachineInfo.rpm)
        self.topGroupBox.light_12.updateRpmLightColor(dashMachineInfo.rpm)

        self.rpmLabel.updateRpmLabel(dashMachineInfo.rpm)
        self.gearLabel.updateGearLabel(dashMachineInfo.gearVoltage.gearType)
        self.timeLabel.updateTime()

        self.waterTempTitleValueBox.updateValueLabel(dashMachineInfo.waterTemp)
        self.waterTempTitleValueBox.updateWaterTempWarning(dashMachineInfo.waterTemp)
        self.oilTempTitleValueBox.updateValueLabel(dashMachineInfo.oilTemp)
        self.oilTempTitleValueBox.updateOilTempWarning(dashMachineInfo.oilTemp)
        self.oilPressTitleValueBox.updateValueLabel(dashMachineInfo.oilPress.oilPress)
        self.oilPressTitleValueBox.updateOilPressWarning(dashMachineInfo.oilPress)

        self.messageIconValueBox.updateMessageLabel(message)

        # no mock data-----------
        self.fuelPressTitleValueBox.updateValueLabel(dashMachineInfo.fuelPress)
        self.fanSwitchStateTitleValueBox.valueLabel.setText(
            str(dashMachineInfo.fanEnabled)
        )
        self.brakeBiasTitleValueBox.updateValueLabel(dashMachineInfo.brakePress.front)
        self.tpsTitleValueBox.updateValueLabel(dashMachineInfo.throttlePosition)
        self.bpsFTitleValueBox.updateValueLabel(dashMachineInfo.brakePress.front)
        self.bpsRTitleValueBox.updateValueLabel(dashMachineInfo.brakePress.rear)
        self.tpsBar.updatePedalBar(dashMachineInfo.throttlePosition)
        self.bpsFBar.updatePedalBar(dashMachineInfo.brakePress.front)
        self.bpsRBar.updatePedalBar(dashMachineInfo.brakePress.rear)
        self.batteryIconValueBox.updateBatteryValueLabel(dashMachineInfo.batteryVoltage)

        # mock data for testing----------
        # testData = int(time.time() * 100) * 10 % 10000
        # self.fuelPressTitleValueBox.updateValueLabel(testData)
        # self.fanSwitchStateTitleValueBox.valueLabel.setText("OFF")
        # self.fanSwitchStateTitleValueBox.valueLabel.setStyleSheet(
        #     "color : #FFF; background-color: #F00"
        # )
        # self.brakeBiasTitleValueBox.updateValueLabel(testData)
        # self.tpsTitleValueBox.updateValueLabel(testData)
        # self.bpsFTitleValueBox.updateValueLabel(testData)
        # self.bpsRTitleValueBox.updateValueLabel(testData)
        # self.tpsBar.updatePedalBar(testData)
        # self.bpsFBar.updatePedalBar(testData)
        # self.bpsRBar.updatePedalBar(testData)
        # self.lapTimeIconValueBox.updateBatteryValueLabel(testData / 10)
        # self.lapTimeIconValueBox.valueLabel.setText("55.3s")
        # self.batteryIconValueBox.updateBatteryValueLabel(testData / 10)
        # -----------------------

    # ------------------------------Define Overall Layout Group Box---------------------
    def createTopGroupBox(self):
        self.topGroupBox = RpmLightBar()

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

        self.waterTempTitleValueBox = TitleValueBox("Water Temp")
        self.oilTempTitleValueBox = TitleValueBox("Oil Temp")
        self.oilPressTitleValueBox = TitleValueBox("Oil Press")
        self.fuelPressTitleValueBox = TitleValueBox("Fule Press")
        self.fanSwitchStateTitleValueBox = TitleValueBox("Fan Switch")
        self.brakeBiasTitleValueBox = TitleValueBox("Brk Bias(F%)")

        layout.addWidget(self.waterTempTitleValueBox, 0, 0)
        layout.addWidget(self.oilTempTitleValueBox, 1, 0)
        layout.addWidget(self.oilPressTitleValueBox, 1, 1)
        layout.addWidget(self.fuelPressTitleValueBox, 0, 1)
        layout.addWidget(self.fanSwitchStateTitleValueBox, 2, 0)
        layout.addWidget(self.brakeBiasTitleValueBox, 2, 1)
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

        self.rpmLabel = RpmLabel()
        self.gearLabel = GearLabel()
        self.timeLabel = TimeLabel()

        # self.kartLogoIcon = QPixmap("src\gui\icons\kart_logo.png")
        # self.kartLogoIconLable = QLabel(self)
        # self.kartLogoIconLable.setPixmap(self.kartLogoIcon)
        # self.kartLogoIconLable.setStyleSheet("background-color: #000")
        # self.kartLogoIconLable.setFixedSize(196, 50)
        # self.kartLogoIconLable.setAlignment(QtCore.Qt.AlignCenter)
        # self.kartLogoIconLable.setScaledContents(True)
        # logo表示なし#

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

        self.tpsTitleValueBox = TitleValueBox("TPS")
        self.tpsTitleValueBox.valueLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.bpsFTitleValueBox = TitleValueBox("BPS F")
        self.bpsRTitleValueBox = TitleValueBox("BPS R")
        self.tpsBar = PedalBar(30, 340, "#0F0", 100)
        self.bpsFBar = PedalBar(30, 150, "#F00", 400)
        self.bpsRBar = PedalBar(30, 150, "#F00", 400)
        self.bpsRBar.setInvertedAppearance(True)

        layout.addWidget(self.tpsTitleValueBox, 0, 0, 2, 1)
        layout.addWidget(self.tpsBar, 0, 1, 2, 1)
        layout.addWidget(self.bpsFBar, 0, 2)
        layout.addWidget(self.bpsFTitleValueBox, 0, 3)
        layout.addWidget(self.bpsRBar, 1, 2)
        layout.addWidget(self.bpsRTitleValueBox, 1, 3)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

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

        self.batteryIconValueBox = IconValueBox("src\gui\icons\BatteryIcon.png")
        self.lapTimeIconValueBox = IconValueBox("src\gui\icons\LaptimeIcon.png")
        self.messageIconValueBox = IconValueBox("src\gui\icons\MeesageIcon.png")
        self.messageIconValueBox.valueLabel.setAlignment(QtCore.Qt.AlignVCenter)
        self.messageIconValueBox.layout.setColumnStretch(0, 1)
        self.messageIconValueBox.layout.setColumnStretch(1, 6)

        layout.addWidget(self.messageIconValueBox, 0, 0)
        layout.addWidget(self.lapTimeIconValueBox, 0, 1)
        layout.addWidget(self.batteryIconValueBox, 0, 2)
        layout.setColumnStretch(0, 4)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.bottomGroupBox.setLayout(layout)
