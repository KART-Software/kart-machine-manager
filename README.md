# kart-machine-manager

## 開発環境

poetryでパッケージ管理しています  
ビルドツールはmakeを使用してください

参考  
https://org-technology.com/posts/python-poetry.html <br>
https://cocoatomo.github.io/poetry-ja/ <br>
https://kk6.hateblo.jp/entry/2018/12/20/124151

## 使用方法

### 推奨
環境構築前に以下のコマンドでプロジェクトの配下に仮想環境を作成できます。
```bash
poetry config virtualenvs.in-project true
```

### poetry環境構築
    poetry install

### 起動（本番）
    make prod

### 起動(デバッグ)
    make debug

### テスト
    make test

### 型チェック
    make type-check

### フォーマット
    make format

### 静的解析
    make lint

### 速度評価(cProfile)
    make prod-cProfile
or
```
make debug-cProfile
```