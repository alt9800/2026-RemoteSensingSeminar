# 03. COG化と検証

## COGとは（復習）

通常のGeoTIFFと100%互換のまま、内部レイアウトを規約化してHTTP Range Requestで部分読み出しできるようにしたものです。第2回のPMTilesと同じ「静的ファイル + Range」の設計思想です。

## 実行

```sh
rio cogeo create dem_10m.tif dem_cog.tif
rio cogeo validate dem_cog.tif
```

`validate` が valid である旨を返せば成功です。

## GDAL単体でやる場合（rio-cogeoが使えない環境向け）

```sh
gdal_translate dem_10m.tif dem_cog.tif -of COG -co COMPRESS=DEFLATE
```

GDAL 3.1以降はCOGドライバを内蔵しています。オーバービューも自動生成されます。

## 中身の変化を確認する

```sh
gdalinfo dem_cog.tif
```

変換前と比べて増えているもの：

```
Overviews: 2250x1875, 1125x938, ...   <- 縮小版ピラミッドが内蔵された
Band 1 Block=512x512                  <- ストリップから内部タイルに変わった
```

## この時点でできること

`dem_cog.tif` をNginx（第2回構成）に置けば、対応クライアントから直接読めます。タイル化せずCOG直読みで済むケースもあります（第6回で比較します）。

`dem_cog.tif` は第6回でも使用します。保管してください。
