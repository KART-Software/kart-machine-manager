import sys
import os
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, QUrl, QTimer, QDateTime
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine


class Gui:
    def __init__(self):
        self.app = QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()
        self.engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))
        if not self.engine.rootObjects():
            sys.exit(-1)
