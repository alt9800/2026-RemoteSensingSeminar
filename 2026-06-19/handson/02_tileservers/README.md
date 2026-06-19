# タイルサーバー比較

タイルサーバーのインストール用の便利帳です。

---

## Martin（Rust製）

### インストール

```bash
# macOS
brew install martin

# Linux / WSL
# GitHub Releases からバイナリをDL
curl -L https://github.com/maplibre/martin/releases/latest/download/martin-x86_64-unknown-linux-gnu.tar.gz \
  | tar xz
sudo mv martin /usr/local/bin/

# Rust 環境がある場合（全OS共通）
cargo install martin
```

### PMTiles を配信する

```bash
martin fude.pmtiles
# → http://localhost:3000/fude/{z}/{x}/{y}
```

設定ファイルを使う場合：

```bash
martin --config martin.yml
```

→ `martin.yml` の内容は同ディレクトリを参照。

### MapLibre からの接続

```js
map.addSource('fude', {
  type: 'vector',
  tiles: ['http://localhost:3000/fude/{z}/{x}/{y}']
});
```

### PostGIS と組み合わせる場合

```yaml
# martin.yml
postgres:
  connection_string: postgresql://user:pass@localhost/gisdb
  tables:
    fude:
      schema: public
      table: fude_polygon
      srid: 4326
      geometry_column: geom
```

```bash
martin --config martin.yml
# → http://localhost:3000/fude/{z}/{x}/{y}
```

---

## tileserver-gl（Node.js製）

サーバーサイドレンダリング（ラスタータイルの動的生成）が必要な場合に使う。

### インストール

```bash
npm install -g tileserver-gl
```

### 起動

```bash
tileserver-gl fude.mbtiles
# → http://localhost:8080
```

`.pmtiles` を直接渡す場合も同様。Web UI でタイルのプレビューができる。

---

## GeoServer（Java製 / 参考）

OGC 標準（WMS / WFS / WMTS）への準拠が必要な場合のみ検討する。

```bash
# Docker で起動（最も手軽）
docker run -p 8080:8080 docker.osgeo.org/geoserver:2.25.x
# → http://localhost:8080/geoserver/web/
```

WMTS の URL 例：

```
http://localhost:8080/geoserver/gwc/service/wmts
  ?SERVICE=WMTS&REQUEST=GetTile
  &LAYER=cite:fude
  &TILEMATRIXSET=EPSG:3857
  &TILEMATRIX=EPSG:3857:14
  &TILEROW=6461&TILECOL=14552
  &FORMAT=application/vnd.mapbox-vector-tile
```

Martin の `/z/x/y` と比較すると URL の複雑さが分かりやすい。

---

## まとめ：どれを選ぶか

| 状況 | 選択 |
|---|---|
| PMTiles を静的配信するだけ | Nginx（第2回で扱う）|
| PostGIS のデータをリアルタイム配信したい | Martin |
| ラスタータイルを動的に生成したい | tileserver-gl |
| OGC 標準準拠が必要 | GeoServer |
| とりあえず確認したい（SaaS） | MapTiler Cloud |