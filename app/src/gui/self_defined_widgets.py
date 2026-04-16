import datetime

from PyQt6 import QtCore
from PyQt6.QtGui import QColor, QFont, QPalette, QPixmap
from PyQt6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QLabel,
    QProgressBar,
    QSizePolicy,
    QWidget,
)

from src.models.models import (
    BatteryVoltage,
    GearType,
    Message,
    OilPress,
    OilPressStatus,
    OilTemp,
    OilTempStatus,
    Rpm,
    WaterTemp,
    WaterTempStatus,
)


class QCustomLabel(QLabel):
    def __init__(self):
        super(QCustomLabel, self).__init__()
        self._font = QFont()
        # self.setFont(self._font)
        self.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self._fontScale = 1.0

    def setFontFamily(self, face):
        self._font.setFamily(face)

    def setFontScale(self, scale):
        self._fontScale = scale

    def resizeEvent(self, evt):
        width = self.size().width() / 2
        height = self.size().height()
        baseSize = 0
        if width > height:
            baseSize = height
        else:
            baseSize = width

        self._font.setPixelSize(int(baseSize * self._fontScale))
        self.setFont(self._font)


class TitleValueBox(QGroupBox):
    def __init__(self, titleLabel):
        super(TitleValueBox, self).__init__(None)
        self.setFlat(True)
        self.layout = QGridLayout()
        self.setObjectName("TitleValueBox")
        self.setStyleSheet(
            "QGroupBox#TitleValueBox { border: 1px solid #333; border-radius: 3px;}"
        )
        self.TitleFont = "Arial"
        self.titleColor = "#FD6"
        self.valueFont = "Arial"
        self.valueColor = "#FFF"
        self.titleBackgroundColor = "#000"

        self.titleLabel = QCustomLabel()
        self.titleLabel.setText(titleLabel)
        # self.titleLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.titleLabel.setFontFamily(self.TitleFont)
        self.titleLabel.setFontScale(0.55)
        self.titleLabel.setStyleSheet(
            "color :"
            + self.titleColor
            + "; background-color:"
            + self.titleBackgroundColor
            + ";font-weight: bold"
        )

        self.valueLabel = QCustomLabel()
        self.valueLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.valueLabel.setFontFamily(self.valueFont)
        self.valueLabel.setFontScale(0.75)
        self.valueLabel.setStyleSheet(
            "font-weight: bold; color :" + self.valueColor + ";"
        )
        # self.setStyleSheet("color : #FFF; background-color: #000;")

        self.layout.addWidget(self.titleLabel, 0, 0)
        self.layout.addWidget(self.valueLabel, 1, 0)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 2)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.setLayout(self.layout)

        # Pre-cached warning styles & dirty check state
        self._warningStyles: dict[str, str] = {}
        self._lastWarningStyle: str | None = None

    def _getWarningStyle(self, color: str) -> str:
        style = self._warningStyles.get(color)
        if style is None:
            style = (
                "font-weight: bold; border-radius: 5px;"
                f" color: #FFF; background-color: {color};"
            )
            self._warningStyles[color] = style
        return style

    def _applyWarningStyle(self, color: str) -> None:
        style = self._getWarningStyle(color)
        if style != self._lastWarningStyle:
            self._lastWarningStyle = style
            self.valueLabel.setStyleSheet(style)

    def updateValueLabel(self, value):
        self.valueLabel.setText(str(value))

    def updateBoolValueLabel(self, value: bool):
        if value:
            self.valueLabel.setText("ON")
        else:
            self.valueLabel.setText("OFF")

    # --------------- update background warning color  ----------
    def updateWaterTempWarning(self, waterTemp: WaterTemp):
        if waterTemp.status == WaterTempStatus.LOW:
            color = "#000"
        elif waterTemp.status == WaterTempStatus.MIDDLE:
            color = "#FB0"
        elif waterTemp.status == WaterTempStatus.HIGH:
            color = "#F00"
        self._applyWarningStyle(color)

    def updateOilTempWarning(self, oilTemp: OilTemp):
        if oilTemp.status == OilTempStatus.LOW:
            color = "#000"
        elif oilTemp.status == OilTempStatus.MIDDLE:
            color = "#FB0"
        elif oilTemp.status == OilTempStatus.HIGH:
            color = "#F00"
        self._applyWarningStyle(color)

    def updateOilPressWarning(self, oilPress: OilPress):
        # self.valueLabel.setText(str(round(oilPress, 2)))
        if oilPress.status == OilPressStatus.LOW:
            color = "#F00"
        elif oilPress.status == OilPressStatus.MIDDLE:
            color = "#FB0"
        elif oilPress.status == OilPressStatus.HIGH:
            color = "#000"
        self._applyWarningStyle(color)

    def updateFanWarning(self, fanEnable: bool):
        if fanEnable:
            color = "#000"
        else:
            color = "#F00"
        self._applyWarningStyle(color)


