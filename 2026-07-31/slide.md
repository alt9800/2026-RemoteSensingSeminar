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

## 本日の流れ（2.5h）

| 時間          | 内容 |
| ----------- | ---- |
| 00:00–00:10 | 前回成果物の確認・本日の位置づけ |
| 00:10–00:25 | ブラウザで地形を立体表示する2つの実装（MapLibre / deck.gl） |
| 00:25–00:55 | ハンズオン①：`terrain.pmtiles` を3D表示する |
| 00:55–01:05 | Mapterhorn比較：解像度とエンコード方式の違いを見る |
| 01:05–01:15 | 休憩 |
| 01:15–01:45 | ハンズオン②：NDWI・防災重点溜池を重ねたハザードビューア |
| 01:45–01:55 | 発展の紹介：PLATEAU 3D Tiles・deck.gl・AR（デモ・持ち帰り） |
| 01:55–02:10 | 現地調査ツールとしての設計：通信前提とオフライン |
| 02:10–02:30 | 全6回の振り返り・Q&A |

---

## 前回作成したファイルがそのまま使えます

第5回のハンズオンで手元に残っているはずのもの：

| ファイル | 今日の用途 |
| -------- | ---------- |
| `terrain.pmtiles` | 3D表示の標高ソース（ハンズオン①②の主役） |
| `dem_cog.tif` | 検算・QGISでの確認、COG直読みの実験 |

```sh
# 中身の確認（第5回の復習）
pmtiles show terrain.pmtiles
# minzoom / maxzoom / bounds が対象範囲と合っているかを見る
```

未完走の方には完成版を用意しています。Slackの本日チャンネル、またはハンズオンページ記載の静的ファイルURLから取得してください。

<div class="note">第5回の発展課題（GSI 1mメッシュ）まで進めた方は、そのpmtilesも後半で使えます。</div>

---

## 配信のおさらい

PMTilesはHTTP経由で配信されている必要があります。`http-server`や`python -m http.server`などでハンズオン用ディレクトリをホストして進めてください。

```sh
cd handson-20260731
python3 -m http.server 8000
# → http://localhost:8000/01_terrain3d/
```

第2回のNginx構成がある方はそちらでも構いません。

---

## ブラウザで地形を立体表示する2つのアプローチ

| | MapLibre terrain | deck.gl TerrainLayer |
|---|---|---|
| 立ち位置 | 地図エンジンの組み込み機能 | 汎用WebGLレイヤーの一つ |
| 実装量 | 少ない（`setTerrain`一発） | 中程度（レイヤー定義を書く） |
| デコード | `encoding`指定（mapbox / terrarium） | `elevationDecoder`に式を自分で書く |
| カメラ | 地図的（pitch最大85度前後） | 自由（真横からも見られる） |
| 適する用途 | 背景としての地形＋2D的操作 | 点群・解析結果との統合表示 |

本日の主経路はMapLibre。実装が軽く、スマホブラウザでの現地利用に向く。

deck.gl版は`04_deckgl_terrain`に比較用コードを置いています（第4回のPointCloudLayerと同じ枠組みで書ける）。

---

## MapLibre terrainの最小構成

第5回の検証ビューア（hillshade）に、`setTerrain`を足すだけで3Dになる。

```js
const protocol = new pmtiles.Protocol();
maplibregl.addProtocol("pmtiles", protocol.tile);

const map = new maplibregl.Map({
  container: "map",
  style: { version: 8, sources: {
    terrainSource: {
      type: "raster-dem",
      url: "pmtiles://terrain.pmtiles",
      encoding: "mapbox",       // 第5回のrio rgbify / 自前エンコードはこの方式
      tileSize: 256
    }, /* ... 背景タイル省略 ... */ },
    layers: [ /* ... */ ] },
  center: [131.256, 33.983],
  zoom: 14, pitch: 60, maxPitch: 85
});
map.on("load", () => {
  map.setTerrain({ source: "terrainSource", exaggeration: 1.5 });
});
```

