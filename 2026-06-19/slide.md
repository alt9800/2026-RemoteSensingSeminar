---
marp: true
theme: default
header: "衛星データ解析技術研究会<br>技術セミナー（応用編）第一回 2026/06/19"
footer: "第1回：タイル配信①：データ構造とパース"

paginate: true

style: |
    section.title {
        justify-content: center;
        text-align: center;
    }
    .round-icon {
      position: absolute;
      top: 50px;
      right: 50px;
      width: 400px;
      height: 400px;
      border-radius: 20%;
      object-fit: cover;
      z-index: 10;
    }
    .tiny-text {
      font-size: 0.6em;
    }
    /* 画像グリッド用 */
    .grid-4 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 20px;
      height: 70%;
    }
    .grid-4 > p {
      margin: 0;
      height: 100%;
    }
    .grid-4 img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }


---
---
## 衛星データ解析技術研究会<br>技術セミナー（応用編）
### Webアプリケーションの開発技術の習得

# 第1回：タイル配信①：データ構造とパース

第一回 2026/06/19

担当講師 : 田中聡至

---

## 本日のテーマ

第1回：タイル配信①：データ構造とパース

1. ガイダンス（全6回の位置づけ、到達目標の確認）
1. WebGISタイル配信エコシステムの概論
1. ラスタータイルとベクタータイル（MVT/PMTiles）の違い
1. タイルサーバー比較環境の構築・起動
1. タイルピラミッド／XYZ・TMS・WMTSの仕組み
1. GISレンダリングエンジンのタイル読み込み処理を読む
1. ハンズオン：tippecanoeによるMVT生成
1. まとめ・次回への接続

---


## 大まかな予定

| 時間 | 項目 |
|---|---|
| 0:00–0:05 | ガイダンス |
| 0:05–0:20 | WebGISタイル配信エコシステムの概論 |
| 0:20–0:35 | タイルピラミッド・座標系・リクエストの仕組み |
| 0:35–0:50 | ラスタータイルとベクタータイルの違い |
| 0:50–1:00 | 中休み |
| 1:00–1:25 | タイルサーバー比較（GeoServer / Martin / SaaS） |
| 1:25–1:45 | GISレンダリングエンジンのタイル処理を読む |
| 1:45–2:20 | ハンズオン：tippecanoeでMVT/PMTiles生成 → MapLibre確認 |
| 2:20–2:30 | まとめ・次回への接続 |

---

## 0:05–0:20　WebGISタイル配信エコシステムの概論

### 現代のWebGISが前提とするもの

地図を「画像を表示する」仕組みから「データとして扱う」仕組みに転換したのがタイル配信という設計思想の核心。

- ブラウザが地図を表示する際、全データを一括取得するのではなく、表示範囲・ズームレベルに応じた断片（タイル）を逐次取得する
- これによって大量の地物データが扱えるようになった

### FOSSとエコシステムの位置づけ

| 区分 | 代表例 | 備考 |
|---|---|---|
| レンダリングエンジン | MapLibre GL JS、OpenLayers、Leaflet | 本講義の主軸はMapLibre |
| タイルサーバー | Martin、GeoServer、tileserver-gl | 後述 |
| データ変換 | GDAL、tippecanoe | コマンドラインツール |
| SaaS | MapTiler Cloud、Mapbox | 料金・ロックインの観点で比較 |

OSGeo / FOSS4Gという国際コミュニティが上記ツール群の多くを支えている背景も触れる。

---

## 0:20–0:35　タイルピラミッド・座標系・リクエストの仕組み

### タイルピラミッドとは

ズームレベル0では世界全体が1枚のタイル。  
ズームレベルが1上がるごとにタイル数は4倍になる（各辺が2分割される）。

```
ズームレベル 0  : 1タイル（世界全体）
ズームレベル 1  : 4タイル
ズームレベル 10 : 約100万タイル
ズームレベル 17 : 約170億タイル（農地区画レベル）
```