class IconValueBox(QGroupBox):
    def __init__(self, iconPath):
        super(IconValueBox, self).__init__(None)
        self.setFlat(True)

        self.valueFont = QFont("Arial", 18)
        self.valueColor = "#FFF"
        self.layout = QGridLayout()

        self.iconLabel = QLabel(self)
        self.iconLabel.setPixmap(QPixmap(iconPath))
        self.iconLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.iconLabel.setScaledContents(True)

        # self.valueLabel = QLabel(self)
        self.valueLabel = QCustomLabel()
        self.valueLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.valueLabel.setFontScale(0.6)
        self.valueLabel.setFontFamily("Arial")
        self.valueLabel.setStyleSheet(
            "QLabel { font-weight: bold; color : " + self.valueColor + "; }"
        )

        # self.layout.addWidget(batteryTitleLabel, 0, 0)
        self.layout.addWidget(self.iconLabel, 0, 0)
        self.layout.addWidget(self.valueLabel, 0, 1)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 3)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.setLayout(self.layout)

    def updateBatteryValueLabel(self, batteryVoltage: BatteryVoltage):
        # value = "12.3 V"
        self.valueLabel.setText(str(round(batteryVoltage, 2)) + " V")
        # self.valueLabel.setText(str(round(battery, 2)))

    # def updateBatteryWarning(self. battery: Battery)
    #     self.valueLabel.setText(str(round(battery, 2)))

    #     if battery.status == BatteryStatus.LOW:
    #         color = "#F00"
    #     elif battery.status == BatteryStatus.HIGH:
    #         color = "#000"

    #     self.batteryGroupBox.setStyleSheet("background-color: " + color + ";")

    # def updateLapTimeValueLabel(self, lapTime: LapTime):
    #     minute = lapTime.seconds // 60
    #     second = lapTime.seconds % 60
    #     aftersecond = lapTime.microseconds // 10000
    #     self.lapTimeLabel.setText(
    #         str(minute) + "." + str(second) + "." + str(aftersecond)
    #     )

    def updateMessageLabel(self, message: Message):
        self.valueLabel.setText(message.text)

    def updateTime(self):
        dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        text = dt_now.strftime("%H:%M")
        if text != self.valueLabel.text():
            self.valueLabel.setText(text)


class PedalBar(QProgressBar):
    def __init__(self, barColor, maxValue):
        super(PedalBar, self).__init__(None)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        # self.adjustSize()
        # self.setMaximum(Rpm.MAX)
        self.setMaximum(maxValue)
        # self.setValue(40)
        self.setTextVisible(False)
        self.setOrientation(QtCore.Qt.Orientation.Vertical)
        # self.setStyleSheet(
        #     """
        #     QProgressBar
        #         {
        #             border: 2px solid;
        #             border-color: #AAA;
        #             border-radius: 5px;
        #             background-color: #333;
        #         }
        #     """
        # )
        self.setStyleSheet(
            """
            QProgressBar
                {
                    border: 2px solid;
                    border-color: #AAA;
                    border-radius: 5px;
                    background-color: #333;
                }
            QProgressBar::chunk
                {
                    background-color: %s;
                    height: 1px;
                }
            """
            % (barColor)
        )

    def updatePedalBar(self, value):
        self.setValue(int(value))


