import time

import can

from can_mock_py.mock_machine import MockMachine

DEFAULT_CHANNEL = "/dev/ttyACM0"
DEFAULT_BITRATE = 1000000
DEFAULT_INTERVAL = 0.033
DEFAULT_REINIT_INTERVAL = 1.0


class MockCanSender:
    """slcan インターフェース経由で擬似マシンの CAN フレームを送信する。

    app/src/can/mock_can_sender.py の MockCanSender と同じ送信仕様だが、
    バスを virtual ではなく slcan (pyserial 経由のシリアル CAN アダプタ) で開く。

    bus-off 自動復帰 (2026-09-14): ベンチはノードが CANable とボードの 2 つだけ
    なので、ボードが落ちる (電源断 / M7 リセット / OTA) と ACK 相手が消え、
    CANable は数十 ms で **bus-off** に入り沈黙する。slcan の CANable2 は bus-off を
    報告しない (F/V コマンド無応答を実測) ため検知はできないが、slcan の
    ``C`` (close channel) → ``O`` (open channel) を撃つと CAN コントローラだけが
    ~10ms で再初期化され bus-off が晴れる (serial は閉じないので CANable の
    CDC-ACM リセット ~2s は起きない)。そこで **一定間隔で C/O 再初期化**を
    無条件に回す:健全時は 1 フレーム落ちる程度で無害、bus-off 時は次の周期で
    自動復帰する。ボードとの IP 到達性に依存しないので、CANable を挿しただけの
    別ホストでも動く。送信/シリアル例外 (USB 抜けなど) はバスごと再オープンする。
    """

    machine: MockMachine

    def __init__(
        self,
        channel: str = DEFAULT_CHANNEL,
        bitrate: int = DEFAULT_BITRATE,
        interval: float = DEFAULT_INTERVAL,
        reinit_interval: float = DEFAULT_REINIT_INTERVAL,
    ) -> None:
        self.channel = channel
        self.bitrate = bitrate
        self.interval = interval
        # <=0 で C/O 再初期化 (bus-off 自動復帰) を無効化
        self.reinit_interval = reinit_interval
        self.machine = MockMachine()
        self.bus = self._open()

    def _open(self) -> can.BusABC:
        return can.Bus(interface="slcan", channel=self.channel, bitrate=self.bitrate)

    def _reinit(self) -> None:
        """CAN チャネルだけ C/O で再初期化して bus-off を晴らす (serial は閉じない)。

        slcanBus.close()/open() は ``C``/``O`` の protocol コマンドのみでシリアル
        ポートには触れない (= CDC-ACM リセットの ~2s が起きない)。失敗したら
        バスごと再オープンにフォールバックする。
        """
        try:
            self.bus.close()  # -> _write("C")
            time.sleep(0.01)
            self.bus.open()  # -> _write("O")
        except Exception as e:
            print(f"can-mock: C/O 再初期化に失敗、バス再オープン: {e}", flush=True)
            self._reopen()

    def _reopen(self) -> None:
        try:
            self.bus.shutdown()
        except Exception:
            pass
        while True:
            try:
                self.bus = self._open()
                print("can-mock: バス再オープン完了", flush=True)
                return
            except Exception as e:
                print(f"can-mock: 再オープン失敗、1s 後に再試行: {e}", flush=True)
                time.sleep(1.0)

    def close(self) -> None:
        self.bus.shutdown()

    def sendOnce(self) -> None:
        self.machine.update(int(time.time() * 1000))
        for msg in self.machine.toMessages():
            self.bus.send(msg)

    def sendEvery(self) -> None:
        last_reinit = time.time()
        while True:
            if self.reinit_interval > 0 and (
                time.time() - last_reinit >= self.reinit_interval
            ):
                self._reinit()
                last_reinit = time.time()
            try:
                self.sendOnce()
            except Exception as e:
                print(f"can-mock: 送信エラー、バス再オープン: {e}", flush=True)
                self._reopen()
            time.sleep(self.interval)
