# 08. 発展：県公開の点群からPDALでDSMを自作する

静岡（VIRTUAL SHIZUOKA）・東京（都デジタルツイン点群）・長崎（オープンナガサキ）など、都県単位で航空LiDAR点群がオープンデータ化されています。ここでは点群1タイルからDSM/DTMを作り、本編パイプラインに合流させます。

第4回の点群処理（CloudCompare / PDAL）の続きとしても読めます。

## 準備

- PDAL：`conda install -c conda-forge pdal` または各OSのパッケージ（第4回04資料参照）
- データ：G空間情報センター等から対象範囲のLAS/LAZを1タイル取得
  - 公開名称・配布形式は変更されることがあります。最新の公開ページを確認してください

## まず中身を見る

```sh
pdal info --metadata input.laz
pdal info --stats input.laz | head -50
```

- CRS（県のLiDARは平面直角座標系が多い。EPSGコードを控える）
- 分類コードが付与されているか（`Classification` の統計に2=地面があるか）

## DSMを作る（ファーストリターン + max）

`dsm.json`:

```json
{
  "pipeline": [
    "input.laz",
    { "type": "filters.range", "limits": "returnnumber[1:1]" },
    { "type": "writers.gdal",
      "filename": "dsm.tif",
      "resolution": 1.0,
      "output_type": "max",
      "nodata": -9999,
      "gdaldriver": "GTiff" }
  ]
}
```

```sh
pdal pipeline dsm.json
```

## DTMを作る（地面分類 + idw）

`dtm.json`（差分のみ）:

```json
    { "type": "filters.range", "limits": "Classification[2:2]" },
    { "type": "writers.gdal",
      "filename": "dtm.tif",
      "resolution": 1.0,
      "output_type": "idw",
      "nodata": -9999 }
```

- 分類コードが未付与のデータでは `filters.smrf`（地面点分類フィルタ）を前段に挟みます

## DSM - DTM = CSM（樹高・構造物高）

```sh
gdal_calc.py -A dsm.tif -B dtm.tif --outfile=csm.tif --calc="A-B" --NoDataValue=-9999
```

## 本編パイプラインへの合流

できあがった `dsm.tif` は本編の `dem_src.tif` と同じ扱いです。02（gdalwarp）から先をそのまま適用してください。CRSが平面直角座標系である点だけ `-s_srs` に注意します。

## 観察ポイント

- 同じ場所のDSMとDTMを06のビューアで見比べると、DSM/DTMの違い（Part 1）が視覚的に理解できます
- CSMで市街地を見ると建物高が、山林を見ると樹高が浮かび上がります
