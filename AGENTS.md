# AGENTS.md — kart-machine-manager

全日本学生フォーミュラ大会用カート インパネ (ダッシュボード) アプリケーション。  
Raspberry Pi (800×480) 上で PyQt5 フルスクリーンGUI を表示し、CAN バス経由で ECU データを取得・表示する。

## Quick Reference

| 操作 | コマンド (`app/` ディレクトリで実行) |
|------|------|
| 依存解決 | `rye sync` |
| 起動 (本番) | `rye run prod` |
| 起動 (デバッグ) | `rye run debug` |
| テスト | `rye test` |
| 型チェック | `rye run mypy .` |
| フォーマット | `rye run ruff format` |
| リント | `rye run ruff check` |
| リント自動修正 | `rye run ruff check --fix` |

> **注意**: コマンドはすべて `app/` ディレクトリで実行すること。

## Tech Stack

- **Python 3.11+** / パッケージ管理: **rye**
- **PyQt5** (GUI)、**python-can** (CAN バス通信)
- **ruff** (フォーマット & リント, line-length=88)、**mypy** (型チェック)
- **PlatformIO** (CAN Mock — Arduino UNO + MCP2515)

## Architecture

```
main.py → Application (WindowListener)
              ├── MainWindow (PyQt5 GUI, 50ms QTimer更新)
              └── Machine
                    ├── CanMaster → DashInfoListener → DashMachineInfo (モデル)
                    │              → UdpPayloadListener
                    ├── UdpTransmitter (30ms周期, クラウドへ送信)
                    └── Messenger (5s周期, HTTP ポーリング)
```

**データフロー**: CAN Bus → `CanMaster` → Listener → `DashMachineInfo` → `Application.onUpdate()` → `MainWindow.updateDashboard()`

## Key Conventions

- **環境切替**: `DEBUG` 環境変数で仮想CAN (`MockCanSender`) / 実CAN (`socketcan`) を自動切替
- **設定**: `.env` ファイル + `python-dotenv`。設定値は `src/util/config.py` でモジュール変数として公開
- **ドメインモデル**: `int`/`float` を継承したプリミティブクラス (`Rpm`, `WaterTemp` 等) に閾値判定ロジックを持たせる — [models.py](app/src/models/models.py) 参照
- **CAN データ形式**: ビッグエンディアン、2バイト単位、10倍/100倍/1000倍スケーリング
- **スレッドモデル**: メインスレッド = GUI、デーモンスレッド = CAN Mock / UDP送信 / HTTPポーリング
- **GUI更新**: `QTimer` 50ms → Observer パターン (`WindowListener`)

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
- `getRunId()` はクラウド API に接続できるまで**無限リトライ**する
- テストファイルは未作成 (`rye test` は動くがテストが無い)
- アイコンファイル名に typo: `MeesageIcon.png` (Message)

## Project Structure

```
app/
  main.py                  # エントリポイント
  .env                     # 環境設定
  src/
    application/           # Application (GUI ↔ Machine 橋渡し)
    can/                   # CAN 通信 (CanMaster, Listeners, MockSender)
    gui/                   # PyQt5 ウィジェット群
    machine/               # Machine (初期化・各コンポーネント保持)
    message/               # クラウド HTTP ポーリング
    models/                # ドメインモデル (DashMachineInfo 等)
    udp/                   # UDP 送信
    util/                  # 設定読み込み (config.py)
can-mock/                  # PlatformIO Arduino CAN モック
```
