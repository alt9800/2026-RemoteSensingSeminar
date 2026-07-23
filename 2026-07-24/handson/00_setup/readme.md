# 00. 環境準備

## 必要なツール

| ツール | 用途 | 確認コマンド |
|---|---|---|
| GDAL 3.4以降 | 変換パイプラインの中核 | `gdalinfo --version` |
| Python 3.9以降 + pip | rioツール群の実行 | `python3 --version` |
| rio-cogeo | COG生成・検証 | `rio cogeo --help` |
| rio-rgbify | Terrain RGBエンコード | `rio rgbify --help` |
| pmtiles CLI | mbtiles → PMTiles変換 | `pmtiles version` |

## GDALの導入

### Windows

OSGeo4Wインストーラを使用します。QGISを導入済みの場合は「OSGeo4W Shell」からGDALコマンドが使えます（本ハンズオンはこれで十分です）。

```
OSGeo4W Shell を起動して:
gdalinfo --version
```

### macOS

```sh
brew install gdal
gdalinfo --version
```

### Linux (Ubuntu/Debian)

```sh
sudo apt install gdal-bin python3-gdal
gdalinfo --version
```

## Python系ツールの導入

```sh
pip install rio-cogeo rio-rgbify
```

- 仮想環境（venv）の利用を推奨します
- `rio rgbify` の導入に失敗する・実行時エラーになる場合は `04_terrainrgb` の代替手順（gdal_calcによる自前エンコード）に進めます。詰まったら先へ進んでください

## pmtiles CLI

第2回で導入済みのものをそのまま使います。未導入の場合：

- https://github.com/protomaps/go-pmtiles/releases から各OS向けバイナリを取得しPATHを通す

## 動作確認（全部そろったか）

```sh
gdalinfo --version
rio cogeo --help
rio rgbify --help
pmtiles version
```

4つすべてが応答すれば準備完了です。
