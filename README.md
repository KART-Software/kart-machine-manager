# kart-machine-manager
全日本学生フォーミュラ大会 インパネ

## App

uvでパッケージ管理をしています

参考\
https://docs.astral.sh/uv/


以下のコマンドはappディレクトリで行ってください

* 環境構築
```
uv sync
```

* デーモン起動（本番）
```
uv run main.py
```

* デーモン起動（デバッグ）
```
DEBUG=TRUE uv run main.py
```

* GUI起動通知（UnixソケットにSTART送信）
```
uv run python -m src.ipc.socket_notify START
```

* デーモン疎通確認
```
uv run python -m src.ipc.socket_notify PING
```

* デーモン停止
```
uv run python -m src.ipc.socket_notify STOP
```

デフォルトのソケットパスは `/run/user/<uid>/kmm.sock` です。ディレクトリに書き込み権限がない場合は `/tmp/kmm.sock` に自動フォールバックします。明示的に指定する場合は `KMM_SOCKET_PATH` 環境変数で上書きできます。

* テスト
```
uv run pytest
```

* 型チェック
```
uv run mypy .
```

* フォーマット
```
uv run ruff format
```

* 静的解析
```
uv run ruff check
```
```
uv run ruff check --fix
```

## CAN Mock
CANの疑似信号を出すだけのArduinoのコードです\
PlatformIO拡張機能をいれて使用してください