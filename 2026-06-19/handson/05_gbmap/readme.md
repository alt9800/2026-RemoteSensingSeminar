# GBMap 開発ノウハウ

Game Boy 風ラスタータイルを OSM データから生成するパイプラインの記録。

デモ：https://alt9800.github.io/sample-maps/etc/GB-map/

---

## 環境

- macOS (Apple Silicon)
- Python 3.x / venv (`~/.venv/gbmap`)
- osmium-tool (Homebrew)
- ライブラリ: Pillow, shapely, pyproj

```bash
brew install osmium-tool
python3 -m venv ~/.venv/gbmap
source ~/.venv/gbmap/bin/activate
pip install Pillow shapely pyproj
# fiona は GDAL 依存が重いため不使用。GeoJSON は標準 json で読む。
```

---

## データ取得

GeoFabrik から九州 PBF を取得し、福岡市領域で切り出す。

```bash
curl -L -o kyushu-latest.osm.pbf \
  https://download.geofabrik.de/asia/japan/kyushu-latest.osm.pbf

osmium extract \
  --bbox 130.2,33.4,130.7,33.8 \
  --output fukuoka.osm.pbf \
  kyushu-latest.osm.pbf
```

bbox は `lon_min,lat_min,lon_max,lat_max` の順。

---

## GeoJSON エクスポート

osmium export で way/polygon を GeoJSON に変換。fiona 不要で Python の `json` モジュールで直接読める。

```bash
cat > export.json << 'EOF'
{
  "attributes": {
    "type": false, "id": false, "version": false,
    "timestamp": false, "uid": false, "user": false, "changeset": false
  },
  "linear_tags": ["highway", "railway", "waterway", "name"],
  "area_tags": ["building", "landuse", "leisure", "natural", "amenity"]
}
EOF

osmium export \
  --geometry-types=linestring,polygon \
  --config=export.json \
  --output=fukuoka.geojson \
  fukuoka.osm.pbf
```

出力サイズの目安: 福岡市エリアで約 230MB。

---

## タイル座標計算

```python
import math

def deg2tile(lat, lon, zoom):
    n = 2 ** zoom
    x = int((lon + 180) / 360 * n)
    y = int((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n)
    return x, y

def tile2bbox(x, y, z):
    n = 2 ** z
    lon_min = x / n * 360 - 180
    lon_max = (x+1) / n * 360 - 180
    lat_max = math.degrees(math.atan(math.sinh(math.pi * (1 - 2*y/n))))
    lat_min = math.degrees(math.atan(math.sinh(math.pi * (1 - 2*(y+1)/n))))
    return lon_min, lat_min, lon_max, lat_max
```

福岡市中心エリア (zoom=14) の範囲:

```
x: 14119 ~ 14138  (20 tiles)
y: 6558  ~ 6574   (17 tiles)
total: 340 tiles
```

---

## レイヤー設計と色割り当て

4色制約（Game Boy Original パレット）でレイヤーを割り当てる。

| レイヤー | OSM タグ | 色 | 備考 |
|---|---|---|---|
| 陸地 (background) | — | c0 `#9bbc0f` | ベース |
| 森林 | `landuse=forest/wood`, `natural=wood` | c1 `#8bac0f` | fill |
| 公園・緑地 | `leisure=park`, `landuse=grass` 等 | c1 | 森林と同色 |
| 海・湖 | `natural=water`, `waterway=dock` | c3 `#0f380f` | fill |
| 川 | `waterway=river/stream/canal` | c3 | line、幅を river/stream で分ける |
| 建物 | `building=*` | c2 `#306230` fill + c3 outline | |
| 道路 highway | `highway=motorway/trunk/primary/secondary` | c3 casing + c1 fill | 二重ライン |
| 道路 street | `highway=tertiary/residential/unclassified` 等 | c2 | 細ライン |
| 鉄道 | `railway=rail/subway/tram` | c3 base + c0 zebra dash | ゼブライン |

車道のみ対象（`footway` / `path` / `cycleway` は除外）。