<span class="warn">ソースの`minzoom`/`maxzoom`はpmtilesの実ズーム範囲に合わせる。</span>実データより低いminzoomを書いても、そのズームにタイルは存在しない（初期表示が空になる典型例）。

---

## 垂直誇張（exaggeration）の設計

`exaggeration: 1.5`は標高を1.5倍に引き伸ばす指定。

- 低山地・丘陵地（山口県の多く）は1.0だと起伏が伝わりにくい
- 誇張しすぎると距離感・斜度の判断を誤らせる

| 用途 | 目安 |
|------|------|
| 広域の概観 | 1.5〜2.0 |
| 現地調査・斜度の読み取り | 1.0〜1.2 |
| プレゼン・デモ | 2.0前後 |

実務資料に載せる場合は誇張倍率を注記する。見せるための誇張と判断材料としての表示は分けて考える。

---

## hillshade：3Dにしなくても伝わる場面は多い

同じ`raster-dem`ソースから陰影段彩レイヤーも作れる（第5回の検証ビューアがこれ）。

```js
map.addLayer({
  id: "hillshade",
  type: "hillshade",
  source: "terrainSource",
  paint: { "hillshade-exaggeration": 0.6 }
});
```

- pitchを倒さない平面地図でも地形が読める。描画負荷も3Dより軽い
- 溜池・水路と地形の関係を俯瞰するには、平面＋陰影の方が読みやすいことも
- 光源方向に依存する弱点は第5回で触れたCS立体図・赤色立体図の出発点

3Dで見せること自体は目的ではない。読み取りたい情報に合わせて表示を選ぶ。

---

<!-- _class: dark -->

# ハンズオン①

## terrain.pmtiles を3D表示する

- 第5回の検証ビューアを3D地形ビューアに発展させる
- 垂直誇張スライダー・hillshade切り替えをつける
- クリック地点の標高読み取り（Terrain RGBデコードの復習）

<div class="note">資料：handson/01_terrain3d/（完成版index.html同梱）</div>

---

## ハンズオン①：チェックポイント

- pitchを倒すと地形が立体表示される
- スライダーで誇張倍率が変わる
- クリックした地点の標高値が妥当（第5回のgdalinfo statsと突き合わせる）

| 症状 | 確認すること |
|------|-------------|
| 地形が真っ平ら | `pitch`が0のまま／`setTerrain`が`load`前に呼ばれている |
| 初期表示が空 | ソースのminzoomと実データのズーム範囲の不一致 |
| 標高が異常（-10000m等） | NoData由来。エンコード時の欠測処理を確認（第5回04参照） |
| 深い穴・崖が出る | 同上。データ縁のNoDataが標高値として解釈されている |

<div class="note">1mメッシュ由来のデータは実測範囲が狭く、範囲外がNoDataになりやすい。「穴」はバグではなくデータの被覆そのもの。</div>

---

## Mapterhorn比較：同じ場所を別のタイルで見る

第5回で紹介したMapterhornのzxyエンドポイントをソースとして差し替えてみる。

```js
terrainSource: {
  type: "raster-dem",
  tiles: ["https://tiles.mapterhorn.com/{z}/{x}/{y}.webp"],
  encoding: "terrarium",   // Mapbox方式ではない
  tileSize: 512            // 256のままだと標高が破綻する
}
```

見るべき違い：

- **解像度**：日本域は現状Copernicus 30m相当。自作の1m/10mタイルと同じ谷を見比べると、グローバルデータと国内データの情報量の差が視覚的にわかる
- **エンコード方式**：`encoding`と`tileSize`の2箇所を差し替え忘れると壊れた地形になる。第5回で「方式に互換性はない」と述べたことの実演
- **配信形態**：先方はPMTiles＋zxyの両対応。自作タイルと同じ設計思想で公開されている

---

<!-- _class: dark -->

# ハンズオン②

## NDWI・防災重点溜池を重ねたハザードビューア

- ハンズオン①のビューアにラスター・ベクターを重ねる
- タップで溜池の属性（名称・堤高・貯水量）を表示する
- 地形＋NDWI＋溜池で、水の溜まる場所・流れる先を目視で検討する

