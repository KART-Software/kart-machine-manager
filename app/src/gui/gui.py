import sys
import os
from PyQt5.QtCore import QObject, QVariant, pyqtSignal, pyqtProperty, QUrl, QTimer, QDateTime, pyqtSlot
from PyQt5.QtQml import QQmlComponent, QJSValue
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from src.machine.machine import Machine


class Gui:
    def __init__(self):
        self.app = QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()
        self.guiMachine = GuiMachine()
        self.context = self.engine.rootContext()

        self.engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))
        if not self.engine.rootObjects():
            sys.exit(-1)

    def setProperty(self, machine: Machine):
        self.context.setContextProperty('machine', QVariant(machine.machineInfo))



class GuiMachine(QObject):

    def __init__(self):
        QObject.__init__(self)
        
"""     signal = pyqtSignal(QJSValue)
    

    @pyqtSlot(QJSValue)
    def onPySignal(self, machine : Machine):
        self.signal.emit(machine)

        obj = machine.toVariant()
        print('onPySignal', obj)
        print(dir(obj))

    def connect(self, machine: Machine):
        self.signal.connect(self.onPySignal)
        self.signal.emit(machine) """