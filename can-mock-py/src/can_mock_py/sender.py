import time

import can

from can_mock_py.mock_machine import MockMachine

DEFAULT_CHANNEL = "/dev/ttyACM0"
DEFAULT_BITRATE = 1000000
DEFAULT_INTERVAL = 0.033


class MockCanSender:
    """slcan インターフェース経由で擬似マシンの CAN フレームを送信する。

    app/src/can/mock_can_sender.py の MockCanSender と同じ送信仕様だが、
    バスを virtual ではなく slcan (pyserial 経由のシリアル CAN アダプタ) で開く。
    """

    machine: MockMachine

    def __init__(
        self,
        channel: str = DEFAULT_CHANNEL,
        bitrate: int = DEFAULT_BITRATE,
        interval: float = DEFAULT_INTERVAL,
    ) -> None:
        self.bus = can.Bus(interface="slcan", channel=channel, bitrate=bitrate)
        self.machine = MockMachine()
        self.interval = interval

    def close(self) -> None:
        self.bus.shutdown()

    def sendOnce(self) -> None:
        self.machine.update(int(time.time() * 1000))
        for msg in self.machine.toMessages():
            self.bus.send(msg)

    def sendEvery(self) -> None:
        while True:
            self.sendOnce()
            time.sleep(self.interval)
