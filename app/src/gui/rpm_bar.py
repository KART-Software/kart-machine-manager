from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)


class RpmBar(QWidget):
    def createRpmLightBox1(self):
        self.rpmLightBox1 = QGroupBox()
        self.rpmLightBox1.setFlat(True)
        self.rpmLightBox1.setStyleSheet("border:0;")
        self.rpmLightBox1.setFixedSize(50, 50)
        self.rpmLightBox1.setStyleSheet("background-color: " + "#AF0" + ";")
