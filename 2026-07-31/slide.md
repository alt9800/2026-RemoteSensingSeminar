---
marp: true
theme: default
header: "衛星データ解析技術研究会<br>技術セミナー（応用編）第六回 2026/07/31"
footer: "第6回 高さデータ②：可視化・実務データとのオーバーラップ・現地調査への応用"
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

# 衛星データ解析技術研究会 技術セミナー（応用編）

## 第6回 高さデータ②
## 可視化・実務データとのオーバーラップ・現地調査への応用

### 2026年7月31日（金）

到達目標：高さデータとリモートセンシング由来データを組み合わせた3D地図をブラウザ上で動かせる／通信前提とオフライン設計のトレードオフを説明できる

---

## 本日のタイムテーブル（140分）

| 時間 | 内容 |
|------|------|
| 10分 | イントロ・前回の復習（Terrain RGBタイルはどこまでできたか） |
| 15分 | ブラウザで地形を立体表示する2つの実装（MapLibre terrain / deck.gl TerrainLayer） |
| 35分 | ハンズオン①：MapLibreで3D地形ビューア＋衛星画像・NDWIオーバーレイ |
| 10分 | 休憩 |
| 30分 | ハンズオン②：防災重点溜池を重ねたハザードマップビューア |
| 15分 | 現地調査ツールとしての仕上げ：通信前提設計とオフライン設計の判断基準 |
| 15分 | 全6回の振り返り・Q&A |

<div class="note">前回はGDALで高さデータを「WebGISが読める形」に変換した。今回はそれをブラウザで立体的に描き、実務データと重ねる回。</div>

---

## 前回の復習：手元にあるはずのもの

第5回で作成した成果物を今日そのまま使う。

| 成果物 | 形式 | 今日の用途 |
|--------|------|-----------|
| Terrain RGBタイル | XYZ PNGタイル | 地形の標高ソース |
| COG化したDEM | GeoTIFF (COG) | 検算・QGISでの確認用 |
| ヒルシェード | ラスタータイル | 平面地図への陰影オーバーレイ |

```sh
# タイルディレクトリの確認（前回の出力）
ls terrain-rgb/
# => 10/ 11/ 12/ 13/ 14/  ← ズームレベルごとのディレクトリ
```

<div class="note">未完了の方は配布済みの完成版タイルセットを使ってください（USBまたはローカルサーバーから取得）。</div>

---

## Terrain RGBの復習：標高を色に埋め込む

RGBの3チャンネル（各8bit）に標高値をエンコードした形式。

```
elevation = -10000 + ((R * 256 * 256 + G * 256 + B) * 0.1)
```

- 1px = 24bit → 0.1m刻みで約1677万段階を表現できる
- 見た目はサイケデリックな画像だが、デコードすれば数値ラスターに戻る
- MapLibre・deck.glともにこの形式を直接読める

| 方式 | 由来 | デコード式 |
|------|------|-----------|
| Mapbox Terrain-RGB | Mapbox | 上記の式 |
| Terrarium | Mapzen (AWS Terrain Tiles) | `(R * 256 + G + B / 256) - 32768` |

<span class="warn">どちらの式でエンコードしたかを取り違えると標高が壊れる。</span>前回はMapbox式（`rio rgbify`のデフォルト）で作成した。

---

## ブラウザで地形を立体表示する2つのアプローチ

| | MapLibre terrain | deck.gl TerrainLayer |
|---|---|---|
| 立ち位置 | 地図エンジンの組み込み機能 | 汎用WebGLレイヤーの一つ |
| 実装量 | 少ない（`setTerrain`一発） | 中程度（レイヤー定義を書く） |
| カメラ | 地図的（pitch最大85度前後） | 自由（真横からも見られる） |
| 他レイヤーとの合成 | スタイル内で完結 | 任意のdeck.glレイヤーと合成 |
| 適する用途 | 背景としての地形＋2D的操作 | 点群・解析結果との統合表示 |

