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
    LapTimeLabel,
    PedalBar,
    RpmLabel,
    RpmLightBar,
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

        self.createAllWidgets()
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
        mainLayout.addWidget(self.leftGroupBox, 1, 0, 1, 1)
        mainLayout.addWidget(self.centerGroupBox, 1, 1, 1, 1)
        mainLayout.addWidget(self.rightGroupBox, 1, 2, 1, 1)
        mainLayout.addWidget(self.bottomGroupBox, 2, 0, 1, 3)

        mainLayout.setColumnStretch(0, 3)
        mainLayout.setColumnStretch(1, 2)
        mainLayout.setColumnStretch(2, 3)
        mainLayout.setRowStretch(0, 1)
        mainLayout.setRowStretch(1, 6)
        mainLayout.setRowStretch(2, 1)

    def updateDashboard(self, dashMachineInfo: DashMachineInfo, message: Message):
        self.rpmLightBar.updateRpmBar(dashMachineInfo.rpm)
        self.rpmLabel.updateRpmLabel(dashMachineInfo.rpm)
        self.gearLabel.updateGearLabel(dashMachineInfo.gearVoltage.gearType)
        self.waterTempTitleValueBox.updateValueLabel(dashMachineInfo.waterTemp)
        self.waterTempTitleValueBox.updateWaterTempWarning(dashMachineInfo.waterTemp)
        self.oilTempTitleValueBox.updateValueLabel(dashMachineInfo.oilTemp)
        self.oilTempTitleValueBox.updateOilTempWarning(dashMachineInfo.oilTemp)
        self.oilPressTitleValueBox.updateValueLabel(dashMachineInfo.oilPress.oilPress)
        self.oilPressTitleValueBox.updateOilPressWarning(dashMachineInfo.oilPress)
        self.messageIconValueBox.updateMessageLabel(message)
        self.lapTimeLabel.updateLapTimeLabel(message)
        self.timeIconValueBox.updateTime()
        # no mock data-----------
        self.fuelPressTitleValueBox.updateValueLabel(dashMachineInfo.fuelPress)
        self.fanSwitchStateTitleValueBox.updateBoolValueLabel(
            dashMachineInfo.fanEnabled
        )
        self.fanSwitchStateTitleValueBox.updateFanWarning(dashMachineInfo.fanEnabled)
        self.brakeBiasTitleValueBox.updateValueLabel(dashMachineInfo.brakePress.bias)
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

    def createAllWidgets(self):
        self.rpmLabel = RpmLabel()
        self.gearLabel = GearLabel()
        self.lapTimeLabel = LapTimeLabel()

        self.waterTempTitleValueBox = TitleValueBox("Water Temp")
        self.oilTempTitleValueBox = TitleValueBox("Oil Temp")
        self.oilPressTitleValueBox = TitleValueBox("Oil Press")
        self.fuelPressTitleValueBox = TitleValueBox("Fuel Press")
        self.fanSwitchStateTitleValueBox = TitleValueBox("Fan Switch")
        self.brakeBiasTitleValueBox = TitleValueBox("Brk Bias(F%)")

        self.tpsTitleValueBox = TitleValueBox("TPS")
        self.tpsTitleValueBox.valueLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.bpsFTitleValueBox = TitleValueBox("BPS F")
        self.bpsRTitleValueBox = TitleValueBox("BPS R")
        self.tpsBar = PedalBar("#0F0", 100)
        self.bpsFBar = PedalBar("#F00", 600)
        self.bpsRBar = PedalBar("#F00", 600)
        self.bpsRBar.setInvertedAppearance(True)

        self.batteryIconValueBox = IconValueBox("src/gui/icons/BatteryIcon.png")
        self.lapTimeIconValueBox = IconValueBox("src/gui/icons/LaptimeIcon.png")
        self.timeIconValueBox = IconValueBox("src/gui/icons/LaptimeIcon.png")
        self.messageIconValueBox = IconValueBox("src/gui/icons/MeesageIcon.png")
        self.messageIconValueBox.valueLabel.setAlignment(QtCore.Qt.AlignVCenter)
        self.messageIconValueBox.layout.setColumnStretch(0, 1)
        self.messageIconValueBox.layout.setColumnStretch(1, 6)

    # ------------------------------Define Overall Layout Group Box---------------------
    def createTopGroupBox(self):
        self.topGroupBox = QGroupBox()
        self.topGroupBox.setFlat(True)
        # self.topGroupBox.setObjectName("TopBox")
        # self.topGroupBox.setStyleSheet("QGroupBox#TopBox { border: 1px solid white;}")

        layout = QGridLayout()
        self.rpmLightBar = RpmLightBar()
        layout.addWidget(self.rpmLightBar, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.topGroupBox.setLayout(layout)

    def createLeftGroupBox(self):
        self.leftGroupBox = QGroupBox()
        self.leftGroupBox.setFlat(True)
        # self.leftGroupBox.setStyleSheet("border:0;")
        self.leftGroupBox.setObjectName("LeftBox")
        self.leftGroupBox.setStyleSheet("QGroupBox#LeftBox { border: 2px solid white;}")
        # self.leftGroupBox.setGeometry(1, 81, 200, 320)
        # self.leftGroupBox.setFixedSize(300, 380)

        layout = QGridLayout()
        # layout = QVBoxLayout()

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
        self.centerGroupBox.setStyleSheet("border: 2px solid white;")
        # self.centerGroupBox.setStyleSheet("QGroupBox { border: 2px solid white;}")
        # self.centerGroupBox.setGeometry(301, 81, 200, 320)
        # self.centerGroupBox.setFixedSize(200, 380)

        layout = QGridLayout()

        layout.addWidget(self.rpmLabel, 0, 0, 1, 2)
        layout.addWidget(self.gearLabel, 1, 0, 1, 2)
        layout.addWidget(self.lapTimeLabel, 2, 0, 1, 2)

        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 10)
        layout.setRowStretch(2, 3)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.centerGroupBox.setLayout(layout)

    def createRightGroupBox(self):
        self.rightGroupBox = QGroupBox()
        self.rightGroupBox.setFlat(True)
        # self.rightGroupBox.setStyleSheet("border:0;")
        self.rightGroupBox.setObjectName("RightBox")
        self.rightGroupBox.setStyleSheet(
            "QGroupBox#RightBox { border: 2px solid white;}"
        )
        # self.rightGroupBox.setGeometry(501, 81, 200, 320)
        # self.rightGroupBox.setFixedSize(300, 380)

        layout = QGridLayout()

        layout.addWidget(self.tpsTitleValueBox, 0, 0, 2, 1)
        layout.addWidget(self.tpsBar, 0, 1, 2, 1)
        layout.addWidget(self.bpsFBar, 0, 2)
        layout.addWidget(self.bpsFTitleValueBox, 0, 3)
        layout.addWidget(self.bpsRBar, 1, 2)
        layout.addWidget(self.bpsRTitleValueBox, 1, 3)

        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 2)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.rightGroupBox.setLayout(layout)

    def createBottomGroupBox(self):
        self.bottomGroupBox = QGroupBox()
        self.bottomGroupBox.setFlat(True)
        self.bottomGroupBox.setStyleSheet("border: 0px;")
        # self.bottomGroupBox.setObjectName("BottomBox")
        # self.bottomGroupBox.setStyleSheet(
        #     "QGroupBox#BottomBox { border: 0px solid white;}"
        # )
        # self.bottomGroupBox.setGeometry(1, 401, 800, 80)
        # self.bottomGroupBox.setFixedSize(800, 50)

        layout = QGridLayout()

        layout.addWidget(self.messageIconValueBox, 0, 0)
        layout.addWidget(self.batteryIconValueBox, 0, 1)
        layout.addWidget(self.timeIconValueBox, 0, 2)

        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.bottomGroupBox.setLayout(layout)
