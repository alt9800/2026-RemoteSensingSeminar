# 03_hazard_viewer：NDWI・防災重点溜池を重ねたハザードビューア

`01_terrain3d` のビューアにNDWIラスターと防災重点溜池（国土数値情報）を重ね、地形と水の関係を読むためのビューアに仕上げます。完成版は同梱の `index.html` です。

## 使用データ（`00_setup` で取得）

| ファイル | 内容 |
| -------- | ---- |
| `ndwi/{z}/{x}/{y}.png` | NDWIラスタータイル（Sentinel-2由来、水域を青系で着色済み） |
| `tameike.geojson` | 防災重点溜池（山口県分、属性：名称・堤高・貯水量） |

## 実装の要点

NDWI（ラスター）の追加：

```js
map.addSource("ndwi", {
  type: "raster",
  tiles: ["../ndwi/{z}/{x}/{y}.png"],
  tileSize: 256, minzoom: 10, maxzoom: 14
});
map.addLayer({
  id: "ndwi-layer", type: "raster", source: "ndwi",
  paint: { "raster-opacity": 0.6 }
});
```

溜池（ベクター）の追加とポップアップ：

```js
map.addSource("tameike", { type: "geojson", data: "../tameike.geojson" });
map.addLayer({
  id: "tameike-pt", type: "circle", source: "tameike",
  paint: { "circle-radius": 6, "circle-color": "#B91C1C",
           "circle-stroke-color": "#fff", "circle-stroke-width": 1.5 }
});
map.on("click", "tameike-pt", (e) => {
  const p = e.features[0].properties;
  new maplibregl.Popup().setLngLat(e.lngLat)
    .setHTML(`<strong>${p.name}</strong><br>堤高: ${p.height} m<br>貯水量: ${p.volume} m³`)
    .addTo(map);
});
```

terrainが有効な状態では、rasterレイヤーは地形に沿って貼り付き、circleレイヤーは地表面の標高に配置されます。

## 読み取りの演習

1. 溜池の直下流にあたる谷筋はどこか（誇張1.5前後で確認）
2. NDWI高値域と溜池の位置関係。常時水がある谷か、乾いた谷か
3. 谷の出口に集落・農地があるか（第2回の `fude.pmtiles` を重ねてもよい）

これは現地に行く前の下見ツールです。浸水想定区域図の代替にはなりません（正式な氾濫解析は水理計算に基づきます）。また、NDWIの値には観測日・雲・解像度の影響が乗っています。

## 属性名について

`tameike.geojson` の属性キー（`name` / `height` / `volume`）は配布データの前処理で付け直したものです。国土数値情報の原本はコード体系の属性名（`W09_001` 等）なので、自分でダウンロードして使う場合は読み替えてください。
