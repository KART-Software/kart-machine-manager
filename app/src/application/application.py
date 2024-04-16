import sys

from PyQt5.QtWidgets import QApplication

from src.machine.machine import Machine
from src.machine.can_master import CanMaster
from ..gui.gui import MainWindow, WindowListener


class Application(WindowListener):

    machine: Machine

    def __init__(self):
        super().__init__()
        self.machine = Machine()

    def initialize(self) -> None:
        self.machine.initialise()
        self.app = QApplication(sys.argv)
        self.window = MainWindow(self)
        self.window.showFullScreen()
        # self.window.show()
        sys.exit(self.app.exec_())

    def onUpdate(self) -> None:
        self.machine.updateMachineInfo()
        self.window.updateDashboard(self.machine.machineInfo)
        return super().onUpdate()