class RpmLightBar(QGroupBox):
    def __init__(self):
        super(RpmLightBar, self).__init__(None)
        self.setFlat(True)
        self.setObjectName("RpmLightBar")
        self.setStyleSheet("QGroupBox#RpmLightBar { border: 0; }")

        self.layout = QGridLayout()

        # # shift point 8500
        # self.lightRpm_1 = 1000
        # self.lightRpm_2 = 2000
        # self.lightRpm_3 = 3000
        # self.lightRpm_4 = 4000
        # self.lightRpm_5 = 4500
        # self.lightRpm_6 = 5000
        # self.lightRpm_7 = 5500
        # self.lightRpm_8 = 6000
        # self.lightRpm_9 = 6500
        # self.lightRpm_10 = 7000
        # self.lightRpm_11 = 7500
        # self.lightRpm_12 = 8000

        # shift point 9000
        self.lightRpm_1 = 1000
        self.lightRpm_2 = 2000
        self.lightRpm_3 = 3000
        self.lightRpm_4 = 4000
        self.lightRpm_5 = 5000
        self.lightRpm_6 = 5500
        self.lightRpm_7 = 6000
        self.lightRpm_8 = 6500
        self.lightRpm_9 = 7000
        self.lightRpm_10 = 7500
        self.lightRpm_11 = 8000
        self.lightRpm_12 = 8500

        self.greenLightColor = "#0F0"
        self.yellowLightColor = "#FF0"
        self.redLightColor = "#F00"
        self.blueLightColor = "#8FF"

        self.light_1 = RpmLight(self.lightRpm_1, self.greenLightColor)
        self.light_2 = RpmLight(self.lightRpm_2, self.greenLightColor)
        self.light_3 = RpmLight(self.lightRpm_3, self.greenLightColor)
        self.light_4 = RpmLight(self.lightRpm_4, self.greenLightColor)
        self.light_5 = RpmLight(self.lightRpm_5, self.yellowLightColor)
        self.light_6 = RpmLight(self.lightRpm_6, self.yellowLightColor)
        self.light_7 = RpmLight(self.lightRpm_7, self.yellowLightColor)
        self.light_8 = RpmLight(self.lightRpm_8, self.yellowLightColor)
        self.light_9 = RpmLight(self.lightRpm_9, self.redLightColor)
        self.light_10 = RpmLight(self.lightRpm_10, self.redLightColor)
        self.light_11 = RpmLight(self.lightRpm_11, self.blueLightColor)
        self.light_12 = RpmLight(self.lightRpm_12, self.blueLightColor)

        self.layout.addWidget(self.light_1, 0, 0)
        self.layout.addWidget(self.light_2, 0, 1)
        self.layout.addWidget(self.light_3, 0, 2)
        self.layout.addWidget(self.light_4, 0, 3)
        self.layout.addWidget(self.light_5, 0, 4)
        self.layout.addWidget(self.light_6, 0, 5)
        self.layout.addWidget(self.light_7, 0, 6)
        self.layout.addWidget(self.light_8, 0, 7)
        self.layout.addWidget(self.light_9, 0, 8)
        self.layout.addWidget(self.light_10, 0, 9)
        self.layout.addWidget(self.light_11, 0, 10)
        self.layout.addWidget(self.light_12, 0, 11)

        # self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.setSpacing(0)

        self.setLayout(self.layout)

    def updateRpmBar(self, rpm: Rpm):
        self.light_1.updateRpmLightColor(rpm)
        self.light_2.updateRpmLightColor(rpm)
        self.light_3.updateRpmLightColor(rpm)
        self.light_4.updateRpmLightColor(rpm)
        self.light_5.updateRpmLightColor(rpm)
        self.light_6.updateRpmLightColor(rpm)
        self.light_7.updateRpmLightColor(rpm)
        self.light_8.updateRpmLightColor(rpm)
        self.light_9.updateRpmLightColor(rpm)
        self.light_10.updateRpmLightColor(rpm)
        self.light_11.updateRpmLightColor(rpm)
        self.light_12.updateRpmLightColor(rpm)


class RpmLight(QWidget):
    def __init__(self, onRpm, onColor):
        super().__init__()
        self.setAutoFillBackground(True)

        self.onRpm = onRpm
        self.shiftRpm = 8700

        self._offColor = QColor("#333")
        self._onColor = QColor(onColor)
        self._shiftColor = QColor("#8FF")
        self._lastColor: QColor | None = None

        # Set initial off color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, self._offColor)
        self.setPalette(palette)

    def updateRpmLightColor(self, rpm: Rpm):
        if rpm < self.onRpm:
            color = self._offColor
        elif rpm < self.shiftRpm:
            color = self._onColor
        else:
            color = self._shiftColor
        if color != self._lastColor:
            self._lastColor = color
            palette = self.palette()
            palette.setColor(QPalette.ColorRole.Window, color)
            self.setPalette(palette)


class GearLabel(QCustomLabel):
    def __init__(self):
        super(GearLabel, self).__init__()
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFontFamily("Arial")
        self.setFontScale(2.5)
        self.setStyleSheet("font-weight: bold; color: #FFF; background-color: #000")
        self._lastGearType: GearType | None = None
        self._neutralStyle = "font-weight: bold; color: #FD6; background-color: #000"
        self._normalStyle = "font-weight: bold; color: #FFF; background-color: #000"
        self._lastStyle: str | None = None

    def updateGearLabel(self, gearType: GearType):
        if gearType == self._lastGearType:
            return
        self._lastGearType = gearType
        if int(gearType) == GearType.NEUTRAL:
            self.setText("N")
            style = self._neutralStyle
        else:
            self.setText(str(int(gearType)))
            style = self._normalStyle
        if style != self._lastStyle:
            self._lastStyle = style
            self.setStyleSheet(style)


class RpmLabel(QCustomLabel):
    def __init__(self):
        super(RpmLabel, self).__init__()
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFontFamily("Arial")
        self.setFontScale(0.8)
        self.setStyleSheet("font-weight: bold; color : #FFF; background-color: #000")

    def updateRpmLabel(self, rpm: Rpm):
        self.setText(str(rpm))


class LapTimeLabel(QCustomLabel):
    def __init__(self):
        super(LapTimeLabel, self).__init__()

        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFontFamily("Times New Roman")
        self.setFontScale(0.8)
        self.setStyleSheet("color : #B6F; background-color: #000")

    def updateLapTimeLabel(self, message: Message):
        self.setText(str(round(message.laptime, 2)) + " s")
