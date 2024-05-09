import threading
import time
from typing import List

import can
import cantools.database


class MockMachine:
    rpm: int
    throttlePosition: float
    engineTemperature: float
    oilTemperature: float
    oilPressure: float
    gearVoltage: float
    batteryVoltage: float
    lambda_: float
    manifoldPressure: float
    fuelPressure: float
    wheelSpeedFrontLeft: float
    wheelSpeedFrontRight: float
    wheelSpeedRearLeft: float
    wheelSpeedRearRight: float
    strokeFrontLeft: float
    strokeFrontRight: float
    strokeRearLeft: float
    strokeRearRight: float
    latitude: float
    longitude: float
    altitude: float
    gpsSpeed2D: float
    gpsSpeed3D: float
    verticalAccel: float
    lateralAccel: float
    longitudinalAccel: float
    speed: float
    yawRate: float
    pitchRate: float
    rollRate: float

    def __init__(self):
        self.dl1Dbc = cantools.database.load_file("./spec/can/dl1.dbc")

        self.rpm = 0
        self.throttlePosition = 0
        self.engineTemperature = 0
        self.oilTemperature = 0
        self.oilPressure = 0
        self.gearVoltage = 0
        self.batteryVoltage = 0
        self.lambda_ = 0
        self.manifoldPressure = 0
        self.fuelPressure = 0
        self.wheelSpeedFrontLeft = 0
        self.wheelSpeedFrontRight = 0
        self.wheelSpeedRearLeft = 0
        self.wheelSpeedRearRight = 0
        self.strokeFrontLeft = 0
        self.strokeFrontRight = 0
        self.strokeRearLeft = 0
        self.strokeRearRight = 0
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.gpsSpeed2D = 0
        self.gpsSpeed3D = 0
        self.verticalAccel = 0
        self.lateralAccel = 0
        self.longitudinalAccel = 0
        self.speed = 0
        self.yawRate = 0
        self.pitchRate = 0
        self.rollRate = 0

    def toMessages(self) -> List[can.Message]:
        msgs = []
        bs = bytearray()
        bs += (self.rpm & 0xFFFF).to_bytes(2, "big")
        bs += (int(self.throttlePosition * 10) & 0xFFFF).to_bytes(2, "big")
        bs += (int(self.engineTemperature * 10) & 0xFFFF).to_bytes(2, "big")
        bs += (int(self.oilTemperature * 10) & 0xFFFF).to_bytes(2, "big")
        msgs.append(can.Message(arbitration_id=0x5F0, is_extended_id=False, data=bs))

        bs = bytearray()
        bs += (int(self.oilPressure) & 0xFFFF).to_bytes(2, "big")
        bs += (int(self.gearVoltage * 1000) & 0xFFFF).to_bytes(2, "big")
        bs += (int(self.batteryVoltage * 1000) & 0xFFFF).to_bytes(2, "big")
        bs += (int(self.lambda_ * 1000) & 0xFFFF).to_bytes(2, "big")
        msgs.append(can.Message(arbitration_id=0x5F1, is_extended_id=False, data=bs))

        bs = bytearray()
        bs += (int(self.manifoldPressure) & 0xFFFF).to_bytes(2, "big")
        bs += (int(self.fuelPressure) & 0xFFFF).to_bytes(2, "big")
        msgs.append(can.Message(arbitration_id=0x5F2, is_extended_id=False, data=bs))

        msgs += list(
            map(
                lambda m: can.Message(
                    arbitration_id=m.frame_id,
                    is_extended_id=False,
                    dlc=m.length,
                    data=bytes(m.length),
                ),
                self.dl1Dbc.messages,
            )
        )

        return msgs


class MockCanSender:
    machine: MockMachine

    def __init__(self) -> None:
        self.bus = can.Bus(channel="debug", interface="virtual")
        self.machine = MockMachine()

    def __del__(self) -> None:
        self.bus.shutdown()

    def updateMachine(self):
        t = int(time.time() * 1000)
        self.machine.rpm = t % 9500
        self.machine.throttlePosition = (t % 1000) / 20.0
        self.machine.engineTemperature = (t % 1200) / 10.0
        self.machine.oilTemperature = (t % 1200) / 10.0
        self.machine.oilPressure = (t % 2000) / 10.0
        self.machine.gearVoltage = (t % 5000) / 1000.0
        self.machine.batteryVoltage = (t % 12000) / 1000.0
        self.machine.lambda_ = 0.7 + (t % 600) / 1000.0
        self.machine.manifoldPressure = (t % 10000) / 100.0
        self.machine.fuelPressure = (t % 3000) / 10.0

    def sendEvery(self):
        while True:
            self.updateMachine()
            for msg in self.machine.toMessages():
                self.bus.send(msg)
            time.sleep(0.033)

    def start(self):
        t = threading.Thread(target=self.sendEvery)
        t.setDaemon(True)
        t.start()
