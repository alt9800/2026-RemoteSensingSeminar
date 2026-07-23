[ハンズオン目次に戻る](../)

# 04. Terrain RGBエンコード

標高値（Float32）を、PNGの24bit（RGB）に詰め替えます。

## エンコード式（Mapbox Terrain-RGB方式）

```
height = -10000 + ((R * 256 * 256 + G * 256 + B) * 0.1)
```

- 分解能 0.1m。MapLibre / deck.gl が標準でデコードできます
- 地理院標高タイルPNGは別方式であり互換性がありません

## 実行（rio-rgbify）

```sh
rio rgbify \
  --min-z 8 --max-z 14 \
  --interval 0.1 \
  --format png \
  dem_cog.tif terrain.mbtiles
```

| オプション | 意味 |
|---|---|
| `--interval 0.1` | エンコード分解能（式の `* 0.1` に対応） |
| `--max-z 14` | 最大ズーム。10m解像度に見合う上限の目安 |
| `--format png` | 可逆圧縮必須。JPEGを選ぶと標高値が壊れます |

max-zの決め方：ズームzでの1pxの地上サイズが元データの解像度を下回っても情報は増えません。10m DEMならz14前後（緯度による）が実用上限です。

## NoData（海域・欠測）の扱い

NoData縁がノイズ状の崖として描画されることがあります。症状が出た場合：

```sh
# NoDataを標高0に置換してからエンコードする対処（海域が0mで問題ない場合）
gdal_calc.py -A dem_cog.tif --outfile=dem_filled.tif \
  --calc="numpy.where(A==-9999, 0, A)" --NoDataValue=none
```

厳密に透過させたい場合はアルファ付きの処理が必要になりますが、本日は上記の簡易対処で進めます。

## 代替手順：rio-rgbifyが動かない場合（gdal_calcによる自前エンコード）

エンコード式を逆に解くと、各チャンネルは次で求められます：

```sh
# v = (height + 10000) / 0.1 として R,G,B に分解する
gdal_calc.py -A dem_cog.tif --outfile=r.tif --type=Byte \
  --calc="((A+10000)/0.1)//65536"
gdal_calc.py -A dem_cog.tif --outfile=g.tif --type=Byte \
  --calc="(((A+10000)/0.1)%65536)//256"
gdal_calc.py -A dem_cog.tif --outfile=b.tif --type=Byte \
  --calc="((A+10000)/0.1)%256"
gdal_merge.py -separate -o terrain_rgb.tif r.tif g.tif b.tif

# タイル化はgdal2tilesで（--xyz必須。TMSとY軸が逆になるため）
gdal2tiles.py --xyz -z 8-14 -r bilinear terrain_rgb.tif tiles/
```

- gdal2tiles出力（ディレクトリ形式）は `pmtiles convert` ではなく、mb-util等でmbtiles化してからPMTiles化するか、そのままNginxに置いて `{z}/{x}/{y}.png` として配信できます
- こちらの経路は「エンコードの中身を完全に自分の手で追える」利点があります。時間があれば両方試してください

---

前: [03. COG化と検証](../03_cog/) ｜ 次: [05. PMTiles化と配信](../05_tiles_pmtiles/)
