from dataclasses import dataclass
import time
import can
import cantools.database
from typing import List

from src.models.models import (
    DashMachineInfo,
    Rpm,
    WaterTemp,
    OilTemp,
    OilPress,
    GearVoltage,
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
            self.dashMachineInfo.rpm = Rpm.from_bytes(msg.data[0:2], "little")
            self.dashMachineInfo.oilPress.setRequiredOilPress(self.dashMachineInfo.rpm)
            self.dashMachineInfo.waterTemp = WaterTemp(
                int.from_bytes(msg.data[4:6], "little") // 10
            )
            self.dashMachineInfo.oilTemp = OilTemp(
                int.from_bytes(msg.data[6:8], "little") // 10
            )
        elif msg.arbitration_id == 0x5F1:
            self.dashMachineInfo.oilPress = OilPress(
                int.from_bytes(msg.data[0:2], "little") / 10
            )
            self.dashMachineInfo.gearVoltage = GearVoltage(
                int.from_bytes(msg.data[2:4], "little") / 1000
            )
        # ここの数字は後で変更


class UdpPayloadListener(can.Listener):

    MOTEC_CAN_ID_LENGTHS = [
        CanIdLength(0x5F0, 8),
        CanIdLength(0x5F1, 8),
        CanIdLength(0x5F2, 4),
    ]

    canIdLength: List[CanIdLength]
    receivedMessages: dict[int, can.Message]

    def __init__(self) -> None:
        dl1Dbc = cantools.database.load_file("./spec/can/dl1.dbc")
        dl1CanIdLengths = list(
            map(lambda m: CanIdLength(m.frame_id, m.length), dl1Dbc.messages)
        )
        # CAN IDの小さい方から順に並べる
        self.canIdLength = sorted(
            self.MOTEC_CAN_ID_LENGTHS + dl1CanIdLengths, key=lambda il: il.id
        )

        self.receivedMessages = {}

        # 最初は何も入っていない
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
