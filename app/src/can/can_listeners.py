import time
from dataclasses import dataclass
from typing import List

import can
import cantools.database

from src.models.models import (
    BatteryVoltage,
    DashMachineInfo,
    FuelPress,
    GearVoltage,
    OilTemp,
    WaterTemp,
)


@dataclass
class CanIdLength:
    id: int
    length: int


class DashInfoListener(can.Listener):
    dashMachineInfo: DashMachineInfo

    def __init__(self) -> None:
        super().__init__()
        self.dashMachineInfo = DashMachineInfo()

    def on_message_received(self, msg: can.Message) -> None:
        if msg.arbitration_id == 0x5F0:
            self.dashMachineInfo.setRpm(int.from_bytes(msg.data[0:2], "big"))
            self.dashMachineInfo.throttlePosition = int.from_bytes(msg.data[2:4]) / 10
            self.dashMachineInfo.waterTemp = WaterTemp(
                int.from_bytes(msg.data[4:6], "big") // 10
            )
            self.dashMachineInfo.oilTemp = OilTemp(
                int.from_bytes(msg.data[6:8], "big") // 10
            )
        elif msg.arbitration_id == 0x5F1:
            self.dashMachineInfo.oilPress.oilPress = (
                int.from_bytes(msg.data[0:2], "big") / 10
            )
            self.dashMachineInfo.gearVoltage = GearVoltage(
                int.from_bytes(msg.data[2:4], "big") / 1000
            )
            self.dashMachineInfo.batteryVoltage = BatteryVoltage(
                int.from_bytes(msg.data[4:6], "big") / 100
            )
        elif msg.arbitration_id == 0x5F2:
            self.dashMachineInfo.fuelPress = FuelPress(
                int.from_bytes(msg.data[2:4]) / 10
            )
            self.dashMachineInfo.brakePress.front = (
                int.from_bytes(msg.data[4:6], "big") / 10
            )
            self.dashMachineInfo.brakePress.rear = (
                int.from_bytes(msg.data[6:8], "big") / 10
            )
        elif msg.arbitration_id == 0x5F3:
            self.dashMachineInfo.fanEnabled = bool(msg.data[1])

        # ここの数字は後で変更


class UdpPayloadListener(can.Listener):
    MOTEC_CAN_ID_LENGTHS = [
        CanIdLength(0x5F0, 8),
        CanIdLength(0x5F1, 8),
        CanIdLength(0x5F2, 8),
        CanIdLength(0x5F3, 8),
        CanIdLength(0x5F4, 6),
    ]

    canIdLength: List[CanIdLength]
    receivedMessages: dict[int, can.Message]

    def __init__(self) -> None:
        dl1Dbc = cantools.database.load_file("./spec/can/dl1.dbc")
        if isinstance(dl1Dbc, cantools.database.can.database.Database):
            dl1CanIdLengths = list(
                map(lambda m: CanIdLength(m.frame_id, m.length), dl1Dbc.messages)
            )
        # CAN IDの小さい方から順に並べる
        self.canIdLength = sorted(
            self.MOTEC_CAN_ID_LENGTHS + dl1CanIdLengths, key=lambda il: il.id
        )

        # 最初は何も入っていない
        self.receivedMessages = {}

        super().__init__()

    def on_message_received(self, msg: can.Message) -> None:
        self.receivedMessages[msg.arbitration_id] = msg

    def getUdpPayload(self, machineId: int, runId: int, errorCode: int) -> bytes:
        bs = bytearray()
        bs += (machineId & 0xFFFFFFFF).to_bytes(4, "little")
        bs += (runId & 0xFFFFFFFF).to_bytes(4, "little")
        bs += (errorCode & 0xFF).to_bytes(1, "little")
        bs += (int(time.time() * 1000) & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little")
        for il in self.canIdLength:
            startIndex = len(bs)
            bs += bytes(il.length)
            if il.id in self.receivedMessages:
                for i in range(min(il.length, self.receivedMessages[il.id].dlc)):
                    bs[startIndex + i] = self.receivedMessages[il.id].data[i]
        return bytes(bs)