今日は両方を動かして比較する。

- ハンズオン①：MapLibre（実装が軽く、現地調査ツールに向く）
- ハンズオン②の後半で：deck.gl版との見え方の違いを確認

---

## MapLibre terrainの最小構成

スタイルに`raster-dem`ソースを追加し、`setTerrain`で指定するだけ。

```js
const map = new maplibregl.Map({
  container: 'map',
  style: 'style.json',
  center: [131.25, 33.95],
  zoom: 12,
  pitch: 60,          // 立体感を出すには pitch が必須
  maxPitch: 85
});

map.on('load', () => {
  map.addSource('dem', {
    type: 'raster-dem',
    tiles: ['./terrain-rgb/{z}/{x}/{y}.png'],
    tileSize: 256,
    encoding: 'mapbox',   // Terrarium形式なら 'terrarium'
    maxzoom: 14
  });
  map.setTerrain({ source: 'dem', exaggeration: 1.5 });
});
```

<div class="note">配信は第2回で構築したNginx静的配信がそのまま使える。Terrain RGBタイルはただのPNGなので特別な設定は不要。</div>

---

## 垂直誇張（exaggeration）の設計

`exaggeration: 1.5`は標高を1.5倍に引き伸ばす指定。

- 低山地・丘陵地（山口県の多く）は1.0だと起伏が伝わりにくい
- 誇張しすぎると距離感・斜度の判断を誤らせる

| 用途 | 目安 |
|------|------|
| 広域の概観（県スケール） | 1.5〜2.0 |
| 現地調査・斜度の読み取り | 1.0〜1.2 |
| プレゼン・デモ | 2.0前後（ただし誇張している旨を明記） |

<span class="warn">実務資料に誇張した3D表示を載せる場合は倍率を必ず注記する。</span>「見栄えのための誇張」と「判断材料としての表示」は分けて考える。

---

## hillshade：3Dにしなくても伝わる場面は多い

MapLibreは同じ`raster-dem`ソースから陰影段彩（hillshade）レイヤーも生成できる。

```js
map.addLayer({
  id: 'hillshade',
  type: 'hillshade',
  source: 'dem',
  paint: {
    'hillshade-exaggeration': 0.4,
    'hillshade-shadow-color': '#473B24'
  }
});
```

- pitchを倒さない平面地図でも地形が読める
- 3D表示より描画負荷が軽い（モバイルで効く）
- 溜池・水路と地形の関係を俯瞰するにはむしろ平面＋陰影が読みやすいことも

<div class="note">「3Dで見せること」自体は目的ではない。読み取りたい情報に対して表示方法を選ぶ。</div>

---

<!-- _class: dark -->

# ハンズオン①

## 3D地形ビューア＋NDWIオーバーレイ

- 前回のTerrain RGBタイルをMapLibreで立体表示する
- 配布済みNDWIラスタータイルを半透明で重ねる
- 垂直誇張・不透明度をUIから調整できるようにする

<div class="note">手順は本スライドに沿って進めます。完成版コードは handson/01_terrain_viewer/ にあります。</div>

---

## ハンズオン①：ファイル構成

```
01_terrain_viewer/
├── index.html        # 本体（HTML + JS + CSS を1ファイルに）
├── terrain-rgb/      # 前回作成したTerrain RGBタイル
│   └── {z}/{x}/{y}.png
└── ndwi/             # 配布済みNDWIラスタータイル
    └── {z}/{x}/{y}.png
```

配信はローカルNginxまたは開発サーバーで行う。

```sh
# 手軽に試すなら（Python標準ライブラリ）
python3 -m http.server 8000
# ブラウザで http://localhost:8000/index.html
```

<span class="warn">`file://`で直接開くとタイルのfetchが失敗する。</span>必ずHTTP経由で配信する。

---

## ハンズオン①：NDWIタイルを重ねる

NDWI（正規化水指数）は水域で高い値を示す。配布タイルは水域を青系で着色済み。

