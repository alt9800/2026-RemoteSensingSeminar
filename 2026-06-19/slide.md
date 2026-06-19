---
marp: true
theme: default
header: "衛星データ解析技術研究会<br>技術セミナー（応用編）第一回 2026/06/19"
footer: "第1回：タイル配信①：データ構造とパース"
paginate: true
style: |
  /* ── カラー変数 ──────────────────────────────────────────
     講義全体で使うブランドカラーを一元管理する。
     変更する場合はここだけ編集すればよい。              */
  :root {
    --navy:       #1C3A4A;   /* 見出し・テーブルヘッダー */
    --teal:       #028090;   /* アクセント・ラベル・リンク */
    --green:      #2D7D46;   /* 正例・OKの強調 */
    --red:        #B91C1C;   /* 警告・注意事項 */
    --gray:       #374151;   /* 本文グレー */
    --light:      #F8FAFB;   /* テーブル偶数行・薄い背景 */
    --teal-light: #E6F4F6;   /* h2 の下線・カード背景 */
    --brand:      #9DE371;   /* ロゴのイエローグリーン：タイトル・区切りスライドのアクセント */
  }

  /* ── 通常スライドの基本スタイル ──────────────────────── */
  section {
    font-family: "Noto Sans JP", "Hiragino Sans", sans-serif;
    font-size: 22px;
    color: #1A1A1A;
    background: #ffffff;
    padding: 48px 56px;
  }

  /* ── 見出し ──────────────────────────────────────────── */
  h1 {
    font-size: 2em;
    color: var(--navy);
    border: none;
    margin-bottom: 0.5em;
  }
  h2 {
    /* セクション内の中見出し。下線でセクションの切れ目を示す */
    font-size: 1.3em;
    color: var(--teal);
    border-bottom: 2px solid var(--teal-light);
    padding-bottom: 0.2em;
  }
  h3 {
    font-size: 1.05em;
    color: var(--navy);
  }

  /* ── コードブロック ──────────────────────────────────── */
  code {
    /* インラインコード（コマンド名・変数名など） */
    font-family: "Courier New", monospace;
    background: #F0F0F0;
    padding: 0.1em 0.4em;
    border-radius: 3px;
    font-size: 0.88em;
    color: #2B2B2B;
  }
  pre {
    /* フェンスコードブロック（コマンド・スクリプト全体） */
    background: #F0F0F0;
    border-radius: 6px;
    padding: 0.8em 1em;
    font-size: 0.82em;
    line-height: 1.55;
  }
  pre code {
    background: none;
    padding: 0;
  }

  /* ── テーブル ────────────────────────────────────────── */
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88em;
  }
  th {
    background: var(--navy);
    color: #ffffff;
    padding: 0.4em 0.7em;
    font-weight: bold;
  }
  td {
    padding: 0.4em 0.7em;
    border-bottom: 1px solid #e0e0e0;
    vertical-align: top;
  }
  tr:nth-child(even) td { background: var(--light); }

  /* ── ユーティリティクラス ────────────────────────────── */
  .label {
    /* スライド上部に置くセクション名ラベル（小さめの大文字） */
    font-size: 0.7em;
    font-weight: bold;
    color: var(--teal);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.2em;
  }
  .note {
    /* 補足・注意書き。スライド下部に配置することが多い */
    font-size: 0.78em;
    color: #6B7280;
    font-style: italic;
    margin-top: 0.6em;
  }
  .warn { color: var(--red);   font-weight: bold; }  /* 警告テキスト */
  .ok   { color: var(--green); font-weight: bold; }  /* OK・正解テキスト */

  /* ── タイトルスライド（_class: title） ─────────────────
     プロジェクター投影を考慮して白背景。
     ブランドカラー（--brand）を左帯として使い視認性を確保。 */
  section.title {
    background: #ffffff;
    color: var(--navy);
    justify-content: flex-start;
    padding-top: 60px;
    border-left: 14px solid var(--brand);
  }
  section.title h1 { color: var(--navy); font-size: 1.4em; margin-bottom: 0.1em; }
  section.title h2 { color: var(--navy); font-size: 2.2em; border: none; margin-bottom: 0.2em; font-weight: bold; }
  section.title h3 { color: var(--teal); font-size: 1.2em; font-weight: normal; }
  section.title p  { color: var(--gray); font-size: 0.85em; }

  /* ── アクセントスライド（_class: dark）─ ハンズオン導入・予告などに使用
     名称は dark のまま互換性を保つが、プロジェクター向けに白背景へ変更。
     上部にブランドカラーの帯を入れてセクション区切りを示す。          */
  section.dark {
    background: #ffffff;
    color: var(--navy);
    justify-content: flex-start;
    border-top: 12px solid var(--brand);
    padding-top: 52px;
  }
  section.dark h1   { color: var(--gray); font-size: 1.1em; margin-bottom: 0.2em; font-weight: normal; }
  section.dark h2   { color: var(--navy); font-size: 1.9em; border: none; margin-bottom: 0.5em; font-weight: bold; }
  section.dark li   { color: var(--gray); }
  section.dark .note { color: var(--teal); font-style: italic; }