### パレットバリエーション

| 名称 | c0 | c1 | c2 | c3 |
|---|---|---|---|---|
| Game Boy | `#9bbc0f` | `#8bac0f` | `#306230` | `#0f380f` |
| GB Pocket | `#c4cfa1` | `#a9b389` | `#4d6a45` | `#1a2e1a` |
| GB Light  | `#d0f0a0` | `#a8d070` | `#308050` | `#083028` |
| CGB Green | `#b4d893` | `#82b54b` | `#3e7a1f` | `#0e3600` |

---

## タイル生成スクリプトの要点

### STRtree で空間インデックス

230MB の GeoJSON を毎タイルごとにフルスキャンすると遅い。shapely の `STRtree` でインデックスを構築してからタイル bbox で `query()` する。

```python
from shapely.strtree import STRtree
tree = STRtree(geom_list)
hits = tree.query(tile_box)  # index の配列が返る
```

### レイヤーの描画順

```
水域ポリゴン → 森林/公園ポリゴン → 建物ポリゴン
→ 水域ライン → 道路（major casing → major fill → minor）→ 鉄道
```

### 鉄道ゼブラライン

c3 の太いソリッドラインに c0 の短いセグメントを交互に重ねる。

```python
# 下地
draw.line(pts, fill=C3, width=4)
# zebra
for j in range(len(pts)-1):
    x1,y1 = pts[j]; x2,y2 = pts[j+1]
    steps = max(1, int(math.hypot(x2-x1,y2-y1) / 6))
    for s in range(steps):
        if s % 2 == 0:
            ax = x1+(x2-x1)*s/steps;     ay = y1+(y2-y1)*s/steps
            bx = x1+(x2-x1)*(s+1)/steps; by = y1+(y2-y1)*(s+1)/steps
            draw.line([(ax,ay),(bx,by)], fill=C0, width=2)
```

### タイル出力

```python
out_dir = f"tiles/{ZOOM}/{tx}"
os.makedirs(out_dir, exist_ok=True)
img.save(f"{out_dir}/{ty}.png")
```

XYZ スキーマ (`z/x/y.png`) で出力すると MapLibre / Leaflet の `tileUrl` にそのまま対応できる。

---

## HTML ビューア

CSS Grid でタイルを並べる。`image-rendering: pixelated` が必須。

```html
<style>
#map {
  display: grid;
  grid-template-columns: repeat(20, 256px);
  grid-template-rows: repeat(17, 256px);
}
#map img {
  width: 256px; height: 256px;
  image-rendering: pixelated;
  image-rendering: crisp-edges;
}
</style>
```

`file://` だとブラウザのセキュリティポリシーで画像読み込みが制限される場合があるため、ローカルサーバーで確認する。

```bash
python3 -m http.server 8000
```

---

## ディザリング

4色制約の中でエッジの中間調を表現する手法。森林エッジ・海岸線で効果的。

Bayer 4×4 マトリクスを使った ordered dithering:

```python
BAYER4 = [
  [ 0, 8, 2,10],
  [12, 4,14, 6],
  [ 3,11, 1, 9],
  [15, 7,13, 5]
]
threshold = (BAYER4[y % 4][x % 4] + 0.5) / 16
color = colorA if ratio < threshold else colorB
```

---

## Git 管理

リポジトリに含めるもの・含めないもの。

```
# 含める
index.html
generate_tiles.py
tile_range.py
export.json
tiles/          # 生成済みタイル (340枚, ~数十MB)
README.md

# .gitignore に追加
*.pbf
*.geojson
```

PBF・GeoJSON は再生成可能なため除外。タイルは生成物だが軽量のため含める。

---

## 今後の課題

- ズームレベル 15/16 への対応（建物・道路の密度増加への対処）
- Game Boy 筐体 UI（D-pad パン、A ボタンパレット切替、select でディザ ON/OFF）との統合
- MapLibre GL JS への移行（ラスタータイルソースとして読み込む）
- PMTiles 形式へのパッケージング