```js
map.addSource('ndwi', {
  type: 'raster',
  tiles: ['./ndwi/{z}/{x}/{y}.png'],
  tileSize: 256,
  minzoom: 10,
  maxzoom: 14
});
map.addLayer({
  id: 'ndwi-layer',
  type: 'raster',
  source: 'ndwi',
  paint: { 'raster-opacity': 0.6 }   // 地形が透けて見える程度に
});
```

- terrainが有効な状態では、rasterレイヤーも地形に沿って貼り付く
- 谷筋・低地とNDWIの高い領域（水域・湿潤域）の対応が立体的に読める

---

## ハンズオン①：UIをつける（誇張・不透明度スライダー）

```html
<div id="ctrl">
  <label>垂直誇張 <input type="range" id="exag"
    min="0" max="3" step="0.1" value="1.5"></label>
  <label>NDWI不透明度 <input type="range" id="op"
    min="0" max="1" step="0.05" value="0.6"></label>
</div>
```

```js
document.getElementById('exag').addEventListener('input', (e) => {
  map.setTerrain({ source: 'dem', exaggeration: Number(e.target.value) });
});
document.getElementById('op').addEventListener('input', (e) => {
  map.setPaintProperty('ndwi-layer', 'raster-opacity', Number(e.target.value));
});
```

```css
/* 地図の上に重ねる操作パネル。モバイルでは下端に寄せて親指で届く位置に */
#ctrl { position: absolute; z-index: 1; bottom: 12px; left: 12px;
        background: rgba(255,255,255,0.9); padding: 8px 12px; border-radius: 6px; }
@media (max-width: 600px) { #ctrl { left: 8px; right: 8px; } }
```

---

## チェックポイント①

以下が確認できたら休憩へ。

- pitchを倒すと地形が立体的に表示される
- スライダーで誇張倍率がリアルタイムに変わる
- NDWIレイヤーが地形に沿って表示され、不透明度を調整できる
- 谷筋・溜池の位置とNDWI高値域が対応している

うまくいかないときの切り分け：

| 症状 | 確認すること |
|------|-------------|
| 地形が真っ平ら | `pitch`が0のまま／`setTerrain`が`load`前に呼ばれていないか |
| 標高が異常（数千m等） | `encoding`指定とエンコード方式の不一致 |
| タイルが404 | パスの`{z}/{x}/{y}`とディレクトリ構造の対応、配信URL |
| モバイルで極端に重い | `maxzoom`の下げすぎ・タイルサイズ・端末のWebGL性能 |

---

## 防災重点溜池データ（国土数値情報）

ハンズオン②で使う実務データ。

- 農業用溜池のうち、決壊時に人的被害を与えるおそれのあるものを都道府県が選定
- 国土数値情報（ため池データ）としてGeoJSON/Shapefileで公開されている
- 属性：名称、所在地、堤高、貯水量、防災重点指定の有無など

前処理は第1回・第2回で学んだ流れがそのまま使える：

```sh
# Shapefile → GeoJSON（山口県分を抽出済みのものを配布）
ogr2ogr -f GeoJSON tameike.geojson tameike.shp -t_srs EPSG:4326

# 件数が多い場合はPMTiles化（今回の県内データは素のGeoJSONで足りる）
tippecanoe -o tameike.pmtiles -zg tameike.geojson
```

<div class="note">「タイル配信で学んだ変換パイプライン」「高さデータ」「実務のポイントデータ」がここで一つに合流する。</div>

---

<!-- _class: dark -->

# ハンズオン②

## 防災重点溜池を重ねたハザードマップビューア

- ハンズオン①のビューアに溜池ポイント/ポリゴンを追加する
- タップで属性（名称・堤高・貯水量）をポップアップ表示する
- 地形＋NDWI＋溜池で「決壊時にどこへ流れるか」を目視で検討する

---

## ハンズオン②：溜池レイヤーの追加

