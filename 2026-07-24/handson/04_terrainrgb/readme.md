[ハンズオン目次に戻る](../)

# 04. Terrain RGBエンコード

標高値(Float32)を、PNGの24bit(RGB)に詰め替えます。

## エンコード式(Mapbox Terrain-RGB方式)

```
height = -10000 + ((R * 256 * 256 + G * 256 + B) * 0.1)
```

- 分解能 0.1m。MapLibre / deck.gl が標準でデコードできます
- 地理院標高タイルPNGは別方式であり互換性がありません
- 上記はあくまで解説式です。シェルにそのまま貼り付けるとエラーになるので注意してください(`(`や`*`がシェルのグロブ・演算子として解釈されます)

## 実行(rio-rgbify)

```sh
rio rgbify \
  --min-z 8 --max-z 14 \
  --interval 0.1 \
  --format png \
  dem_cog.tif terrain.mbtiles
```

| オプション | 意味 |
|---|---|
| `--interval 0.1` | エンコード分解能(式の `* 0.1` に対応) |
| `--max-z 14` | 最大ズーム。10m解像度に見合う上限の目安 |
| `--format png` | 可逆圧縮必須。JPEGを選ぶと標高値が壊れます |

max-zの決め方: ズームzでの1pxの地上サイズが元データの解像度を下回っても情報は増えません。10m DEMならz14前後(緯度による)が実用上限です。

## 既知の不具合1: rio-rgbifyが `densify_pts must be at least 2` で落ちる

比較的新しいGDAL/PROJの組み合わせの環境(Python 3.14 + 新しめのGDALで確認済み)で、rio-rgbifyが以下のエラーで停止することがあります。

```
rasterio._err.CPLE_AppDefinedError: densify_pts must be at least 2 if the output is geograpic.
```

rio-rgbify内部の`transform_bounds(..., densify_pts=0)`呼び出しが原因で、rio-rgbify自体は更新が止まっているため今後も直らない可能性があります(`mapbox/rio-rgbify` issue #39 で同様の報告あり)。

**試して直らなかった対処**: 入力を先にEPSG:4326へreprojectしてから実行する方法(コミュニティ報告あり)は、今回の環境ではさらに悪化し、`Error in sys.excepthook`のみが出て例外内容自体が握りつぶされました。Python 3.14の`sys.excepthook`まわりの変更とrio-rgbifyのマルチプロセス例外処理が噛み合っていないためとみられ、この経路は深追いしても得るものがありません。

rio-rgbifyがエラーになった場合は、下の代替手順に切り替えてください。

## NoData(海域・欠測)の扱い

NoData縁がノイズ状の崖として描画されることがあります。症状が出た場合:

```sh
# NoDataを標高0に置換してからエンコードする対処(海域が0mで問題ない場合)
gdal_calc.py -A dem_cog.tif --outfile=dem_filled.tif \
  --calc="numpy.where(A==-9999, 0, A)" --NoDataValue=none
```

厳密に透過させたい場合はアルファ付きの処理が必要になりますが、本日は上記の簡易対処で進めます。

## 代替手順: rio-rgbifyが動かない場合(gdal_calcによる自前エンコード)

エンコード式を逆に解くと、各チャンネルは次で求められます(動作確認済み)。

```sh
gdal_calc.py -A dem_cog.tif --outfile=r.tif --type=Byte \
  --calc="((A+10000)/0.1)//65536"
gdal_calc.py -A dem_cog.tif --outfile=g.tif --type=Byte \
  --calc="(((A+10000)/0.1)%65536)//256"
gdal_calc.py -A dem_cog.tif --outfile=b.tif --type=Byte \
  --calc="((A+10000)/0.1)%256"
gdal_merge.py -separate -o terrain_rgb.tif r.tif g.tif b.tif
```

`gdal_calc.py`はByte出力に既定でNoData=255を割り当てますが、標高由来のR/G/B値がこの範囲では255と衝突する見込みは低く、実害は確認されていません。

`terrain_rgb.tif`(3バンドByte、Terrain RGBエンコード済み)ができた時点で、経路が2つに分かれます。

### 経路1: PMTiles化する(05に進む場合。推奨)

```sh
gdal_translate terrain_rgb.tif terrain.mbtiles -of MBTILES
gdaladdo -r average terrain.mbtiles 2 4 8 16 32 64
```

- GDALのMBTilesドライバが内部でズームレベルを自動決定し、EPSG:3857への変換も必要なら自動で行います(GDAL公式ドキュメント記載の標準的な使い方です)
- `gdaladdo`のオーバービュー係数はズーム1段につき2倍のため、最大ズームからmin-z 8まで届かせるには`2 4 8 16 32 64`(6段階)が必要です

**既知の不具合2: `bounds`/`minzoom`/`maxzoom`メタデータが書き込まれない**

上記の手順で生成した`terrain.mbtiles`は、タイルデータ自体は正しい位置に格納されるものの、`bounds`/`center`/`minzoom`/`maxzoom`のメタデータが書き込まれないことが確認されています(`gdal_translate -of MBTILES`が書き込む値を、後段の`gdaladdo`のopen/close処理が確定させないためとみられますが未確証)。この状態で`pmtiles convert`すると、`pmtiles show`で`bounds`が全世界(`-180,-85` - `180,85`)、`center`が(0, 0)になります。タイル自体(tile_column/tile_row)は正しいので、メタデータのみ手当てすれば直ります。

```sh
sqlite3 terrain.mbtiles <<'EOF'
INSERT OR REPLACE INTO metadata (name, value) VALUES ('bounds', '131.250000,33.974981,131.262486,33.991667');
INSERT OR REPLACE INTO metadata (name, value) VALUES ('center', '131.256243,33.983324,8');
INSERT OR REPLACE INTO metadata (name, value) VALUES ('minzoom', '8');
INSERT OR REPLACE INTO metadata (name, value) VALUES ('maxzoom', '14');
EOF
```

boundsの数値は対象データのコーナー座標(度単位、西端経度,南端緯度,東端経度,北端緯度)に置き換えてください。手当て後、`pmtiles convert`をやり直せば`pmtiles show`のbounds/centerが正しい値になります。

診断のコツ: `bounds`が入っているか確認するには`sqlite3 terrain.mbtiles "select name, value from metadata;"`、タイル自体の位置が正しいかは`sqlite3 terrain.mbtiles "select zoom_level, tile_column, tile_row from tiles order by zoom_level limit 20;"`で切り分けられます。前者だけ欠けていれば上記の手当てで直ります。

### 経路2: gdal2tilesでタイルディレクトリ化する(PMTiles化しない場合)

```sh
gdal2tiles.py --xyz -z 8-14 -r bilinear terrain_rgb.tif tiles/
```

- 出力は`tiles/{z}/{x}/{y}.png`というディレクトリで、mbtilesではありません
- `pmtiles convert`はmbtiles入力を前提とするため、**このディレクトリのままでは05に進めません**
- そのままNginxに置いて`{z}/{x}/{y}.png`として配信する使い方(PMTiles化しない構成)であればこれで完結します。PMTiles化するなら経路1を使ってください

---

前: [03. COG化と検証](../03_cog/) ｜ 次: [05. PMTiles化と配信](../05_tiles_pmtiles/)