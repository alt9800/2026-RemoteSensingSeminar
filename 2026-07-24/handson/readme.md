# 第5回 ハンズオン：GDAL変換パイプラインでDEMをTerrain RGBタイルにする

配布されたDEM（GeoTIFF）を起点に、WebGISで使える形式（COG / Terrain RGB PMTiles）へ変換するパイプラインを構築します。

## 全体の流れ

```
dem_src.tif
  │ 01: gdalinfo -stats        構造・CRS・NoDataの確認
  │ 02: gdalwarp               EPSG:3857化・クリップ・bilinear
  ▼
dem_10m.tif
  │ 03: rio cogeo create       COG化（この時点で配信可能）
  ▼
dem_cog.tif
  │ 04: rio rgbify             標高値 → RGB 24bitエンコード
  ▼
terrain.mbtiles
  │ 05: pmtiles convert        静的配信可能なアーカイブへ
  ▼
terrain.pmtiles → 06: MapLibre hillshadeで検証
```

## ディレクトリ構成

| ディレクトリ | 内容 | 当日の扱い |
|---|---|---|
| [`00_setup`](./00_setup/) | GDAL / rio-cogeo / rio-rgbify / pmtiles の導入 | 事前準備推奨 |
| [`01_gdalinfo`](./01_gdalinfo/) | データ構造の確認 | ハンズオン |
| [`02_warp_clip`](./02_warp_clip/) | 座標変換・クリップ・リサンプリング | ハンズオン |
| [`03_cog`](./03_cog/) | COG化と検証 | ハンズオン |
| [`04_terrainrgb`](./04_terrainrgb/) | Terrain RGBエンコード | ハンズオン |
| [`05_tiles_pmtiles`](./05_tiles_pmtiles/) | PMTiles化と配信 | ハンズオン |
| [`06_preview`](./06_preview/) | MapLibreによる目視検証 | ハンズオン |
| [`07_gsi1m_yamaguchi`](./07_gsi1m_yamaguchi/) | GSI 1mメッシュ（宇部新川・あすとぴあ周辺）の高精細化 | 発展・持ち帰り |
| [`08_pointcloud_dsm`](./08_pointcloud_dsm/) | 県公開点群からPDALでDSMを自作 | 発展・持ち帰り |

## 前提

- 第1〜2回のPMTiles / Nginx静的配信の環境（`pmtiles` CLI）があると05以降がスムーズです
- 配布データ `dem_src.tif` は講師から共有されるURLから取得してください

## 重要：成果物の保管

`terrain.pmtiles` と `dem_cog.tif` は**第6回でそのまま使用します**。削除しないでください。

## 講師用

- [`faculty/README.md`](./faculty/)：事前検証チェックリスト・当日運用メモ（参加者は読む必要はありません）
