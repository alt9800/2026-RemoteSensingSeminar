[ハンズオン目次に戻る](../)

# 07. 発展：GSI 1mメッシュDEMで山口県内を高精細化する

本編と同じパイプラインを、国土地理院が整備を進める1mメッシュDEMに適用します。対象は宇部新川駅周辺・あすとぴあ周辺です。

処理時間・容量が10m版より大きく増えます。当日中の完走は想定していません。手順を確認して自宅で試してください。

## データの入手

- 公開情報：https://www.gsi.go.jp/gazochosa/gazochosa61005.html
- 対象範囲のダウンロード方法・提供形式は上記ページおよび講師配布のリンク集を参照してください
- 提供形式がJPGIS GML（.xml）の場合、GeoTIFFへの変換が必要です（下記）

## JPGIS GML → GeoTIFF変換（形式がGMLの場合）

方法は複数あります：

1. QGIS：ラスタとして直接読み込み → GeoTIFFにエクスポート（GUIで完結。初心者向け）
2. 変換ツール：基盤地図情報標高DEMコンバータ等のコミュニティツール
3. 複数タイルの結合が必要な場合：

```sh
gdalbuildvrt merged.vrt *.tif      # 変換済みタイル群を仮想結合
gdal_translate merged.vrt dem1m_src.tif
```

## パイプラインの適用（本編との差分のみ）

```sh
# 01: 確認（CRS・NoDataは1m版で異なる可能性がある。必ず確認）
gdalinfo -stats dem1m_src.tif

# 02: 変換（-tr 1 1、範囲は対象地区に絞る）
gdalwarp -s_srs EPSG:XXXX -t_srs EPSG:3857 \
  -te <xmin> <ymin> <xmax> <ymax> -te_srs EPSG:3857 \
  -tr 1 1 -r bilinear -dstnodata -9999 \
  dem1m_src.tif dem1m_3857.tif

# 03: COG化
rio cogeo create dem1m_3857.tif dem1m_cog.tif

# 04: Terrain RGB化（max-zを16に引き上げる）
rio rgbify --min-z 10 --max-z 16 --interval 0.1 --format png \
  dem1m_cog.tif terrain1m.mbtiles

# 05: PMTiles化
pmtiles convert terrain1m.mbtiles terrain1m.pmtiles
```

## 観察ポイント（10m版との比較）

06の検証ビューアで `TERRAIN_URL` と `MAXZOOM` を差し替えて比較してください：

- 河川堤防・道路の切土盛土・ため池堤体など、人工地形の輪郭の出方
- z15〜16まで拡大したときの陰影の破綻の有無
- ファイルサイズと処理時間（10m版の記録と比較）

## なぜmax-z 16か

z16での1pxの地上サイズは中緯度で約1.7〜2.4m（緯度依存）です。1m解像度のデータに対してz17以上を作っても、タイル容量が増えるだけで情報は増えません。

---

前: [06. MapLibre hillshadeによる目視検証](../06_preview/) ｜ 次: [08. 点群からDSM（発展）](../08_pointcloud_dsm/)
