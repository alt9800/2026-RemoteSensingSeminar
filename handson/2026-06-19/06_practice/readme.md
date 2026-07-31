# タイル読み込みリファレンス

MapLibre GL JS / Leaflet / deck.gl / CesiumJS それぞれのタイル読み込み方法をまとめる。

---

## 目次

- [MapLibre GL JS](#maplibre-gl-js)
- [Leaflet V1](#leaflet-v1)
- [Leaflet V2](#leaflet-v2)
- [deck.gl](#deckgl)
- [CesiumJS](#cesiumjs)
- [ライブラリ比較](#ライブラリ比較)

---

## MapLibre GL JS

WebGL ベース。ベクタータイルのネイティブサポートが最も充実している。

### ラスタータイル

```html
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl/dist/maplibre-gl.css" />
<script src="https://unpkg.com/maplibre-gl/dist/maplibre-gl.js"></script>
```

```js
const map = new maplibregl.Map({
  container: 'map',
  style: {
    version: 8,
    sources: {
      osm: {
        type: 'raster',
        tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
        tileSize: 256,
        attribution: '© OpenStreetMap contributors'
      }
    },
    layers: [{ id: 'osm', type: 'raster', source: 'osm' }]
  },
  center: [135.5, 34.7],
  zoom: 10
});
```

### ベクタータイル（MVT）

```js
sources: {
  tiles: {
    type: 'vector',
    tiles: ['https://example.com/tiles/{z}/{x}/{y}.pbf'],
    minzoom: 0,
    maxzoom: 14
  }
},
layers: [
  {
    id: 'buildings',
    type: 'fill',
    source: 'tiles',
    'source-layer': 'building',   // tippecanoe の -l に対応
    paint: { 'fill-color': '#aaa', 'fill-opacity': 0.6 }
  }
]
```

### PMTiles

```html
<script src="https://unpkg.com/pmtiles@2/dist/index.js"></script>
```

```js
// プロトコル登録（map 初期化より前に行う）
const protocol = new pmtiles.Protocol();
maplibregl.addProtocol('pmtiles', protocol.tile);

sources: {
  fude: {
    type: 'vector',
    url: 'pmtiles://./fude.pmtiles'   // ローカルファイル
    // url: 'pmtiles://https://example.com/fude.pmtiles'  // リモート
  }
}
```

### 地理院地図ベクタータイル（スタイルJSON読み込み）

```js
const map = new maplibregl.Map({
  container: 'map',
  style: 'https://gsi-cyberjapan.github.io/gsivectortile-mapbox-gl-js/std.json',
  center: [139.767, 35.681],
  zoom: 10
});
```

---

## Leaflet V1

軽量・シンプル。v1.x 系の安定版。ベクタータイルはプラグイン依存。

### ラスタータイル

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1/dist/leaflet.js"></script>
```

```js
const map = L.map('map').setView([34.7, 135.5], 10);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
  maxZoom: 19
}).addTo(map);
```

### 複数ソースの切り替え

```js
const osm    = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png');
const gsiStd = L.tileLayer('https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png');
const gsiFoto = L.tileLayer('https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg');

L.control.layers({ OSM: osm, '地理院標準': gsiStd, '地理院写真': gsiFoto }).addTo(map);
osm.addTo(map);
```

### ベクタータイル（leaflet.vectorgrid プラグイン）

```html
<script src="https://unpkg.com/leaflet.vectorgrid/dist/Leaflet.VectorGrid.bundled.js"></script>
```

```js
L.vectorGrid.protobuf('https://example.com/tiles/{z}/{x}/{y}.pbf', {
  vectorTileLayerStyles: {
    building: { fill: true, fillColor: '#aaa', fillOpacity: 0.6, weight: 0 },
    road:     { color: '#888', weight: 1 }
  },
  maxZoom: 14,
  interactive: true
}).addTo(map);
```

### PMTiles（leaflet-pmtiles プラグイン）

```html
<script src="https://unpkg.com/pmtiles@2/dist/index.js"></script>
<script src="https://unpkg.com/leaflet-pmtiles/dist/leaflet-pmtiles.js"></script>
```

```js
const layer = new LeafletPMTiles('./fude.pmtiles', {
  style: {
    fude: { fill: true, fillColor: '#6ab04c', fillOpacity: 0.5, weight: 0.5 }
  }
});
layer.addTo(map);
```

---

## Leaflet V2

v2.x 系。ES modules 対応・IE 非サポート・Canvas レンダラー改善。コア API は v1 と互換性が高い。

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@2/dist/leaflet.css" />
<script type="module">
  import L from 'https://unpkg.com/leaflet@2/dist/leaflet-src.esm.js';

  const map = L.map('map').setView([34.7, 135.5], 10);

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);
</script>
```

### v1 との主な差異

| 項目 | v1 | v2 |
|---|---|---|
| モジュール形式 | グローバル `L` | ESM / CommonJS |
| IE サポート | あり | なし |
| Canvas レンダラー | 基本的 | 改善（パフォーマンス向上） |
| TypeScript 定義 | 別パッケージ | 同梱 |
| ベクタータイル | プラグイン依存 | プラグイン依存（変わらず） |

> ベクタータイル（VectorGrid / PMTiles）プラグインの v2 対応状況は各プラグインのリリースノートを確認すること。

---

## deck.gl

WebGL2 ベースの高性能ビジュアライゼーションライブラリ。MapLibre と組み合わせて使うことが多い。

### セットアップ（MapLibre と統合）

```html
<script src="https://unpkg.com/maplibre-gl/dist/maplibre-gl.js"></script>
<script src="https://unpkg.com/deck.gl/dist.min.js"></script>
```

```js
const map = new maplibregl.Map({
  container: 'map',
  style: { version: 8, sources: {}, layers: [] },
  center: [135.5, 34.7],
  zoom: 10
});

const deck = new deck.DeckGL({
  canvas: 'deck-canvas',         // map の上に重ねる canvas 要素
  controller: false,             // MapLibre にコントロールを任せる
  layers: []
});

// MapLibre のカメラと同期
map.on('move', () => {
  const { lng, lat } = map.getCenter();
  deck.setProps({
    viewState: {
      longitude: lng, latitude: lat,
      zoom: map.getZoom(), bearing: map.getBearing(), pitch: map.getPitch()
    }
  });
});
```

### ラスタータイル（TileLayer）

```js
import { TileLayer } from '@deck.gl/geo-layers';
import { BitmapLayer } from '@deck.gl/layers';

new TileLayer({
  data: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
  minZoom: 0, maxZoom: 19,
  tileSize: 256,
  renderSubLayers: props => new BitmapLayer(props, {
    data: null,
    image: props.data,
    bounds: [
      props.tile.bbox.west, props.tile.bbox.south,
      props.tile.bbox.east, props.tile.bbox.north
    ]
  })
})
```

### ベクタータイル（MVTLayer）

```js
import { MVTLayer } from '@deck.gl/geo-layers';

new MVTLayer({
  data: 'https://example.com/tiles/{z}/{x}/{y}.pbf',
  minZoom: 0, maxZoom: 14,
  getFillColor: [100, 180, 80, 180],
  getLineColor: [50, 100, 40],
  getLineWidth: 1,
  pickable: true,
  onClick: ({ object }) => console.log(object?.properties)
})
```

### 地形（TerrainLayer）

```js
import { TerrainLayer } from '@deck.gl/geo-layers';

new TerrainLayer({
  elevationDecoder: {
    rScaler: 6553.6,
    gScaler: 25.6,
    bScaler: 0.1,
    offset: -10000
  },
  // Terrain RGB タイル
  elevationData: 'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png',
  texture: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
  wireframe: false,
  color: [255, 255, 255]
})
```

### 3D Tiles（Tile3DLayer）

```js
import { Tile3DLayer } from '@deck.gl/geo-layers';

new Tile3DLayer({
  data: 'https://example.com/tileset.json',   // 3D Tiles の tileset.json
  onTilesetLoad: tileset => {
    // ロード完了後にカメラを合わせる
    const { cartographicCenter, zoom } = tileset;
    deck.setProps({ viewState: { ...cartographicCenter, zoom } });
  },
  pointSize: 2
})
```

---

## CesiumJS

3D 地球儀・高精度な地理座標処理が強み。3D Tiles の標準実装。

### セットアップ

```html
<script src="https://cesium.com/downloads/cesiumjs/releases/latest/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="https://cesium.com/downloads/cesiumjs/releases/latest/Build/Cesium/Widgets/widgets.css" />
```

```js
// Ion を使わない場合はトークン不要（または空文字）
Cesium.Ion.defaultAccessToken = '';

const viewer = new Cesium.Viewer('cesiumContainer', {
  imageryProvider: false,   // デフォルト Bing を無効化
  baseLayerPicker: false,
  geocoder: false
});
```

### ラスタータイル（ImageryProvider）

```js
// XYZ タイル
viewer.imageryLayers.addImageryProvider(
  new Cesium.UrlTemplateImageryProvider({
    url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    credit: '© OpenStreetMap contributors'
  })
);

// 地理院タイル
viewer.imageryLayers.addImageryProvider(
  new Cesium.UrlTemplateImageryProvider({
    url: 'https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png',
    maximumLevel: 18,
    credit: '国土地理院'
  })
);
```

### WMS

```js
viewer.imageryLayers.addImageryProvider(
  new Cesium.WebMapServiceImageryProvider({
    url: 'https://example.com/geoserver/wms',
    layers: 'workspace:layername',
    parameters: { transparent: true, format: 'image/png' }
  })
);
```

### 3D Tiles

```js
const tileset = await Cesium.Cesium3DTileset.fromUrl(
  'https://example.com/tileset.json'
);
viewer.scene.primitives.add(tileset);

// ロード後にカメラを合わせる
await viewer.zoomTo(tileset);

// スタイリング
tileset.style = new Cesium.Cesium3DTileStyle({
  color: "color('white', 0.8)",
  show: "${height} > 10"
});
```

### ベクタータイル

CesiumJS のベクタータイルネイティブサポートは限定的。
MVT を表示する場合は deck.gl と組み合わせるか、GeoJSON で読み込む方法が現実的。

```js
// GeoJSON として読み込む（小〜中規模データ向け）
const dataSource = await Cesium.GeoJsonDataSource.load('./data.geojson', {
  stroke: Cesium.Color.fromCssColorString('#028090'),
  fill: Cesium.Color.fromCssColorString('#028090').withAlpha(0.5),
  strokeWidth: 2
});
viewer.dataSources.add(dataSource);
```

### 地形（TerrainProvider）

```js
// Cesium World Terrain（Ion 必要）
const terrain = Cesium.Terrain.fromWorldTerrain();
viewer.scene.setTerrain(terrain);

// カスタム Terrain（quantized-mesh 形式）
viewer.terrainProvider = await Cesium.CesiumTerrainProvider.fromUrl(
  'https://example.com/terrain'
);
```

---

## ライブラリ比較

| | MapLibre GL JS | Leaflet v1/v2 | deck.gl | CesiumJS |
|---|---|---|---|---|
| レンダリング | WebGL | Canvas / SVG | WebGL2 | WebGL |
| ラスタータイル | ✓ | ✓ | ✓ (TileLayer) | ✓ |
| ベクタータイル（MVT） | ✓ ネイティブ | プラグイン | ✓ (MVTLayer) | 限定的 |
| PMTiles | ✓ (protocol) | プラグイン | △ | — |
| 3D Tiles | — | — | ✓ (Tile3DLayer) | ✓ ネイティブ |
| 地形（DEM） | ✓ terrain | — | ✓ (TerrainLayer) | ✓ |
| 3D 表示 | ✓ (pitch) | — | ✓ | ✓ 地球儀 |
| 学習コスト | 中 | 低 | 高 | 高 |
| バンドルサイズ | 中 | 小 | 大 | 大 |
| 主な用途 | WebGIS・カートグラフィック | シンプルな地図表示 | 大量データ可視化 | 3D・点群・宇宙 |

### 組み合わせパターン

```
MapLibre + deck.gl     → ベースマップ + 大量フィーチャー可視化
MapLibre + PMTiles     → 自前配信・静的ホスティング
CesiumJS + deck.gl     → 3D地球儀 + 高度なデータ表示
Leaflet + VectorGrid   → シンプルなベクタータイル閲覧
```

---

## 参考リンク

- [MapLibre GL JS ドキュメント](https://maplibre.org/maplibre-gl-js/docs/)
- [Leaflet ドキュメント](https://leafletjs.com/reference.html)
- [deck.gl ドキュメント](https://deck.gl/docs)
- [CesiumJS ドキュメント](https://cesium.com/learn/cesiumjs/ref-doc/)
- [PMTiles プロトコル仕様](https://github.com/protomaps/PMTiles)
- [3D Tiles 仕様](https://github.com/CesiumGS/3d-tiles)