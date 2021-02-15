import sys
from ..gui.gui import Gui

class Application:

    gui: Gui

    def __init__(self):
        super().__init__()

    def initialize(self) -> None:
        self.gui = Gui()
        sys.exit(self.gui.app.exec_())