---

<!-- _class: title -->
<!-- _paginate: false -->

<div class="label">リモセン応用セミナー WebGIS実装講座</div>

# 第1回

## タイル配信①
### データ構造とパース

2026年6月19日（金）　全6回 × 2.5h
対象：WebエンジニアGeocJSON・QGIS経験あり

---

<div class="label">本日の構成</div>

# タイムライン

| 時間 | 項目 |
|---|---|
| 0:00–0:05 | ガイダンス |
| 0:05–0:20 | WebGIS タイル配信エコシステムの概論 |
| 0:20–0:35 | タイルピラミッド・座標系・リクエストの仕組み |
| 0:35–0:50 | ラスタータイルとベクタータイルの違い（MVT / PMTiles） |
| **0:50–1:00** | **── 中休み ──** |
| 1:00–1:25 | タイルサーバー比較（GeoServer / Martin / SaaS） |
| 1:25–1:45 | GIS レンダリングエンジンのタイル処理を読む |
| **1:45–2:20** | **ハンズオン：tippecanoe で PMTiles 生成 → MapLibre 確認** |
| 2:20–2:30 | まとめ・次回への接続 |

---

<div class="label">ガイダンス</div>

# 本日の到達目標

- タイルピラミッドの仕組みを説明できる
- MVT（protobuf）と PMTiles の関係を整理できる
- `tippecanoe` で PMTiles を生成し、MapLibre で表示できた

<br>

> 「外部サービスをブラックボックスとして使わず、データの流れを自分の言葉で整理できる」状態を目標とする

---

<div class="label">エコシステム概論</div>

# WebGIS タイル配信のスタック

| データ生成 | 変換・生成 | 配信 | クライアント |
|---|---|---|---|
| QGIS | GDAL / ogr2ogr | Martin（Rust） | MapLibre GL JS |
| PostGIS | tippecanoe | Nginx + PMTiles | OpenLayers |
| 衛星画像・DEM | rio-cogeo | MapTiler Cloud | Leaflet |

<br>

**本講義のスコープ：変換・生成 → 配信 → クライアント の流れを自分で組む**

<div class="note">OSGeo / FOSS4G コミュニティが上記ツール群の多くを支えている。MapLibre は Mapbox の 2021 年フォーク。</div>

---

<div class="label">タイルピラミッド</div>

# ズームレベルとタイル分割

ズームレベル `z` において、世界地図は **2^z × 2^z 枚**に分割される。

| ズーム | タイル数 | スケール感 |
|---|---|---|
| Z=0 | 1枚 | 世界全体 |
| Z=1 | 4枚 | |
| Z=2 | 16枚 | |
| Z=10 | 約 100万枚 | 市区町村レベル |
| Z=17 | 約 170億枚 | 農地区画・建物レベル |

<div class="note">ズームが1上がるごとにタイル数は4倍。高ズームの全タイル生成はストレージが膨大になるため、tippecanoe では生成範囲を -Z / -z で絞る。</div>

---

<div class="label">タイルピラミッド</div>

# タイルのアドレス指定

```
https://example.com/tiles/{z}/{x}/{y}.pbf

例：東京駅付近・ズーム17
https://example.com/tiles/17/116561/51781.pbf
```

- `x` : 西から数えたタイル番号（0 〜 2^z − 1）
- `y` : 北から数えたタイル番号（**XYZ 規格**の場合）

<br>

| 規格 | y 軸の向き | 備考 |
|---|---|---|
| XYZ（Slippy Map） | 北が 0 | MapLibre・Leaflet のデフォルト |
| TMS | 南が 0（反転） | `gdal2tiles` のデフォルト出力がこれ |
| WMTS | OGC 標準 | GISサーバー系との互換 |

