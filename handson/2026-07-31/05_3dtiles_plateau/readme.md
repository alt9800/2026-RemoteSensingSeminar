# 05_3dtiles_plateau：PLATEAU 3D Tilesを地形の上に重ねる（発展・持ち帰り）

第4回で扱った3D Tilesを、今回の地形と同じ画面に載せます。建物（PLATEAU）と地形（自作Terrain RGB）が同一シーンで合成される構成です。

## 構成

MapLibreとdeck.glをinterleaved（同一WebGLコンテキスト）で重ねます。

```html
<script src="https://unpkg.com/deck.gl@9/dist.min.js"></script>
```

```js
// MapLibre側は 01_terrain3d と同じ（terrain有効）
const overlay = new deck.MapboxOverlay({
  interleaved: true,
  layers: [
    new deck.Tile3DLayer({
      id: "plateau-bldg",
      data: PLATEAU_TILESET_URL,   // 対象都市のtileset.json
      loader: Tiles3DLoader
    })
  ]
});
map.addControl(overlay);
```

`PLATEAU_TILESET_URL` は当日案内します（対象都市の3D Tiles配信URL。PLATEAUの配信サービスから該当都市の建物モデルのtileset.jsonを指定します）。

## 観察するポイント

- 建物が地面から浮く・沈む場合、標高基準（楕円体高／標高）や地形データの解像度差が原因になり得ます。第5回のジオイドの話が実物で確認できる箇所です
- PLATEAU建物モデルには高さ属性（LOD1の押し出し元）があり、地形の高さとは独立に定義されています。「建物の高さ」と「地面の高さ」が別のデータソースから来ていることを意識してください

## Cesiumで見たい場合

CesiumJSはPLATEAU 3D Tilesをそのまま読めますが、地形はquantized-mesh形式が必要です。自作Terrain RGBタイルは使えないため、Cesium World TerrainまたはRe:earth Terrain（第5回参照）と組み合わせることになります。第4回のCesium環境がある方はそちらでも試せます。
