from PyQt5.QtWidgets import (
    QDialog,
)

from abc import ABCMeta, abstractmethod


class WindowListener(metaclass=ABCMeta):
    @abstractmethod
    def onInitClick(self) -> None:
        pass


class MainWindow(QDialog):
    def __init__(self, listener: WindowListener):
        super(MainWindow, self).__init__(None)
        self.listener = listener
