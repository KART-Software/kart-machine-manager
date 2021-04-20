# kart-machine-manager

## 開発環境

pipenvでパッケージ管理しています  
ビルドツールはmakeを使用してください

参考  
https://qiita.com/y-tsutsu/items/54c10e0b2c6b565c887a  
https://blog.mktia.com/make-command-on-windows/

以下のコマンドはappディレクトリで行ってください

### pipenv環境構築
    pipenv install --dev

### 推奨
環境構築前に以下のコマンドでプロジェクトの配下に仮想環境を作成できます  
```
export PIPENV_VENV_IN_PROJECT=true
```

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