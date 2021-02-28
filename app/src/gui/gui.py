from abc import ABCMeta, abstractmethod
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QProgressBar,
)
from src.machine.can_master import Rpm, RpmStatus

from src.machine.machine import MachineInfo


class WindowListener(metaclass=ABCMeta):
    @abstractmethod
    def onUpdate(self) -> None:
        pass


class MainWindow(QDialog):
    def __init__(self, listener: WindowListener):
        super(MainWindow, self).__init__(None)

        self.listener = listener

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.listener.onUpdate)
        self.timer.start(100)

        self.originalPalette = QApplication.palette()
        self.originalPalette.setColor(self.backgroundRole(), QColor("#000"))
        self.originalPalette.setColor(self.foregroundRole(), QColor("#FFF"))

        self.dashboardTitleFont = QFont("Arial", 18)
        self.dashboardValueFont = QFont("Arial", 36)

        self.createRpmBar()
        self.createCenterGroupBox()
        self.createLeftGroupBox()
        self.createRightGroupBox()

        mainLayout = QGridLayout()

        mainLayout.setContentsMargins(1, 1, 1, 1)
        mainLayout.setSpacing(4)

        self.setLayout(mainLayout)
        mainLayout.addWidget(self.rpmBar, 0, 0, 1, 3)
        mainLayout.addWidget(self.centerGroupBox, 1, 1)
        mainLayout.addWidget(self.leftGroupBox, 1, 0)
        mainLayout.addWidget(self.rightGroupBox, 1, 2)

    def updateDashboard(self, machineInfo: MachineInfo):
        self.setRpmBar(machineInfo.rpm)
        self.setRpmLabel(machineInfo.rpm)

    def createRpmBar(self):
        self.rpmBar = QProgressBar(self)
        self.rpmBar.setMaximum(Rpm.MAX)
        self.rpmBar.setValue(0)
        self.rpmBar.setTextVisible(False)
        self.rpmBar.setStyleSheet(
            """
            QProgressBar
                {
                    border-radius: 5px;
                    height: 32px;
                    padding: 0px;
                }
            QProgressBar::chunk
                {
                    background-color: #0F0;
                    width: 7px;
                    margin: 1px;
                }
        """
        )

    def setRpmBar(self, rpm: Rpm):
        self.rpmBar.setValue(int(rpm))
        if rpm.status == RpmStatus.LOW:
            color = "#3F3"
        elif rpm.status == RpmStatus.MIDDLE:
            color = "#F33"
        elif rpm.status == RpmStatus.HIGH:
            color = "#24F"
        self.rpmBar.setStyleSheet(
            """
            QProgressBar
                {
                    border-radius: 5px;
                    height: 32px;
                    padding: 0px;
                }
            QProgressBar::chunk
                {
                    background-color: %s;
                    width: 7px;
                    margin: 1px;
                }
        """
            % (color)
        )

    def createCenterGroupBox(self):
        self.centerGroupBox = QGroupBox()
        self.centerGroupBox.setFlat(True)
        self.centerGroupBox.setStyleSheet("border:0;")

        layout = QGridLayout()

        self.rpmLabel = QLabel(self)
        self.rpmLabel.setText("3454")
        self.rpmLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rpmLabel.setFont(QFont("Arial", 36))

        gearLabel = QLabel(self)
        gearLabel.setText("2")
        gearLabel.setAlignment(QtCore.Qt.AlignCenter)
        gearLabel.setFont(QFont("Arial", 120))

        speedLabel = QLabel(self)
        speedLabel.setText("16")
        speedLabel.setAlignment(QtCore.Qt.AlignCenter)
        speedLabel.setFont(QFont("Arial", 36))

        layout.addWidget(self.rpmLabel, 0, 0)
        layout.addWidget(gearLabel, 1, 0)
        layout.addWidget(speedLabel, 2, 0)
        layout.setRowStretch(1, 2)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        self.centerGroupBox.setLayout(layout)

    def setRpmLabel(self, rpm: Rpm):
        self.rpmLabel.setText(str(rpm))

    def createWaterTempGroupBox(self):

        self.waterTempGroupBox = QGroupBox()
        self.waterTempGroupBox.setFlat(True)
        self.waterTempGroupBox.setStyleSheet("border:0;")

        layout = QGridLayout()

        waterTempTitleLabel = QLabel(self)
        waterTempTitleLabel.setText("Water Temp")
        waterTempTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        waterTempTitleLabel.setFont(self.dashboardTitleFont)

        self.waterTempLabel = QLabel(self)
        self.waterTempLabel.setText("114")
        self.waterTempLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.waterTempLabel.setFont(self.dashboardValueFont)

        layout.addWidget(waterTempTitleLabel, 0, 0)
        layout.addWidget(self.waterTempLabel, 1, 0)
        layout.setRowStretch(1, 3)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        self.waterTempGroupBox.setLayout(layout)
        self.waterTempGroupBox.setStyleSheet("background-color: red;")

    def createOilTempGroupBox(self):

        self.oilTempGroupBox = QGroupBox()
        self.oilTempGroupBox.setFlat(True)
        self.oilTempGroupBox.setStyleSheet("border:0;")

        layout = QGridLayout()

        oilTempTitleLabel = QLabel(self)
        oilTempTitleLabel.setText("Oil Temp")
        oilTempTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        oilTempTitleLabel.setFont(self.dashboardTitleFont)

        self.oilTempLabel = QLabel(self)
        self.oilTempLabel.setText("114")
        self.oilTempLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.oilTempLabel.setFont(self.dashboardValueFont)

        layout.addWidget(oilTempTitleLabel, 0, 0)
        layout.addWidget(self.oilTempLabel, 1, 0)
        layout.setRowStretch(1, 3)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        self.oilTempGroupBox.setLayout(layout)

    def createOilPressGroupBox(self):

        self.oilPressGroupBox = QGroupBox()
        self.oilPressGroupBox.setFlat(True)
        self.oilPressGroupBox.setStyleSheet("border:0;")

        layout = QGridLayout()

        oilPressTitleLabel = QLabel(self)
        oilPressTitleLabel.setText("Oil Press")
        oilPressTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        oilPressTitleLabel.setFont(self.dashboardTitleFont)

        self.oilPressLabel = QLabel(self)
        self.oilPressLabel.setText("114")
        self.oilPressLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.oilPressLabel.setFont(self.dashboardValueFont)

        layout.addWidget(oilPressTitleLabel, 0, 0)
        layout.addWidget(self.oilPressLabel, 1, 0)
        layout.setRowStretch(1, 3)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        self.oilPressGroupBox.setLayout(layout)

    def createLeftGroupBox(self):

        self.leftGroupBox = QGroupBox()
        self.leftGroupBox.setFlat(True)
        self.leftGroupBox.setStyleSheet("border:0;")

        layout = QGridLayout()

        self.createWaterTempGroupBox()
        self.createOilTempGroupBox()
        self.createOilPressGroupBox()

        layout.addWidget(self.waterTempGroupBox, 0, 0)
        layout.addWidget(self.oilTempGroupBox, 1, 0)
        layout.addWidget(self.oilPressGroupBox, 2, 0)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.leftGroupBox.setLayout(layout)

    def createFuelRemainGroupBox(self):

        self.fuelRemainGroupBox = QGroupBox()
        self.fuelRemainGroupBox.setFlat(True)
        self.fuelRemainGroupBox.setStyleSheet("border:0;")

        layout = QGridLayout()

        fuelRemainTitleLabel = QLabel(self)
        fuelRemainTitleLabel.setText("Fuel Remain")
        fuelRemainTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        fuelRemainTitleLabel.setFont(self.dashboardTitleFont)

        self.fuelRemainLabel = QLabel(self)
        self.fuelRemainLabel.setText("30")
        self.fuelRemainLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fuelRemainLabel.setFont(self.dashboardValueFont)

        layout.addWidget(fuelRemainTitleLabel, 0, 0)
        layout.addWidget(self.fuelRemainLabel, 1, 0)
        layout.setRowStretch(1, 3)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        self.fuelRemainGroupBox.setLayout(layout)

    def createBatteryGroupBox(self):

        self.batteryGroupBox = QGroupBox()
        self.batteryGroupBox.setFlat(True)
        self.batteryGroupBox.setStyleSheet("border:0;")

        layout = QGridLayout()

        batteryTitleLabel = QLabel(self)
        batteryTitleLabel.setText("Battery")
        batteryTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        batteryTitleLabel.setFont(self.dashboardTitleFont)

        self.batteryLabel = QLabel(self)
        self.batteryLabel.setText("114")
        self.batteryLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.batteryLabel.setFont(self.dashboardValueFont)

        layout.addWidget(batteryTitleLabel, 0, 0)
        layout.addWidget(self.batteryLabel, 1, 0)
        layout.setRowStretch(1, 3)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        self.batteryGroupBox.setLayout(layout)

    def createLapTimeGroupBox(self):

        self.lapTimeGroupBox = QGroupBox()
        self.lapTimeGroupBox.setFlat(True)
        self.lapTimeGroupBox.setStyleSheet("border:0;")

        layout = QGridLayout()

        lapTimeTitleLabel = QLabel(self)
        lapTimeTitleLabel.setText("Oil Press")
        lapTimeTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        lapTimeTitleLabel.setFont(self.dashboardTitleFont)

        self.lapTimeLabel = QLabel(self)
        self.lapTimeLabel.setText("114")
        self.lapTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.lapTimeLabel.setFont(self.dashboardValueFont)

        layout.addWidget(lapTimeTitleLabel, 0, 0)
        layout.addWidget(self.lapTimeLabel, 1, 0)
        layout.setRowStretch(1, 3)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        self.lapTimeGroupBox.setLayout(layout)

    def createRightGroupBox(self):

        self.rightGroupBox = QGroupBox()
        self.rightGroupBox.setFlat(True)
        self.rightGroupBox.setStyleSheet("border:0;")

        layout = QGridLayout()

        self.createFuelRemainGroupBox()
        self.createBatteryGroupBox()
        self.createLapTimeGroupBox()

        layout.addWidget(self.fuelRemainGroupBox, 0, 0)
        layout.addWidget(self.batteryGroupBox, 1, 0)
        layout.addWidget(self.lapTimeGroupBox, 2, 0)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.rightGroupBox.setLayout(layout)