### タイルのアドレス指定

`/z/x/y` という3つの整数でタイルを一意に特定する。

```
例：東京駅付近・ズーム17
https://example.com/tiles/17/116561/51781.pbf
```

### XYZ / TMS / WMTS の違い

| 規格 | Y軸の向き | 主な用途 |
|---|---|---|
| XYZ（Slippy Map） | 北が0 | MapLibre・Leafletのデフォルト |
| TMS | 南が0（反転） | 古い実装・GDALの出力デフォルト |
| WMTS | OGC標準、パラメータが多い | GISサーバー系との互換 |

MapLibreはXYZ基準。gdal2tilesのデフォルトはTMSなので**変換時に注意が必要**。

### 座標系の整理

タイル配信では基本的に**EPSG:3857（Web Mercator）** でタイルを切り、  
**EPSG:4326（WGS84）** で地物の座標を保持する。

日本の公的データに多い**JGD2011（EPSG:6668）** はそのままでは使えないため、  
`ogr2ogr -t_srs EPSG:4326` で変換する必要がある（ハンズオンで実施）。

---

## 0:35–0:50　ラスタータイルとベクタータイルの違い

### ラスタータイル

- PNG/JPEG 画像のタイル
- ズームレベルごとに事前レンダリング済み
- クライアントは「受け取って並べるだけ」
- スタイルの変更は不可（再生成が必要）

### ベクタータイル（MVT: Mapbox Vector Tile）

- 地物の形状・属性を**バイナリ（protobuf）** でエンコードしたタイル
- クライアント側（ブラウザ・GPU）でレンダリング
- スタイルはクライアント側で自由に変更可能
- ズームを跨いだ滑らかな描画ができる

### protobuf の構造（概観）

MVTは `.proto` スキーマで定義されたバイナリ形式。  
layer → feature → geometry / attributes の階層で格納される。

```
MVT ファイル（バイナリ）
└── layer: "buildings"
    ├── feature (geometry: Polygon, props: {height: 20})
    ├── feature (geometry: Polygon, props: {height: 35})
    └── ...
```

人間が読める形にデコードする方法は後述（ハンズオン内で確認）。

### PMTiles とは

複数タイルを**1ファイルにアーカイブ**した形式。  
Range Request（HTTP 206）でブラウザが必要なタイルだけを取得できるため、  
タイルサーバーを立てなくても静的ファイルとして配信できる。

```
my_data.pmtiles
├── ヘッダー（インデックス）
├── タイル (z=10, x=..., y=...) のバイナリ
├── タイル (z=11, x=..., y=...) のバイナリ
└── ...（全ズームレベルのタイルが1ファイルに）
```

---

## 1:00–1:25　タイルサーバー比較

### 比較の視点

- 起動の簡便さ
- PMTiles対応の有無
- パフォーマンス特性
- 運用コスト・依存関係

### オーソドックス：GeoServer

- Java製、OGC標準（WMS/WFS/WMTS）に厚く対応
- GUIで設定できる分、重く起動が遅い
- エンタープライズGIS環境との互換が必要な場面では選択肢に入る
- PMTilesの直接配信は不可

**実演**：起動して `/geoserver/web/` を確認。リクエストがどのようなURLになるかをNetworkタブで観察。

### モダン：Martin（Rust製）

- シングルバイナリで起動
- PostGIS・MBTiles・PMTilesに対応
- Rustによる高スループット
- 設定はYAML1ファイルで完結

```bash
# インストール（macOS/Linux）
brew install martin
# または
cargo install martin

# PMTilesを配信
martin my_data.pmtiles
# → http://localhost:3000/my_data/{z}/{x}/{y}
```

**実演**：後述ハンズオンで生成したPMTilesをMartinで配信し、MapLibreから接続。

### モダン（補足）：tileserver-gl