<div class="note">資料：handson/03_hazard_viewer/（NDWIタイル・溜池GeoJSONは配布データに同梱）</div>

---

## 防災重点溜池データ（国土数値情報）

- 農業用溜池のうち、決壊時に人的被害を与えるおそれのあるものを都道府県が選定
- 国土数値情報としてGeoJSON/Shapefileで公開。属性に名称・堤高・貯水量など

前処理は第1〜2回で学んだ流れがそのまま使える：

```sh
ogr2ogr -f GeoJSON tameike.geojson tameike.shp -t_srs EPSG:4326
# 件数が多ければPMTiles化（今回の県内データは素のGeoJSONで足りる）
```

タイル配信の変換パイプライン・高さデータ・実務のベクターデータが、ここで一つの画面に合流する。

---

## ハンズオン②：溜池レイヤーとポップアップ

```js
map.addSource("tameike", { type: "geojson", data: "./tameike.geojson" });
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

terrain有効時、circleレイヤーは地表面の標高に配置される。

---

## ハンズオン②：読み取りの演習

3層を重ねた状態で検討する：

1. 溜池の直下流にあたる谷筋はどこか（誇張1.5前後）
2. NDWI高値域と溜池の位置関係。常時水がある谷か、乾いた谷か
3. 谷の出口に集落・農地（第2回のfude.pmtilesを重ねてもよい）があるか

これはあくまで下見ツールであり、浸水想定区域図の代替ではない（正式な氾濫解析は水理計算に基づく）。重ねているのは解析結果ではなく素のデータであり、NDWIの値も観測日・雲・解像度の影響を受けている——という区別を意識して読む。

---

## 発展①：PLATEAU 3D Tiles を地形の上に重ねる

第4回で扱った3D Tilesを、今日の地形と同じ画面に載せられる。

```js
// deck.gl Tile3DLayer + MapLibre（interleaved）
new deck.Tile3DLayer({
  id: "plateau-bldg",
  data: "https://.../tileset.json",   // PLATEAU配信の建物3D Tiles
});
```

- PLATEAU（国交省）は建物等を3D Tilesでストリーミング配信している
- 建物の高さ（第4回）と地形の高さ（第5〜6回）が同じシーンで合成される
- 標高基準のずれ（第5回のジオイドの話）が「建物が浮く・沈む」という形で現れることがある。ずれを見つけたら原因を考えてみてほしい

資料：`05_3dtiles_plateau/`。対象都市の収録状況により題材エリアが変わる可能性あり（当日案内）。

---

## 発展②：deck.gl TerrainLayer／Cesium経路

```js
new deck.TerrainLayer({
  elevationData: "https://localhost:8000/terrain/{z}/{x}/{y}.png",
  elevationDecoder: { rScaler: 6553.6, gScaler: 25.6, bScaler: 0.1, offset: -10000 },
  texture: "..."   // 表面に貼るテクスチャ
});
```

- `elevationDecoder`に式を直接書く設計。エンコード方式の違いがコードに現れる
- 点群（第4回）や解析メッシュと同一シーンにしたい場合はこちらが向く

CesiumJSで地形を扱う場合はラスタータイルではなくquantized-mesh（第5回で触れたRe:earth Terrainが直結）。Terrain RGBタイルからの直接変換経路は一般的でないため、Cesiumが要件なら配信元の選択から設計する。

---

## 発展③：DEMをARで見る（参考・持ち帰り）

Terrain RGBをデコードして`PlaneGeometry`の頂点変位に使えば、卓上に地形模型を置くARが作れる（第3回のA-Frame環境の応用）。

- 屋内で完結し、GPS精度に依存しない「模型AR」が現実的
- 実地形に重ねる位置情報ARは、第3回で経験した方位・測位誤差がそのまま効いてくる

タイルの中身が数値であることを最も実感できる応用のひとつ。`99_ar_dem/`にアイディアと参考実装へのリンクをまとめています。

---

## 現地で使うときに確認すること

スマホブラウザで動かす前提なら、コードより先に運用面の確認事項が多い。

操作パネルは画面下端に寄せる（親指が届く）、現在位置はGeolocation API（第3回）で追従、WebGLとGPSの併用はバッテリー消費が大きい、直射日光下では白背景・高コントラストが読みやすい——このあたりは実際に外で使ってみると必要性がわかる。

```js
navigator.geolocation.watchPosition((pos) => {
  marker.setLngLat([pos.coords.longitude, pos.coords.latitude]);
}, null, { enableHighAccuracy: true });
```

そして最大の変数が現地の通信環境。次のスライドで整理する。

---

## 通信前提設計とオフライン設計の判断基準

まず「通信前提で足りるか」を検討する。オフライン化はコストが高い。

| 判断材料 | 通信前提でよい | オフライン設計が必要 |
|----------|---------------|---------------------|
| 調査地の電波 | 市街地・幹線道路沿い | 山間部・谷底 |
| 失敗時の影響 | 後日再訪できる | 再訪困難（船・許可が必要な場所） |
| データ量 | タイル都度取得で足りる | 広域を高ズームで見る必要がある |
| 利用者 | 自分（切り分けできる） | 配布先（トラブル対応できない） |

オフライン化の主な手段：

- ブラウザのHTTPキャッシュ：事前に対象範囲をなぞって温める（簡易・保証なし）
- Service Worker + Cache Storage：PWAとしてタイルを明示的に先読み保存
- タイル同梱＋ローカル配信：第2回のRaspberry Pi構成。確実だが機材を持ち歩く

---

## タイル容量の見積り（オフライン設計の第一歩）

```
必要容量 ≒ タイル数 × 平均タイルサイズ
タイル数は範囲(bbox)とズーム範囲から機械的に決まる
```

- z14まで市町村1つ分で数百MBになることもある。全域キャッシュは現実的ではない
- 調査対象範囲だけを先読みする設計（bbox指定）に落ち着くことが多い
- PMTilesなら`pmtiles extract --bbox=...`で範囲を切り出したファイルを作れる（Mapterhornの配布方式と同じ）
- iOS SafariのCache Storageには容量・保持期間の制約がある

どのレベルで自作するか（第2回）と同じ問い。要件が軽ければブラウザ任せ、確実性が要るならファイル同梱。

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
| 第2回 | 自前配信・スタイル | PMTiles配信・オフライン時のローカル配信 |
| 第3回 | スマホセンサー | 現在位置の追従・AR応用 |
| 第4回 | 3Dの描画基盤 | deck.gl・3D Tilesとの合成 |
| 第5回 | 高さデータの変換 | 今日の入力データすべて |

外部サービスの各機能がこの線のどこを肩代わりしているかを指させれば、採用・自作の判断は自分でできる。

---

## この先へ

- 正式な浸水解析・斜面解析への接続：GDAL/GRASS/SAGAの地形解析モジュール
- 点群（第4回）とDEM（第5〜6回）の統合：LiDAR点群からのDTM生成（第5回08参照）
- FOSS4Gコミュニティ：国内イベント・ソースコードリーディングは学習の近道
- 本セミナーの教材はすべてリポジトリに残ります。改変・再利用は自由です

質問・相談は本日のQ&Aのほか、セミナーSlackでも受け付けます。

### 全6回、お疲れさまでした。

---

## データの入手元のまとめ

| データ | 入手元 |
|--------|--------|
| DEM（元データ） | 基盤地図情報 数値標高モデル（国土地理院） |
| Terrain RGBタイル | 第5回で自作／Mapterhorn（比較用） |
| NDWIラスター | 配布データ（Sentinel-2由来、観測日はメタデータ参照） |
| 防災重点溜池 | 国土数値情報 ため池データ（国土交通省） |
| 筆ポリゴン | 農林水産省 筆ポリゴンオープンデータ |
| 建物3D Tiles | PLATEAU（国土交通省） |
| 背景地図 | OpenStreetMap contributors／地理院タイル |

公開・再配布するものには出典を明記する。ここまでの6回で扱ったデータはすべてオープンデータだが、オープンであることと出典表記が不要であることは別の話。
