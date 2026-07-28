# kart-machine-manager (C++ port)

`app/`(Python + PyQt6) の C++ / Qt6 Widgets 移植。PyQt6 の import 約 1.5 秒
（起動高速化のユーザースペース側の下限だった）をなくすことが目的。

## 設計: 直接起動（デーモン + notifier 廃止）

Python 版の kmmd（デーモン）+ kmm-start（notifier）分割は「PyQt6 の import
約 1.5 秒を weston 起動の裏に隠す」ための仕掛けだった。C++ では隠すものが
ないので廃止し、**プロセス起動 = 即 GUI 表示**。weston / can0 の準備待ちは
systemd のユニット順序で表現する:

```ini
[Unit]
After=weston.service can0-up.service data.mount
Requires=weston.service data.mount
Wants=can0-up.service

[Service]
Type=notify        # 初回 expose（実描画）で READY=1 を送る（libsystemd 不使用）
ExecStart=/usr/bin/kmm
```

`kmm-start.service`・unix socket の START/PING/STOP プロトコル・
`socket_notify.py` は不要になった。停止/再起動は systemctl で行う
（kart-image.bb の `resolved-delayed-start.timer` も `After=kmm.service` に
付け替え済み）。

- **環境変数は Python 版と同一**: `MACHINE_ID`, `UDP_ADDRESS`, `UDP_PORT`,
  `CLOUD_RUN_API_ENDPOINT`, `CLOUD_MESSAGE_API_ENDPOINT`,
  `CLOUD_LAPTIME_API_ENDPOINT`, `DEBUG`（`KMM_SOCKET_PATH` は廃止）。
  カレントディレクトリの `.env` も dotenv 同様に読む（既存環境変数は上書きしない）。
- **UDP ペイロード形式同一**: machineId u32le + runId u32le + errorCode u8 +
  epoch-ms u64le + 固定スロット (0x5F0–0x5F4 = 8,8,8,8,6 / 0x700–0x70E = 8) = 175 bytes。
- **DEBUG=TRUE** で mock CAN（Python 版 `MockCanSender` と同じ波形を 33ms 周期で生成）。
  それ以外は `can0` を SocketCAN raw で直接 read。

## ソース対応表

| C++ | Python |
|-----|--------|
| `src/main.cpp` | `application.py` + `machine.py`（main.py のデーモン部は廃止） |
| `src/models.hpp` | `src/models/models.py` |
| `src/config.{hpp,cpp}` | `src/util/config.py` |
| `src/canbus.{hpp,cpp}` | `src/canbus/` + `src/can/mock_can_sender.py` |
| `src/stores.{hpp,cpp}` | `src/can/can_listeners.py` |
| `src/udp_transmitter.{hpp,cpp}` | `src/udp/udp_transmitter.py` |
| `src/cloud.{hpp,cpp}` | `getRunId()` + `src/message/message.py` |
| `src/gui/widgets.{hpp,cpp}` | `src/gui/self_defined_widgets.py` |
| `src/gui/mainwindow.{hpp,cpp}` | `src/gui/gui.py` |

HTTP は Qt Network（メインループ上で非同期、run ID は 1 秒間隔リトライ）。
アイコンは qrc でバイナリに埋め込み。

## ビルド

```bash
sudo apt install qt6-base-dev   # ホスト開発時
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
```

## 実行（ローカル動作確認）

```bash
export MACHINE_ID=7 UDP_ADDRESS=127.0.0.1 UDP_PORT=41234 \
  CLOUD_RUN_API_ENDPOINT=http://... CLOUD_MESSAGE_API_ENDPOINT=http://... \
  CLOUD_LAPTIME_API_ENDPOINT=http://... DEBUG=TRUE
./build/kmm   # 即ウィンドウ表示（mock CAN 駆動）
```

## 実機向けビルド（Yocto SDK）

SDK インストーラ（`bitbake meta-toolchain-qt6`、kmm-yocto 側で生成・配布）を
展開して environment-setup を source すれば、素の cmake がクロスビルドになる:

```bash
source <SDK>/environment-setup-cortexa76-poky-linux
cmake -B build-rpi5 && cmake --build build-rpi5 -j
```

## Yocto 統合

kmm-yocto 側で統合済み: `meta-kart/recipes-app/kart-machine-manager/`
（`qt6-cmake` + `DEPENDS qtbase`、この repo を `SRCREV` 固定で取得して
`/usr/bin/kmm` にインストール、`kmm.service` 同梱）。
アプリ更新はレシピの `SRCREV` を上げて再ビルド → OTA。