```js
map.addSource('tameike', {
  type: 'geojson',
  data: './tameike.geojson'
});
map.addLayer({
  id: 'tameike-pt',
  type: 'circle',
  source: 'tameike',
  paint: {
    'circle-radius': 6,
    'circle-color': '#B91C1C',
    'circle-stroke-color': '#ffffff',
    'circle-stroke-width': 1.5
  }
});
map.on('click', 'tameike-pt', (e) => {
  const p = e.features[0].properties;
  new maplibregl.Popup()
    .setLngLat(e.lngLat)
    .setHTML(`<strong>${p.name}</strong><br>堤高: ${p.height} m<br>貯水量: ${p.volume} m³`)
    .addTo(map);
});
```

<div class="note">terrain有効時、circleレイヤーは地表面の標高に配置される。ポップアップの座標も地形を考慮して表示される。</div>

---

## ハンズオン②：読み取りの演習

3つのレイヤーを重ねた状態で、次を検討する。

1. 溜池の直下流にあたる谷筋はどこか（誇張1.5前後で確認）
2. NDWI高値域と溜池の位置関係：常時水がある谷か、乾いた谷か
3. 谷の出口に集落・農地（第2回のfude.pmtilesを重ねてもよい）があるか

<span class="warn">この目視検討は「浸水想定区域図」の代替にはならない。</span>正式な氾濫解析は水理計算に基づく。ここで作っているのは、現地に行く前に地形と水の関係を掴むための下見ツール。

- どのデータが「解析結果」で、どれが「素のデータの重ね合わせ」かを区別する
- リモートセンシング由来の値（NDWI）も観測日・雲・解像度の影響を受けている

---

## 参考：deck.gl TerrainLayerでの実装

同じタイルセットをdeck.glでも表示できる。第4回のPointCloudLayerと同じ枠組み。

```js
new deck.TerrainLayer({
  id: 'terrain',
  elevationData: './terrain-rgb/{z}/{x}/{y}.png',
  texture: './ndwi/{z}/{x}/{y}.png',      // 表面に貼るテクスチャ
  elevationDecoder: {                       // Mapbox式のデコード係数
    rScaler: 6553.6, gScaler: 25.6, bScaler: 0.1, offset: -10000
  },
  maxZoom: 14
});
```

- `elevationDecoder`に式を直接書く＝エンコード方式の違いがコードに現れる
- 点群（第4回）や解析メッシュと同一シーンで合成したい場合はdeck.glが向く
- 単に「地図として地形を見たい」だけならMapLibreの方が実装も動作も軽い

<div class="note">handson/03_deckgl_terrain/ に比較用の完成コードを置いています。時間があれば触ってください。</div>

---

## 現地調査ツールとして仕上げる

スマホブラウザで動かす前提で確認すべきこと。

| 観点 | 対応 |
|------|------|
| 画面サイズ | 操作パネルを下端配置・タップ領域を44px以上に |
| 現在位置 | GeolocationAPI（第3回）でマーカー表示 |
| 通信 | 現地の電波状況を事前に確認する |
| バッテリー | WebGL＋GPSは消費が大きい。モバイルバッテリー携行 |
| 直射日光 | 画面輝度・配色（白背景＋高コントラストが有利） |

```js
// 現在位置の追従（第3回の復習）
navigator.geolocation.watchPosition((pos) => {
  marker.setLngLat([pos.coords.longitude, pos.coords.latitude]);
}, null, { enableHighAccuracy: true });
```

---

## 通信前提設計とオフライン設計の判断基準

まず「通信前提で足りるか」を検討する。オフライン化はコストが高い。

| 判断材料 | 通信前提でよい | オフライン設計が必要 |
|----------|---------------|---------------------|
| 調査地の電波 | 市街地・幹線道路沿い | 山間部・谷底・トンネル |
| 失敗時の影響 | 後日再訪できる | 再訪困難（船・許可が必要な場所） |
| データ量 | タイル都度取得で足りる | 広域を高ズームで見る必要がある |
| 利用者 | 自分（切り分けできる） | 配布先（トラブル対応できない） |