<p class="warn">gdal2tiles で生成したタイルは TMS 形式 → MapLibre へ渡す際に y 軸の変換が必要</p>

---

<div class="label">座標系の整理</div>

# EPSG:4326 / 3857 / JGD2011

| コード | 名称 | 用途 |
|---|---|---|
| EPSG:4326 | WGS84 | 緯度・経度の10進数表現。GeoJSON・GPS データのデフォルト。 |
| EPSG:3857 | Web Mercator | タイルグリッド・地図表示のデファクト標準。メートル単位の平面座標。 |
| EPSG:6668 | JGD2011 | 日本の公的データ（農水省筆ポリゴン等）の配布座標系。**そのままでは使えない。** |

<br>

```bash
# JGD2011 → WGS84 変換
ogr2ogr -f GeoJSON output.geojson input.shp -t_srs EPSG:4326
```

<div class="note">ハンズオンの Step 1 でこの変換を実施する。</div>

---

<div class="label">タイルの種類</div>

# ラスタータイルとベクタータイル（MVT）

|  | ラスタータイル | ベクタータイル（MVT） |
|---|---|---|
| 形式 | PNG / JPEG 画像 | protobuf（バイナリ） |
| レンダリング | サーバー側で事前生成 | クライアント（GPU）側 |
| スタイル変更 | 不可（再生成が必要） | リアルタイムに変更可能 |
| 滑らかさ | ズーム段差あり | スムーズ |
| 主な用途 | 衛星画像・Terrain RGB | 地物・道路・境界 |

<div class="note">本講義はベクタータイル（MVT / PMTiles）を主軸とする。ラスタータイルは第3・4回（DEM）で扱う。</div>

---

<div class="label">データ構造</div>

# MVT（Mapbox Vector Tile）の構造

```
.pbf ファイル（バイナリ）
└── layer: "buildings"
    ├── feature { geometry: Polygon, props: {height: 20} }
    ├── feature { geometry: Polygon, props: {height: 35} }
    └── ...
└── layer: "roads"
    ├── feature { geometry: LineString, props: {name: "国道2号"} }
    └── ...
```

