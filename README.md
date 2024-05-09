# kart-machine-manager
全日本学生フォーミュラ大会 インパネ

## App

ryeでパッケージ管理をしています

参考\
https://zenn.dev/3w36zj6/scraps/de5a102362c405
https://rye-up.com/

makeコマンドもインストールしてください\
https://blog.mktia.com/make-command-on-windows/


以下のコマンドはappディレクトリで行ってください

* rye環境構築
```
rye sync
```

* 起動（本番）
```
make prod
```

* 起動（デバッグ）
```
make debug
```

* テスト
```
make test
```

* 型チェック
```
make type-check
```

* フォーマット
```
make format
```

* 静的解析
```
make lint
```
```
make lint-fix
```

## CAN Mock
CANの疑似信号を出すだけのArduinoのコードです\
PlatformIO拡張機能をいれて使用してください