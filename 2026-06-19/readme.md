# 構成ドラフト

```
./2026-06-19/
┣ slide.md
┗ handson/
  ┣ 00_setup.md              # 事前環境確認（GDAL・tippecanoe・Node.js）
  ┣ 01_pmtiles/              # メインハンズオン
  ┃  └ index.html            # MapLibre + PMTiles 表示
  ┣ 02_tileservers/          # タイルサーバー比較（GitHub で一緒に眺める用）
  ┃  ┣ README.md             # 各サーバーの起動手順まとめ
  ┃  ┣ martin.yml            # Martin 設定ファイルサンプル
  ┃  └ tileserver-gl.json    # tileserver-gl 設定ファイルサンプル
  └ 03_rust_intro/           # 補足：Rust と Geo界隈のトレンド
     └ README.md             # rustup導入・WASMとの関係・関連クレート紹介
```