- Node.js製
- MapLibre GL Nativeを使ったサーバーサイドレンダリングが可能
- `.mbtiles` や `.pmtiles` の配信に対応
- Martinより重いが、ラスタータイルの動的生成ができる

### SaaS：MapTiler Cloud / Mapbox

| | MapTiler Cloud | Mapbox |
|---|---|---|
| 無料枠 | あり（月100万リクエスト程度） | あり（月5万MAU相当） |
| 料金発生条件 | リクエスト数超過 | MAU超過 |
| ロックインリスク | 中（APIキー依存） | 高（独自仕様が多い） |
| 自前データ投入 | 可 | 可（有償プランで） |

**整理**：SaaSは「すぐ動く」が、データの流れとコストが不透明になりやすい。  
本講義では「自分たちのデータを自分たちで配信できる」状態を目標とする。

---

## 1:25–1:45　GISレンダリングエンジンのタイル処理を読む

### MapLibre GL JSがタイルを処理する流れ

```
1. スタイルJSON読み込み → sourceのURLを確認
2. 現在のviewport + zoomから必要なタイル座標(z/x/y)を計算
3. タイルURLにリクエスト（XHRまたはFetch）
4. 受け取ったprotobuf（MVT）をデコード
5. WebGLにジオメトリを転送してGPUでレンダリング
```

### MapLibreが内部で使っているもの

- タイルのスライシング：`geojson-vt`（GeoJSON sourceを使う場合）
- protobufのデコード：`@mapbox/vector-tile` + `pbf`
- レンダリング：WebGL

### GeoJSON sourceとvector sourceの違い（重要）

**GeoJSON source**を使う場合、MapLibreは受け取ったGeoJSONを  
内部で `geojson-vt` によってタイルに変換してからレンダリングする。  
つまり**クライアントがタイル変換のコストを負担する**。

フィーチャー数が10万オーダーを超えると、この変換処理がボトルネックになる。  
（ネットワーク転送が完了してもブラウザがフリーズするか、タイムアウトで描画されない。）

> **実例**：地番ポリゴン（約11万フィーチャー）をConoHaレンタルサーバー上の  
> GeoJSONから直接読み込んだところ、データは到達しているのに描画されない事象が発生。  
> DevToolsのMemoryタブではメモリ展開済みだったことから、  
> MapLibre内部の変換処理がCPUボトルネックになっていたと判断。  
> PMTilesに変換したところ解決した。

**vector source（PMTiles/MVT）** を使う場合は、タイル変換済みのバイナリを  
直接デコードしてGPUに渡すため、上記のボトルネックが発生しない。

### MapLibreとOpenLayersの処理方式の比較

| | MapLibre GL JS | OpenLayers |
|---|---|---|
| レンダリング | WebGL（GPU） | Canvas 2D / WebGL混在 |
| MVT対応 | ネイティブ | プラグイン（ol-mapbox-style等） |
| スタイル定義 | MapLibre Style Spec（JSON） | 独自API |
| 適したケース | 大量データ・スムーズな操作 | OGC標準との統合重視 |

---

## 1:45–2:20　ハンズオン：tippecanoeでMVT/PMTiles生成 → MapLibre確認

### 使用データ

農林水産省「農業用地利用状況調査（筆ポリゴン）」  
https://open.fude.maff.go.jp/  
→ 山口県または任意の都道府県のShapefileをDL

大量ポリゴンのリアルなケースとして扱いやすく、  
「GeoJSONで直接読むとどうなるか → PMTilesにするとどうなるか」を  
体感できるデータ量（山口県で数十万フィーチャー程度）。

### Step 1：座標変換

筆ポリゴンはJGD2011（EPSG:6668）で配布されているため、WGS84に変換する。

```bash
ogr2ogr \
  -f GeoJSON fude.geojson \
  ダウンロードした.shp \
  -t_srs EPSG:4326
```

### Step 2：tippecanoeでPMTiles生成

