# can-mock-py

`can-mock` (Arduino + MCP2515) / `app/src/can/mock_can_sender.py` と同じ擬似マシンの
CAN フレームを、PC に接続した **slcan** シリアル CAN アダプタ (CANable など) 経由で送信する
Python 実装です。

- 依存: [`python-can`](https://python-can.readthedocs.io/) + [`pyserial`](https://pyserial.readthedocs.io/)
- インターフェース: `slcan`
- 送信フレーム: `0x5F0`〜`0x5F4` (送信仕様は `app/src/can/mock_can_sender.py` と同一)
- 既定ビットレート: 1 Mbps / 既定送信間隔: 33 ms

## セットアップ

```sh
uv sync
```

## 実行

```sh
# 既定 (/dev/ttyACM0, 1Mbps, 33ms間隔)
uv run can-mock-py

# ポート・ビットレート・送信間隔を指定
uv run can-mock-py --channel /dev/ttyUSB0 --bitrate 1000000 --interval 0.033
```

`Ctrl-C` で停止します。

| オプション | 既定値 | 説明 |
| --- | --- | --- |
| `-c`, `--channel` | `/dev/ttyACM0` | slcan アダプタのシリアルポート |
| `-b`, `--bitrate` | `1000000` | CAN ビットレート [bps] |
| `-i`, `--interval` | `0.033` | 送信間隔 [s] |

## 動作確認 (実機なし)

`socat` で仮想シリアルペアを作り、片側を slcan として実機の代わりに使えます。
あるいは `python-can` の `slcand` / 受信側スクリプトで確認してください。
