# 地理院地図ベクター カスタマイズメモ

第2回デモ②の参考資料。  
試行錯誤の記録として残す。実装例：https://alt9800.github.io/sample-maps/maplibre-catalog/

---

## スタイルの読み込み

```js
// 公式が公開しているスタイルJSON
const GSI_VECTOR_STYLE = 'https://gsi-cyberjapan.github.io/gsivectortile-mapbox-gl-js/std.json';

map.setStyle(GSI_VECTOR_STYLE);
```

Maputnik でこの URL を読み込むと各レイヤーを視覚的に編集できる。  
ただしスタイルJSONが大きく、レイヤー数が多いため動作が重い。

---

## ベクタータイルのソース構造

地理院ベクタータイルのソースは `openmaptiles` という ID で登録されている。  
動的にソース ID を取得する場合は以下のようにフォールバックを用意する。

```js
function getBuildingSourceId() {
  const sources = map.getStyle()?.sources || {};
  if (sources['openmaptiles']) return 'openmaptiles';
  // フォールバック：vector ソースを探す
  const found = Object.entries(sources).find(([, s]) => s.type === 'vector');
  return found ? found[0] : 'openmaptiles';
}
```

---

## 建物の押し出し（fill-extrusion）

### ハマりポイント

- プロパティ名が `height` / `min_height` ではなく **`render_height` / `render_min_height`**
- `hide_3d: true` が付いたフィーチャー（輪郭ポリゴン）を除外しないと二重押し出しになる
- `extrude` 属性は Mapbox 独自で OpenMapTiles スキーマには存在しない

```js
map.addLayer({
  id: 'buildings-3d',
  type: 'fill-extrusion',
  source: getBuildingSourceId(),
  'source-layer': 'building',
  minzoom: 13,
  filter: ['!', ['to-boolean', ['get', 'hide_3d']]],  // 輪郭ポリゴンを除外
  paint: {
    'fill-extrusion-color': '#c0bdb8',
    'fill-extrusion-height': [
      'interpolate', ['linear'], ['zoom'],
      13, 0, 16, ['coalesce', ['get', 'render_height'], 5]
    ],
    'fill-extrusion-base': [
      'interpolate', ['linear'], ['zoom'],
      13, 0, 16, ['coalesce', ['get', 'render_min_height'], 0]
    ],
    'fill-extrusion-opacity': 0.85
  }
});
```

---

## スタイル切り替え後の処理タイミング

`setStyle()` の後にソース・レイヤーを追加する場合、`styledata` では早すぎてソースが未確定のことがある。`idle` を使うと全タイル読み込み完了後に確実に処理できる。

```js
map.setStyle(newStyle);
map.once('idle', () => {
  // ここでソースやレイヤーを追加する
});
```

---

## 地形（terrain）との組み合わせ

MapLibre の `fill-extrusion` は terrain に対して自動でドレープしない。  
terrain 有効時に建物が地形に埋まる・浮くことがある。平地の都市部では許容範囲。

terrain に使用している DEM：Mapterhorn（terrarium エンコード・PMTiles 配信）

```js
map.addSource('terrain-src', {
  type: 'raster-dem',
  tiles: ['mapterhorn://{z}/{x}/{y}'],
  encoding: 'terrarium',
  tileSize: 512,
  maxzoom: 14
});
map.setTerrain({ source: 'terrain-src', exaggeration: 1.2 });
```

Mapterhorn は z14 までしか実データがないため、z15 以上のリクエストはクランプが必要。

---

## Maputnik での編集について

地理院ベクタータイルのスタイルは Maputnik で開ける。  
`source-layer` の名称一覧は以下で確認できる：

- `building` — 建物
- `road` — 道路
- `landuse` — 土地利用
- `boundary` — 行政境界
- `label` — ラベル（地名など）

フィルター式や paint プロパティの変更は Maputnik 上でリアルタイムに確認しながら作業できる。  
編集結果は JSON でエクスポートして `map.setStyle()` に渡す。