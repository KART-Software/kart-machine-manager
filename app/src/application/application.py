import sys
from time import sleep

from PyQt5.QtWidgets import QApplication

from src.machine.machine import Machine
from src.machine.can_master import CanMaster
from ..gui.gui import MainWindow, WindowListener


class Application(WindowListener):

    machine: Machine
    canMaster: CanMaster

    def __init__(self):
        super().__init__()
        self.machine = Machine()

    def initialize(self) -> None:
        self.machine.initialise()
        self.app = QApplication(sys.argv)
        self.window = MainWindow(self)
        self.window.showFullScreen()
        sys.exit(self.app.exec_())

    def start(self):
        while True:
            self.machine.updateMachineInfo()
            self.window.updateDashboard(self.machine.machineInfo)
            # sleep(0.1)

    def onUpdate(self) -> None:
        self.machine.updateMachineInfo()
        self.window.updateDashboard(self.machine.machineInfo)
        return super().onUpdate()