```bash
tippecanoe \
  -o fude.pmtiles \
  --force \
  -z 17 -Z 10 \
  --drop-densest-as-needed \
  -l fude \
  fude.geojson
```

**オプション解説**

| オプション | 意味 |
|---|---|
| `-z 17` | 最大ズームレベル17（農地区画の精度に合わせる） |
| `-Z 10` | 最小ズームレベル10（これより引くと何も表示しない） |
| `--drop-densest-as-needed` | タイルサイズ超過時にフィーチャーを自動間引き |
| `-l fude` | source-layer名の指定（MapLibre側で参照する） |

### Step 3：MapLibreで表示

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/maplibre-gl/dist/maplibre-gl.css" />
  <script src="https://unpkg.com/maplibre-gl/dist/maplibre-gl.js"></script>
  <script src="https://unpkg.com/pmtiles@2/dist/index.js"></script>
  <style>
    body { margin: 0; }
    #map { width: 100vw; height: 100vh; }
  </style>
</head>
<body>
  <div id="map"></div>
  <script>
    // PMTilesプロトコルを登録
    const protocol = new pmtiles.Protocol();
    maplibregl.addProtocol('pmtiles', protocol.tile);

    const map = new maplibregl.Map({
      container: 'map',
      style: {
        version: 8,
        sources: {
          'osm': {
            type: 'raster',
            tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
            tileSize: 256
          },
          'fude': {
            type: 'vector',
            url: 'pmtiles://./fude.pmtiles'
          }
        },
        layers: [
          { id: 'osm', type: 'raster', source: 'osm' },
          {
            id: 'fude-fill',
            type: 'fill',
            source: 'fude',
            'source-layer': 'fude',
            paint: {
              'fill-color': '#6ab04c',
              'fill-opacity': 0.5,
              'fill-outline-color': '#2d6a4f'
            }
          }
        ]
      },
      center: [131.4, 34.1],  // 山口県付近
      zoom: 12
    });
  </script>
</body>
</html>
```

### 確認ポイント

- GeoJSON sourceに切り替えるとどうなるか（体感してみる）
- DevToolsのNetworkタブで `/z/x/y` へのリクエストを観察
- ズームイン・アウト時にリクエストが発生するタイミング

### Before / After

| | GeoJSON直読み | PMTiles |
|---|---|---|
| 初期ロード | 全量転送・メモリ展開 | 表示範囲のタイルのみ取得 |
| MapLibre処理 | geojson-vtによる変換コスト（全フィーチャー） | タイル単位でインクリメンタル |
| ファイルサイズ | 数百MB（圧縮前） | tippecanoeが自動間引き |
| ホスティング | 単ファイルだが重い | Range Requestで部分取得可 |
| タイルサーバー | 不要 | 不要（PMTilesなら静的配信可） |

---

## 2:20–2:30　まとめ・次回への接続

### 今回の到達確認

- [ ] タイルピラミッドの仕組みを説明できる
- [ ] XYZ / TMS / WMTS の違いを区別できる
- [ ] MVTとPMTilesの関係を説明できる
- [ ] `tippecanoe` でPMTilesを生成できた
- [ ] MapLibreでvector sourceとして表示できた

### 次回（第2回）でやること

今回生成したPMTilesを「自前のサーバーで配信する」構成に移行する。

- Nginx による静的配信設定（CORS含む）
- Martin によるタイルサーバー起動
- Maputnik でのスタイル設計
- OSMエコシステムと外部サービスの整理

---

## 参考リンク

- [MapLibre GL JS ドキュメント](https://maplibre.org/maplibre-gl-js/docs/)
- [tippecanoe GitHub](https://github.com/felt/tippecanoe)
- [PMTiles 仕様](https://github.com/protomaps/PMTiles)
- [農林水産省 筆ポリゴンデータ](https://open.fude.maff.go.jp/)
- [Martin（Rust製タイルサーバー）](https://github.com/maplibre/martin)
- [FOSS4G コミュニティ](https://foss4g.org/)