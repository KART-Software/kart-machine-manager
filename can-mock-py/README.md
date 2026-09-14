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
| `--reinit-interval` | `1.0` | slcan チャネルを C/O 再初期化して bus-off 自動復帰する間隔 [s] (`<=0` で無効) |

## bus-off 自動復帰

ベンチはノードが CANable とボードの 2 つだけなので、ボードが落ちる (電源断 /
M7 リセット / OTA) と ACK 相手が消え、CANable は数十 ms で **bus-off** に入り沈黙する。
slcan の CANable2 は bus-off を報告しない (F/V 無応答) ため検知できないが、slcan の
`C`→`O`(CAN チャネルだけ再初期化)を撃つと ~10ms で bus-off が晴れる (serial は
閉じないので CDC-ACM リセット ~2s は起きない)。そこで **`--reinit-interval` 間隔で
無条件に C/O 再初期化**する:健全時は 1 フレーム落ちる程度で無害、bus-off 時は次の
周期で自動復帰。ボードとの IP 到達性に依存せず CANable 単体で動く。実機で電源
サイクル→無操作で送信再開を確認 (2026-09-14)。

## 動作確認 (実機なし)

`socat` で仮想シリアルペアを作り、片側を slcan として実機の代わりに使えます。
あるいは `python-can` の `slcand` / 受信側スクリプトで確認してください。
