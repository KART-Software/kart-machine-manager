# AGENTS.md — kart-machine-manager

全日本学生フォーミュラ大会用カート インパネ (ダッシュボード) アプリケーション。  
Raspberry Pi (800×480) 上で PyQt6 フルスクリーンGUI を Wayland 上で表示し、CAN バス経由で ECU データを取得・表示する。

## Quick Reference

| 操作 | コマンド (`app/` ディレクトリで実行) |
|------|------|
| 依存解決 | `uv sync` |
| デーモン起動 (本番) | `uv run python main.py` |
| デーモン起動 (デバッグ) | `DEBUG=TRUE uv run python main.py` |
| GUI 起動通知 | `uv run python -m src.ipc.socket_notify START` |
| 疎通確認 | `uv run python -m src.ipc.socket_notify PING` |
| デーモン停止 | `uv run python -m src.ipc.socket_notify STOP` |
| テスト | `uv run pytest` |
| 型チェック | `uv run mypy .` |
| フォーマット | `uv run ruff format` |
| リント | `uv run ruff check` |
| リント自動修正 | `uv run ruff check --fix` |

> **注意**: コマンドはすべて `app/` ディレクトリで実行すること。

## Tech Stack

- **Python 3.12+** / パッケージ管理: **uv**
- **PyQt6** (GUI, Wayland ネイティブ)、**python-can** (CAN バス通信)
- **ruff** (フォーマット & リント, line-length=88)、**mypy** (型チェック)
- **PlatformIO** (CAN Mock — Arduino UNO + MCP2515)

## Architecture

```
main.py (daemon)
  ├── setup_logging() → log/app_YYYYMMDD_HHMMSS.log
  └── run_daemon()
        ├── UnixTriggerServer (Unix ソケット待受)
        │     START → Application.initialize() (GUI 起動, 1回のみ)
        │     PING  → PONG
        │     STOP  → グレースフル終了
        └── Application (WindowListener)
              ├── MainWindow (PyQt6 GUI, 50ms QTimer更新)
              └── Machine
                    ├── CanMaster → DashInfoListener → DashMachineInfo (モデル)
                    │              → UdpPayloadListener
                    ├── UdpTransmitter (30ms周期, クラウドへ送信)
                    └── Messenger (5s周期, HTTP ポーリング)
```

**データフロー**: CAN Bus → `CanMaster` → Listener → `DashMachineInfo` → `Application.onUpdate()` → `MainWindow.updateDashboard()`

## IPC Protocol (Unix ソケット)

デーモンは Unix ソケットで外部コマンドを受け付ける。ソケットパスのデフォルトは `/run/user/<uid>/kmm.sock`（権限不足時は `/tmp/kmm.sock` にフォールバック）。`KMM_SOCKET_PATH` 環境変数で上書き可能。

| コマンド | レスポンス | 意味 |
|----------|-----------|------|
| `START` | `ACK_STARTED` | GUI 初回起動成功 |
| `START` | `ACK_ALREADY_RUNNING` | GUI 既に起動済み |
| `PING` | `PONG` | ヘルスチェック |
| `STOP` | `ACK_STOPPING` | グレースフル終了 |
| その他 | `ERR_UNKNOWN_COMMAND` | 不明コマンド |

## Key Conventions

- **デーモンモード**: `main.py` は GUI を即時起動せず、Unix ソケット経由で `START` を受信してから起動する
- **環境切替**: `DEBUG` 環境変数で仮想CAN (`MockCanSender`) / 実CAN (`socketcan`) を自動切替
- **設定**: `.env` ファイル + `python-dotenv`。設定値は `src/util/config.py` でモジュール変数として公開
- **ドメインモデル**: `int`/`float` を継承したプリミティブクラス (`Rpm`, `WaterTemp` 等) に閾値判定ロジックを持たせる — [models.py](app/src/models/models.py) 参照
- **CAN データ形式**: ビッグエンディアン、2バイト単位、10倍/100倍/1000倍スケーリング
- **スレッドモデル**: メインスレッド = GUI、デーモンスレッド (すべて `setDaemon(True)`) = CAN Mock / UDP送信 / HTTPポーリング
- **GUI更新**: `QTimer` 50ms → Observer パターン (`WindowListener`)
- **ロギング**: `main.py` の `setup_logging()` で stdout + stderr + `log/` ディレクトリにファイル出力

## Environment Variables

| 変数 | 用途 | デフォルト |
|------|------|-----------|
| `DEBUG` | `TRUE` で仮想 CAN + モック使用 | 未設定 (本番モード) |
| `KMM_SOCKET_PATH` | Unix ソケットパスの上書き | `/run/user/<uid>/kmm.sock` |

`.env` ファイルの設定値: `MACHINE_ID`, `UDP_ADDRESS`, `UDP_PORT`, `CLOUD_RUN_API_ENDPOINT`, `CLOUD_MESSAGE_API_ENDPOINT`, `CLOUD_LAPTIME_API_ENDPOINT`, `CAN_INTERFACE`(省略時 can0)

## CAN ID Map

| ID | 内容 |
|----|------|
| `0x5F0` | RPM, スロットル, 水温, 油温 |
| `0x5F1` | 油圧, ギア電圧, バッテリー電圧 |
| `0x5F2` | 燃圧, ブレーキ圧 (前/後) |
| `0x5F3` | ファンスイッチ |
| `0x700`–`0x70E` | データロガー用 |

## Known Pitfalls

- `CanMaster.__init__` が `subprocess.run("sudo ...")` を呼ぶため、本番では **root 権限が必要**
- `getRunId()` はクラウド API に接続できるまで**無限リトライ**する — API 不通時にスレッドがブロックされる
- テストファイルは未作成 (`uv run pytest` は動くがテストが無い)
- アイコンファイル名に typo: `MeesageIcon.png` (Message)
- ソケット `/run/user/<uid>/kmm.sock` のディレクトリが存在しない場合あり — `/tmp/kmm.sock` にフォールバック

## Project Structure

```
app/
  main.py                  # エントリポイント (デーモン)
  .env                     # 環境設定
  log/                     # ログ出力先
  src/
    application/           # Application (GUI ↔ Machine 橋渡し)
    can/                   # CAN 通信 (CanMaster, Listeners, MockSender)
    gui/                   # PyQt6 ウィジェット群
    ipc/                   # Unix ソケット IPC (TriggerServer, Notify)
    machine/               # Machine (初期化・各コンポーネント保持)
    message/               # クラウド HTTP ポーリング
    models/                # ドメインモデル (DashMachineInfo 等)
    udp/                   # UDP 送信
    util/                  # 設定読み込み (config.py)
can-mock/                  # PlatformIO Arduino CAN モック
```
