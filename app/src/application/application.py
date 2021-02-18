import sys

from src.machine.machine import Machine
from ..gui.gui import Gui


class Application:

    gui: Gui

    machine: Machine

    def __init__(self):
        super().__init__()

    def initialize(self) -> None:
        self.machine = Machine()
        self.gui = Gui()
        sys.exit(self.gui.app.exec_())