オフライン化の主な手段（設計論として）：

- ブラウザのHTTPキャッシュ：滞在前に対象範囲をなぞって温めておく（簡易・保証なし）
- Service Worker + Cache Storage：PWAとして明示的にタイルを先読み保存
- タイル同梱：本セミナー第2回方式。Raspberry Pi等をローカル配信サーバーとして持参

<div class="note">第2回のPi配信構成は「会場に通信がない」問題への回答だった。現地調査でも同じ構図が成り立つ。</div>

---

## PWA・オフラインキャッシュ（設計の要点のみ）

実装は持ち帰り課題とし、構成だけ押さえる。

```
アプリ本体（HTML/JS/CSS） … Service Workerでキャッシュ（小さい）
タイル（terrain-rgb / ndwi）… 範囲×ズームで容量が急増する
GeoJSON（溜池）            … 小さいのでキャッシュ容易
```

- タイル容量の概算：範囲とズームを決めれば `(タイル数) × (平均サイズ)` で見積もれる
- z14まで市町村1つ分で数百MBになることもある。<span class="warn">「全部キャッシュ」は破綻する</span>
- 調査対象範囲だけを先読みする設計（バウンディングボックス指定）が現実的
- iOS SafariのCache Storageには容量・保持期間の制約がある点も考慮する

<div class="note">「どのレベルで自作するか」（第2回）と同じ問い。要件が軽ければブラウザキャッシュ、確実性が要るならタイル同梱＋ローカル配信。</div>

---

## チェックポイント②

- 溜池ポイントが地形上に表示され、タップで属性が出る
- 地形・NDWI・溜池の3層を重ねて谷筋の読み取りができた
- 自分の調査ユースケースが「通信前提」「オフライン必要」のどちらかを説明できる

---

## 全6回の振り返り：一本の線としてのデータフロー

```
[取得]                [変換]                  [配信]              [可視化]
衛星/LiDAR/スマホ → GDAL / tippecanoe →  Nginx / PMTiles  → MapLibre / deck.gl
  第3回・第5回        第1回・第5回           第2回              全回
```

| 回 | 学んだこと | 今日どこで使ったか |
|----|-----------|-------------------|
| 第1回 | タイルの構造・生成 | Terrain RGBもXYZタイルの一種 |
| 第2回 | 自前配信・スタイル | タイルの静的配信・配信環境持参の発想 |
| 第3回 | スマホセンサー | 現在位置の追従表示 |
| 第4回 | 3Dの描画基盤 | deck.glでの地形表示・点群との合成 |
| 第5回 | 高さデータの変換 | 今日の入力データすべて |

外部サービスの各機能が「この線のどこを肩代わりしているか」を指させれば、採用・自作の判断は自分でできる。

---

## この先へ

- 正式な浸水解析・斜面解析への接続：GDAL/GRASS/SAGAの地形解析モジュール
- 点群（第4回）とDEM（第5-6回）の統合：LiDAR点群からのDTM生成
- FOSS4Gコミュニティ：国内イベント・ソースコードリーディングは学習の近道
- 本セミナーの教材はすべてリポジトリに残ります。改変・再利用は自由です

質問・相談は本日のQ&Aのほか、セミナーSlackでも受け付けます。

### 全6回、お疲れさまでした。

---

## 付録：本日使ったデータの出典

| データ | 出典 |
|--------|------|
| DEM（元データ） | 第5回配布（基盤地図情報 数値標高モデル等） |
| NDWIラスター | 配布済み（Sentinel-2由来、観測日はメタデータ参照） |
| 防災重点溜池 | 国土数値情報 ため池データ（国土交通省） |
| 筆ポリゴン | 農林水産省 筆ポリゴンオープンデータ |
| 背景地図 | OpenStreetMap contributors / 地理院タイル |

利用時は各データのライセンス・出典表記に従うこと。