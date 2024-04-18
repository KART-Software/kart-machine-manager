from src.can.can_master import CanMaster


class MachineException(BaseException):
    pass


class Machine:

    canMaster: CanMaster

    def __init__(self) -> None:
        pass

    def initialise(self) -> None:
        self.canMaster = CanMaster()
