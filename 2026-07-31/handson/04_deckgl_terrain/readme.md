# 04_deckgl_terrain：deck.gl TerrainLayerでの実装比較（発展・持ち帰り）

同じTerrain RGBタイルをdeck.glで表示します。第4回のPointCloudLayerと同じ枠組みです。

## MapLibre版との考え方の違い

- MapLibre：`encoding: "mapbox"` と書けばデコード式は内蔵のものが使われる
- deck.gl：`elevationDecoder` に係数を自分で書く。エンコード方式の違いがコードに直接現れる

```js
new deck.TerrainLayer({
  id: "terrain",
  // TerrainLayerはURLテンプレートを取る。pmtilesプロトコルは直接渡せないため、
  // zxy形式で配信するか、pmtiles CLIのserve機能を使う（下記）
  elevationData: "http://localhost:8080/terrain/{z}/{x}/{y}.png",
  texture: "https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png",
  elevationDecoder: {
    // Mapbox Terrain-RGB: h = -10000 + (R*65536 + G*256 + B) * 0.1
    rScaler: 6553.6, gScaler: 25.6, bScaler: 0.1, offset: -10000
  },
  minZoom: 8,
  maxZoom: 14
});
```

Terrariumエンコード（Mapterhorn等）なら係数はこうなります：

```js
// h = (R*256 + G + B/256) - 32768
elevationDecoder: { rScaler: 256, gScaler: 1, bScaler: 1/256, offset: -32768 }
```

## PMTilesをzxyで配信する

deck.glのTerrainLayerに自作PMTilesを食わせる最短経路は、pmtiles CLIのローカルサーバー機能です。

```sh
pmtiles serve . --port 8080
# → http://localhost:8080/terrain/{z}/{x}/{y}.png として参照できる
# （ファイル名 terrain.pmtiles がパスの terrain に対応）
```

## どちらを選ぶか

- 地図として地形を見たい、スマホで軽く動かしたい → MapLibre
- 点群・解析メッシュ・独自レイヤーと同一シーンで合成したい → deck.gl
- Cesiumでの利用が要件 → ラスタータイルではなくquantized-mesh（第5回のRe:earth Terrain参照）。Terrain RGBからの直接変換は一般的でないため、配信元の選択から設計する
