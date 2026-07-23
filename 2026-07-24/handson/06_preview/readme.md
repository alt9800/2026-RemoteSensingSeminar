# 06. MapLibre hillshadeによる目視検証

「正しいタイルが作れたか」をhillshade（陰影起伏）表示で検証します。3D表示（terrain）は第6回で扱います。

## 手順

1. `terrain.pmtiles` をこのディレクトリの `app/` にコピー（または05の配信URLを使用）
2. `app/index.html` をローカルサーバー経由で開く

```sh
cd app
python3 -m http.server 8000
# ブラウザで http://localhost:8000/ を開く
```

file:// で直接開くとPMTilesのRange Requestが動きません。必ずローカルサーバーを経由してください。

## 検証の観点

| 見た目 | 判定 |
|---|---|
| 尾根・谷が自然な陰影で見える | 成功 |
| 全面が単色・真っ黒 | エンコード失敗またはズーム範囲外を見ている |
| 縞模様・等高線状のノイズ | エンコード方式の不一致（intervalやデコード式の確認） |
| データ縁が崖状のノイズ | NoData処理漏れ（04の対処へ） |

## index.htmlの構成

- MapLibre GL JS + pmtiles.js（第2回と同じ構成）
- `raster-dem` ソース + `hillshade` レイヤーのみの最小構成
- ソースURLは冒頭の `TERRAIN_URL` 定数で変更できます
