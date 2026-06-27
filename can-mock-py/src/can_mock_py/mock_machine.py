from typing import List

import can


class MockMachine:
    """擬似マシンの状態と、それを CAN フレームへ変換するロジック。

    app/src/can/mock_can_sender.py の MockMachine と同じ仕様。
    0x5F0〜0x5F4 の 5 フレームを生成する。
    """

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
    brakePresureFront: float
    brakePresureRear: float
    fanEnabled: bool
    istUp: bool
    istDown: bool
    inputRpm: int
    outputRpm: int
    oilTemperature2: float
    oilTemperature3: float
    coolantTemperature: float

    def __init__(self) -> None:
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
        self.brakePresureFront = 0
        self.brakePresureRear = 0
        self.fanEnabled = False
        self.istUp = False
        self.istDown = False
        self.inputRpm = 0
        self.outputRpm = 0
        self.oilTemperature2 = 0
        self.oilTemperature3 = 0
        self.coolantTemperature = 0

    def update(self, t: int) -> None:
        """経過ミリ秒 t に応じて各値を更新する。"""
        self.rpm = t % 10000
        self.throttlePosition = (t % 1000) / 10.0
        self.engineTemperature = (t % 1400) / 10.0
        self.oilTemperature = (t % 1600) / 10.0
        self.oilPressure = (t % 1200) / 10.0
        self.gearVoltage = (t % 5000) / 1000.0
        self.batteryVoltage = (t % 13000) / 1000.0
        self.lambda_ = 0.7 + (t % 600) / 1000.0
        self.manifoldPressure = (t % 10000) / 100.0
        self.fuelPressure = (t % 3000) / 10.0
        self.brakePresureFront = (t % 6000) / 10.0
        self.brakePresureRear = 600.0 - (t % 6000) / 10.0
        self.fanEnabled = bool((t % 10000) // 5000)
        self.istUp = bool((t % 8000) // 4000)
        self.istDown = not bool((t % 8000) // 4000)
        self.inputRpm = t % 5000
        self.outputRpm = t % 4500
        self.oilTemperature2 = (t % 1200) / 10.0
        self.oilTemperature3 = (t % 1200) / 10.0
        self.coolantTemperature = (t % 1200) / 10.0

    def toMessages(self) -> List[can.Message]:
        msgs = []
        bs = bytearray()
        bs += (self.rpm & 0xFFFF).to_bytes(2, "big")
        bs += (int(self.throttlePosition * 10) & 0xFFFF).to_bytes(2, "big")
        bs += (int(self.engineTemperature * 10) & 0xFFFF).to_bytes(2, "big")
        bs += (int(self.oilTemperature * 10) & 0xFFFF).to_bytes(2, "big")
        msgs.append(can.Message(arbitration_id=0x5F0, is_extended_id=False, data=bs))

        bs = bytearray()
        bs += (int(self.oilPressure * 10) & 0xFFFF).to_bytes(2, "big")
        bs += (int(self.gearVoltage * 1000) & 0xFFFF).to_bytes(2, "big")
        bs += (int(self.batteryVoltage * 100) & 0xFFFF).to_bytes(2, "big")
        bs += (int(self.lambda_ * 1000) & 0xFFFF).to_bytes(2, "big")
        msgs.append(can.Message(arbitration_id=0x5F1, is_extended_id=False, data=bs))

        bs = bytearray()
        bs += (int(self.manifoldPressure * 10) & 0xFFFF).to_bytes(2, "big")
        bs += (int(self.fuelPressure * 10) & 0xFFFF).to_bytes(2, "big")  # 35, 36
        bs += (int(self.brakePresureFront * 10) & 0xFFFF).to_bytes(2, "big")  # 37, 38
        bs += (int(self.brakePresureRear * 10) & 0xFFFF).to_bytes(2, "big")  # 39, 40
        msgs.append(can.Message(arbitration_id=0x5F2, is_extended_id=False, data=bs))

        bs = bytearray()
        bs += b"\x00\x01" if self.fanEnabled else b"\x00\x00"  # 41, 42
        if (self.istUp, self.istDown) == (False, False):
            st = b"\x00\x00"
        elif (self.istUp, self.istDown) == (False, True):
            st = b"\x00\x01"
        elif (self.istUp, self.istDown) == (True, False):
            st = b"\x00\x02"
        else:
            st = b"\x00\x03"
        bs += st  # 43, 44
        bs += (self.inputRpm & 0xFFFF).to_bytes(2, "big")  # 45, 46
        bs += (self.outputRpm & 0xFFFF).to_bytes(2, "big")  # 47, 48
        msgs.append(can.Message(arbitration_id=0x5F3, is_extended_id=False, data=bs))

        bs = bytearray()
        bs += (int(self.oilTemperature2 * 10) & 0xFFFF).to_bytes(2, "big")  # 49, 50
        bs += (int(self.oilTemperature3 * 10) & 0xFFFF).to_bytes(2, "big")  # 51, 52
        bs += (int(self.coolantTemperature * 10) & 0xFFFF).to_bytes(2, "big")  # 53, 54
        msgs.append(can.Message(arbitration_id=0x5F4, is_extended_id=False, data=bs))

        return msgs
