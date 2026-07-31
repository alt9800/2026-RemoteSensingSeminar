# 02_mapterhorn_compare：Mapterhornとの比較

第5回で紹介したMapterhorn（全球のオープン地形タイル）をソースとして差し替え、自作タイルと見比べます。

## 手順

`01_terrain3d/index.html` をコピーし、`terrainSource` を以下に差し替えます。

```js
terrainSource: {
  type: "raster-dem",
  tiles: ["https://tiles.mapterhorn.com/{z}/{x}/{y}.webp"],
  encoding: "terrarium",   // Mapbox方式ではない
  tileSize: 512            // 512pxタイル。256のままだと標高が破綻する
}
```

変更点は3箇所です：`tiles`（URLテンプレート指定に変更）、`encoding`、`tileSize`。`minzoom` / `maxzoom` の行は削除して構いません。

## 観察するポイント

1. **解像度の差**：同じ谷・溜池の堤体を、自作タイル（1m/10m由来）とMapterhorn（日本域は現状Copernicus 30m相当）で見比べる。堤防・切土盛土など人工地形の輪郭で差が最もよく出ます
2. **エンコード方式**：`encoding` を `mapbox` のまま、または `tileSize` を256のままにして、何が起きるかを一度見ておく。壊れ方を知っていると、実務で他人のタイルを扱うときの切り分けが速くなります
3. **配信形態**：MapterhornはPMTilesアーカイブとzxyエンドポイントの両方を提供しています。`pmtiles extract --bbox=...` で必要範囲だけ切り出して自前ホストもできます（`06_offline_design` 参照）

## Terrariumエンコードのデコード式（参考）

```
標高 = (R * 256 + G + B / 256) - 32768
```

Mapbox方式とは別物です。クリック標高機能を移植する場合はこの式に書き換える必要があります。
