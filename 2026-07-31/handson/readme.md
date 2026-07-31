# 第6回 ハンズオン：高さデータの3D表示・オーバーレイ・現地調査ツール化

第5回で作成した `terrain.pmtiles` を起点に、ブラウザ上で3D地形として表示し、NDWIラスターや防災重点溜池データを重ねたビューアを組み立てます。

## 全体の流れ

```
terrain.pmtiles（第5回の成果物）
  │ 01: MapLibre terrain          3D表示・垂直誇張・標高読み取り
  │ 02: Mapterhorn比較            解像度とエンコード方式の違いを見る
  ▼
3D地形ビューア
  │ 03: NDWI・溜池オーバーレイ    ハザードマップビューアに発展させる
  ▼
現地調査ツール
```

## ディレクトリ構成

| ディレクトリ | 内容 | 当日の扱い |
| ------------ | ---- | ---------- |
| [`00_setup`](./00_setup/) | 前回成果物の確認・配布データの取得 | 最初に確認 |
| [`01_terrain3d`](./01_terrain3d/) | MapLibre terrainによる3D表示 | ハンズオン |
| [`02_mapterhorn_compare`](./02_mapterhorn_compare/) | Mapterhornとの比較 | ハンズオン |
| [`03_hazard_viewer`](./03_hazard_viewer/) | NDWI・防災重点溜池オーバーレイ | ハンズオン |
| [`04_deckgl_terrain`](./04_deckgl_terrain/) | deck.gl TerrainLayerでの実装比較 | 発展・持ち帰り |
| [`05_3dtiles_plateau`](./05_3dtiles_plateau/) | PLATEAU 3D Tilesの重ね合わせ | 発展・持ち帰り |
| [`06_offline_design`](./06_offline_design/) | オフライン設計の考え方・容量見積り | 読み物 |
| [`99_ar_dem`](./99_ar_dem/) | DEMのAR表示（アイディア・参考実装） | 参考 |

## 前提

- 第5回の成果物 `terrain.pmtiles` と `dem_cog.tif`（未完走の方は [`00_setup`](./00_setup/) の配布データを使用）
- ローカルHTTPサーバー（`python3 -m http.server` や `http-server` など）

## 講師用

- [`faculty/README.md`](./faculty/)：事前検証チェックリスト・既知の問題・引き継ぎ事項（参加者は読む必要はありません）
