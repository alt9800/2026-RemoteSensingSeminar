# 05. PMTiles化と配信

## 変換

```sh
pmtiles convert terrain.mbtiles terrain.pmtiles
```

## 中身の確認

```sh
pmtiles show terrain.pmtiles
```

- タイル数・ズーム範囲・フォーマット（png）を確認します
- ファイルサイズも控えておいてください（第6回の配信設計の材料になります）

## 配信

第2回のNginx構成に置くだけです。ローカル確認なら：

```sh
# terrain.pmtiles のあるディレクトリで
python3 -m http.server 8000
```

- ブラウザ側からは `http://localhost:8000/terrain.pmtiles` をRange Requestで読みます
- Nginxの場合、Rangeは標準で有効です。CORSが必要な構成（別オリジンから読む場合）は第2回資料の `add_header` 設定を参照してください

次の `06_preview` で表示検証を行います。
