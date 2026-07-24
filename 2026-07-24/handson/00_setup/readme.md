[ハンズオン目次に戻る](../)

# 00. 環境準備

## 必要なツール

| ツール | 用途 | 確認コマンド |
|---|---|---|
| GDAL 3.4以降 | 変換パイプラインの中核 | `gdalinfo --version` |
| Python 3.9以降 | rioツール群の実行 | `python3 --version` |
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

`rio-cogeo` と `rio-rgbify` はシステムのPython環境を汚さないよう、仮想環境内に導入します。

### venvを使う場合

```sh
python3 -m venv .venv
source .venv/bin/activate   # Windowsは .venv\Scripts\activate

pip install rio-cogeo rio-rgbify
```

以降の作業も、このディレクトリで作業する際は `source .venv/bin/activate` を先に実行してください。抜けるときは `deactivate` です。

### uvを使う場合

インストールが速いため、時間が限られている場合はuvでも構いません。手順自体は同じです。

```sh
uv venv
source .venv/bin/activate

uv pip install rio-cogeo rio-rgbify
```

どちらを使っても後続の手順に差はありません。以降の資料では `pip install` と表記しますが、uv環境では `uv pip install` に読み替えてください。

`rio rgbify` の導入に失敗する・実行時エラーになる場合は `04_terrainrgb` の代替手順（gdal_calcによる自前エンコード）に進めます。詰まったら先へ進んでください。

## pmtiles CLI

go-pmtiles（Go実装）のCLIツールです。これまでの回では扱っていないため、今回新たに導入します。

### macOS

```sh
brew install protomaps/tap/pmtiles
pmtiles version
```

### Linux / Windows（バイナリ取得）

https://github.com/protomaps/go-pmtiles/releases から環境に合ったバイナリを取得し、PATHの通ったディレクトリに配置します。

```sh
# 例：Linux x86_64
curl -L -o pmtiles.tar.gz \
  https://github.com/protomaps/go-pmtiles/releases/latest/download/go-pmtiles_Linux_x86_64.tar.gz
tar xzf pmtiles.tar.gz
sudo mv pmtiles /usr/local/bin/
pmtiles version
```

Windowsは対応するzipを展開し、実行ファイルのパスをPATHに追加してください。

第1回で使用した `pmtiles` JSライブラリ（ブラウザでのタイル読み込み用）とは別物です。今回のCLIはmbtilesからPMTiles形式へ変換するためのコマンドラインツールです。

## 動作確認（全部そろったか）

```sh
gdalinfo --version
rio cogeo --help
rio rgbify --help
pmtiles version
```

4つすべてが応答すれば準備完了です。

---

次: [01. データ構造の確認](../01_gdalinfo/)