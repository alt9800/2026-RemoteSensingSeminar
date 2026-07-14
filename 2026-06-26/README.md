# 第2回：タイル配信② 自前配信とカートグラフィック

## ディレクトリ構成

```
2026-06-26/
├── slide.md
└── handson/
    ├── README.md
    ├── 00_setup/
    │   └── README.md          ← 事前確認・持ち物・Nginx インストール
    ├── 01_nginx/
    │   └── README.md          ← Nginx 設定・CORS・動作確認・エラー対処
    ├── 02_maputnik/
    │   ├── README.md          ← スタイル編集手順・スタイルの渡し方2パターン
    │   └── maputnik_guide.pdf ← ハンズオン指南書（印刷配布用）
    ├── 03_osm/
    │   └── README.md          ← OSM データモデル・iD エディタ手順・パイプライン・PWA
    ├── 04_raspi/
    │   ├── README.md          ← 受講者向け：デモの説明・接続方法・観察ポイント
    │   ├── SETUP.md           ← 講師向け：Pi 構築手順・データパイプライン・フォールバック構成
    │   ├── raster.html        ← Pi から配信するラスタータイルビューア
    │   └── vector.html        ← Pi から配信するベクタータイルビューア（PMTiles）
    └── 05_zero2w/
        ├── README.md          ← Pi Zero 2W + Martin 検証メモ（FOSS4G Hiroshima 向け）
        └── vector.html        ← 自分の PC で開いて Martin からタイルを取得する HTML
```