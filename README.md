# kart-machine-manager
全日本学生フォーミュラ大会 インパネ

## App

ryeでパッケージ管理をしています

参考\
https://zenn.dev/3w36zj6/scraps/de5a102362c405
https://rye-up.com/


以下のコマンドはappディレクトリで行ってください

* rye環境構築
```
rye sync
```

* 起動（本番）
```
rye run prod
```

* 起動（デバッグ）
```
rye run debug
```

* テスト
```
rye test
```

* 型チェック
```
rye run mypy .
```

* フォーマット
```
rye run ruff format
```

* 静的解析
```
rye run ruff check
```
```
rye run ruff check --fix
```

## CAN Mock
CANの疑似信号を出すだけのArduinoのコードです\
PlatformIO拡張機能をいれて使用してください