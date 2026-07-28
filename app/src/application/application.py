import logging
import sys

from PyQt6.QtWidgets import QApplication

from src.machine.machine import Machine

from ..gui.gui import MainWindow, WindowListener


class Application(WindowListener):
    machine: Machine

    def __init__(self):
        logging.info("Creating Application instance...")
        super().__init__()
        self.machine = Machine()

    def initialize(self) -> None:
        logging.info("Initializing Application...")
        self.machine.initialise()
        self.app = QApplication(sys.argv)
        self.window = MainWindow(self)
        logging.info("Showing main window...")
        # self.window.showFullScreen()
        self.window.show()
        logging.info("Starting application event loop...")
        sys.exit(self.app.exec())

    def shutdown(self) -> None:
        logging.info("Shutting down Application...")
        self.app.quit()

    def onUpdate(self) -> None:
        self.window.updateDashboard(
            self.machine.canMaster.dashMachineInfo,
            self.machine.messenger.getMessageSnapshot(),
        )
        return super().onUpdate()
