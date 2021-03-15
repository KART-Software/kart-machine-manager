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
        print("init")

    def initialize(self) -> None:
        print("initialize")
        self.app = QApplication(sys.argv)
        self.window = MainWindow(self)
        self.window.showFullScreen()
        sys.exit(self.app.exec_())

    def start(self):
        print("started")
        while True:
            self.canMaster.updateCanInfo()
            self.machine.updateMachineInfo()
            self.window.updateDashboard(self.machine.machineInfo)
            # sleep(0.1)

    def onUpdate(self) -> None:
        self.machine.updateMachineInfo()
        self.window.updateDashboard(self.machine.machineInfo)
        print(self.machine.machineInfo.rpm)
        return super().onUpdate()