- 座標は **0〜4096 の整数**（タイル内相対値）でエンコード → 軽量
- 実座標への変換はクライアント側で行う
- 仕様：[mapbox/vector-tile-spec](https://github.com/mapbox/vector-tile-spec)

---

<div class="label">データ構造</div>

# PMTiles とは

複数の MVT タイルを **1ファイルにアーカイブ**した形式。

```
fude.pmtiles（単一ファイル）
├── ヘッダー（インデックス：タイル座標 → バイト位置の対応表）
├── z=10, x=..., y=... のタイルデータ
├── z=11, x=..., y=... のタイルデータ
└── ...（全ズームレベルのタイルが連続格納）
```

**HTTP Range Request（206 Partial Content）** を使い、ブラウザが必要なタイルのバイト範囲だけを取得する。

- タイルサーバーを立てなくても **Nginx / S3 / CDN** で配信可能
- MBTiles（SQLite）との違いはアーカイブ方式のみ

---

<div class="label">タイルサーバー比較</div>

# GeoServer / Martin / tileserver-gl / SaaS

| サーバー | 実装 | PMTiles | 起動コスト | 主な用途 |
|---|---|---|---|---|
| **GeoServer** | Java / WAR | 直接配信不可 | 重い（JVM） | OGC 標準準拠が必要なエンタープライズ連携 |
| **Martin** | Rust / 単一バイナリ | ✓ | 軽い（即起動） | PostGIS / MBTiles / PMTiles を統一配信 |
| **tileserver-gl** | Node.js | ✓ | 中程度 | ラスタータイルの動的生成が必要な場合 |
| **MapTiler / Mapbox** | SaaS | プラン依存 | 最小 | プロトタイピング |

<div class="note">本講義では Martin + PMTiles を軸にする。GeoServer は「起動して URL を確認する」デモに留める。SaaS はリクエスト数超過で課金・ロックインリスクに注意。</div>

---

<div class="label">タイルサーバー比較 — Martin</div>

# Martin の起動と MapLibre からの接続

```bash
# インストール
brew install martin

# PMTiles を配信
martin fude.pmtiles
# → http://localhost:3000/fude/{z}/{x}/{y}
```

```js
// MapLibre からの接続
map.addSource('fude', {
  type: 'vector',
  tiles: ['http://localhost:3000/fude/{z}/{x}/{y}']
});
```

**確認ポイント：** Network タブで `/z/x/y` へのリクエストがズームに連動して発生することを確認。GeoServer の WMTS URL（長いクエリパラメータ）と比較する。

---

<div class="label">GIS レンダリングエンジン</div>

# MapLibre GL JS がタイルを処理する流れ

1. スタイル JSON 読み込み → `source` の URL を確認
2. viewport + zoom から必要タイル座標（z/x/y）を計算
3. タイル URL に Fetch リクエスト
4. 受け取った protobuf（MVT）をデコード
5. WebGL にジオメトリを転送 → GPU でレンダリング

<br>

| 処理 | 内部ライブラリ |
|---|---|
| GeoJSON → タイル変換 | `geojson-vt` |
| protobuf デコード | `@mapbox/vector-tile` + `pbf` |
| レンダリング | WebGL |

---

<div class="label">GIS レンダリングエンジン</div>

# GeoJSON source と vector source の処理コスト

**GeoJSON source を使う場合**、MapLibre は受け取った GeoJSON を内部で `geojson-vt` によってタイルに変換してからレンダリングする。

→ **クライアントがタイル変換のコストを負担する**

フィーチャー数が **10万オーダーを超えると**、この変換処理がボトルネックになる。

<br>

**vector source（PMTiles / MVT）を使う場合**、タイル変換済みのバイナリを直接デコードして GPU に渡す。

→ `geojson-vt` の変換コストは発生しない

---

<div class="label">実例</div>

# 大量ポリゴンが描画されない問題：地番図を例に

| | 内容 |
|---|---|
| **状況** | 10万オーダーの地番ポリゴンを GeoJSON から直接読み込み |
| **症状** | レンタルサーバーでデータは到達しているが描画されない |
| **初期仮説** | ネットワーク転送が原因？ |
| **切り分け** | `curl` → GeoJSON 到達確認。DevTools Memory → メモリ展開済みと確認 |
| **原因** | MapLibre 内部の `geojson-vt` 変換処理が CPU ボトルネック |
| **解決** | GeoJSON → PMTiles（tippecanoe）に変換 → 解消 |

<div class="note">「ネットワークが原因」という初期仮説が外れた点が重要。DevTools の Memory タブでの切り分けが有効。</div>

---

<div class="label">ハンズオン — 事前準備</div>

# ツールのインストール

**GDAL / ogr2ogr**

```bash
# macOS
brew install gdal

# Linux (Ubuntu/Debian)
sudo apt install gdal-bin

# Windows → OSGeo4W インストーラー（QGIS に同梱されていれば不要）
#   https://trac.osgeo.org/osgeo4w/
```

**tippecanoe**

```bash
# macOS
brew install tippecanoe

# Linux (Ubuntu/Debian)
sudo apt install tippecanoe

# Windows → WSL (Windows Subsystem for Linux) を使用
#   WSL 導入: https://learn.microsoft.com/ja-jp/windows/wsl/install
#   WSL 内で上記 Linux コマンドを実行する
```

<p class="warn">tippecanoe は Windows ネイティブビルドが存在しない。Windows の方は WSL を事前に有効化してください。</p>
<div class="note">詳細な確認手順は handson/00_setup.md を参照。</div>

---

<!-- _class: dark -->

# ハンズオン

## tippecanoe で PMTiles を生成して MapLibre で表示する

**使用データ：**
農林水産省「農業用地利用状況調査（筆ポリゴン）」
https://open.fude.maff.go.jp/ → 山口県の Shapefile をDL

1. Step 1：ogr2ogr で座標変換（JGD2011 → WGS84）
2. Step 2：tippecanoe で PMTiles 生成
3. Step 3：MapLibre で表示・確認

---

<div class="label">ハンズオン — Step 1</div>

# ogr2ogr で座標変換

```bash
ogr2ogr \
  -f GeoJSON fude.geojson \
  ダウンロードした.shp \
  -t_srs EPSG:4326
```

変換後の確認：

```bash
# macOS / Linux
ls -lh fude.geojson
wc -l fude.geojson

# Windows (PowerShell)
Get-Item fude.geojson | Select-Object Length
```

- 筆ポリゴンは JGD2011（EPSG:6668）配布 → EPSG:4326 に変換しないと tippecanoe に渡せない
- Shapefile が複数ファイル（`.shp` / `.dbf` / `.prj` / `.shx`）で構成されていることを確認

---

<div class="label">ハンズオン — Step 2</div>

# tippecanoe で PMTiles 生成

```bash
# macOS / Linux（Windows は WSL 内で実行）
tippecanoe \
  -o fude.pmtiles \
  --force \
  -z 17 -Z 10 \
  --drop-densest-as-needed \
  -l fude \
  fude.geojson
```

| オプション | 意味 |
|---|---|
| `-z 17` | 最大ズームレベル（農地区画の精度に合わせる） |
| `-Z 10` | 最小ズームレベル（これより引くとタイルが存在しない） |
| `--drop-densest-as-needed` | タイルサイズ上限（500KB）超過時にフィーチャーを自動間引き |
| `-l fude` | source-layer 名（MapLibre 側で参照する） |

```bash
ls -lh fude.pmtiles   # GeoJSON の数分の1〜数十分の1程度になる
```

---

<div class="label">ハンズオン — Step 3</div>

# MapLibre で PMTiles を表示する（1/2）

```js
// PMTiles プロトコルを登録
const protocol = new pmtiles.Protocol();
maplibregl.addProtocol('pmtiles', protocol.tile);

const map = new maplibregl.Map({
  container: 'map',
  style: {
    version: 8,
    sources: {
      osm: {
        type: 'raster',
        tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
        tileSize: 256
      },
      fude: {
        type: 'vector',
        url: 'pmtiles://./fude.pmtiles'
      }
    },
```

---

<div class="label">ハンズオン — Step 3</div>

# MapLibre で PMTiles を表示する（2/2）

```js
    layers: [
      { id: 'osm', type: 'raster', source: 'osm' },
      {
        id: 'fude-fill', type: 'fill', source: 'fude',
        'source-layer': 'fude',  // tippecanoe の -l に一致させる
        paint: { 'fill-color': '#6ab04c', 'fill-opacity': 0.5 }
      }
    ]
  },
  center: [131.4, 34.1],  // 山口県付近
  zoom: 12
});
```

```bash
# macOS / Linux
python3 -m http.server 8000

# Windows (PowerShell / コマンドプロンプト)
python -m http.server 8000
# または
npx serve .
```

<div class="note">source-layer の名前は tippecanoe の -l で指定した文字列と一致する必要がある（嵌まりやすい）。</div>

---

<div class="label">ハンズオン — 比較</div>

# GeoJSON 直読み vs PMTiles

| 比較項目 | GeoJSON 直読み | PMTiles |
|---|---|---|
| 初期ロード | 全量転送・メモリ展開 | 表示範囲のタイルのみ取得 |
| MapLibre 処理 | `geojson-vt` で全フィーチャーを変換 | タイル単位でインクリメンタルにデコード |
| ファイルサイズ | 数百MB（圧縮前） | tippecanoe が自動間引き・圧縮 |
| ホスティング | 単ファイルだが転送量大 | Range Request で部分取得 |
| タイルサーバー | 不要 | 不要（静的配信で動作） |

**確認：** DevTools の Network タブで PMTiles への Range Request を観察する。GeoJSON source に切り替えて差を体感する。

---

<div class="label">まとめ</div>

# 本日の到達確認

- [ ] タイルピラミッドの仕組みを説明できる
- [ ] XYZ / TMS / WMTS の y 軸の違いを区別できる
- [ ] MVT（protobuf）と PMTiles の関係を説明できる
- [ ] `tippecanoe` で PMTiles を生成できた
- [ ] MapLibre で `vector` source として表示できた
- [ ] GeoJSON source と vector source の処理コストの違いを説明できる

---

<!-- _class: dark -->
<!-- _paginate: false -->

# 第2回（6/26）予告

## タイル配信② 自前配信とカートグラフィック

- Nginx による静的配信設定（CORS 設定含む）
- Maputnik でのスタイル設計
- MapLibre GL JS によるレンダリング実装
- デモ①：ラズパイタイルサーバーへの接続体験
- デモ②：地理院地図ベクターの試行錯誤
- OSM エコシステムと外部サービスの整理・判断基準

<div class="note">第2回は現地開催です。今日生成した PMTiles ファイルを持参または共有してください。</div>