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

* 起動（本番）
```
uv run main.py
```

* 起動（デバッグ）
```
DEBUG=TRUE uv run main.py
```

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