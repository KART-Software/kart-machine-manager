import sys
from PyQt5.QtWidgets import QApplication
from src.gui import MainWindow, WindowListener


class Application(WindowListener):
    def __init__(self):
        super().__init__()

    def initialize(self) -> None:
        app = QApplication(sys.argv)
        self.window = MainWindow(self)
        self.window.showMaximized()
        sys.exit(app.exec_())

    def onInitClick(self) -> None:
        print('')
