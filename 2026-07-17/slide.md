---
marp: true
theme: default
header: "衛星データ解析技術研究会<br>技術セミナー（応用編）第四回 2026/07/17"
footer: "第4回 3D技術②：点群・3DGSのWeb可視化"
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

## 第4回 3D技術②
## 点群・3DGSのWeb可視化

### 2026年7月17日（金）

到達目標：3Dデータのフォーマットと処理パイプラインを説明できる／deck.glで点群をWeb地図上に表示できる／3DGSの現状と入口を把握する

---

## 本日のタイムテーブル（140分）

| 時間 | 内容 |
|------|------|
| 10分 | イントロ・3Dデータフォーマット比較（3D Tiles / glTF / Potree / COPC） |
| 15分 | CesiumJS・Re:Earth の位置づけと活用事例（文化財・インフラ点検） |
| 35分 | ハンズオン①：CloudCompare → PotreeConverter → Web公開 |
| 10分 | 休憩 |
| 30分 | ハンズオン②：deck.gl PointCloudLayer で点群を地図上に表示 |
| 15分 | 3DGS概説（Scaniverse / Luma AI、CesiumJSとの統合動向） |
| 15分 | 振り返り・Q&A |

<div class="note">前回（第3回）はスマホのセンサーを「入力」として使った。今回は3Dデータを「出力」としてブラウザに描く回。</div>

---

## 前回までとのつながり

- 第1〜2回：**2Dのタイル配信**
  - タイルピラミッド・PMTiles・Nginxによる静的配信
- 第3回：**スマホセンサーとAR**
  - Geolocation / DeviceOrientation、カメラ映像への重ね表示
- 第4回（今日）：**3Dデータそのものを扱う**
  - 点群という「巨大な点の集まり」をどう配信・描画するか

2Dタイルで学んだ考え方（**階層化して必要な分だけ読む**）は、3Dでもそのまま生きる。タイルピラミッドの3D版が今日の主役のひとつ「octree（八分木）」。

---

# 1. 3DデータのフォーマットとWebGIS

---

## Webで3Dを扱うときの根本的な問題

- LiDARスキャン1回で **数百万〜数億点** の点群が生まれる
- LASファイルで数GB規模になることも珍しくない
- ブラウザに全部読み込むのは不可能

→ 2Dタイルと同じ発想が必要になる

| 2Dの世界 | 3Dの世界 |
|----------|----------|
| タイルピラミッド（z/x/y） | octree（八分木）による空間分割 |
| ズームレベルに応じて解像度を切替 | カメラ距離に応じてLOD（詳細度）を切替 |
| PMTiles / MVT | 3D Tiles / Potree / COPC |
| Range Request で必要な部分だけ取得 | 同じく必要なノードだけ取得 |

---

## 主要フォーマットの整理（1/2）：交換用と配信用

まず「**編集・交換のためのフォーマット**」と「**Web配信のためのフォーマット**」を区別する。

| 分類 | フォーマット | 特徴 |
|------|--------------|------|
| 交換用（点群） | LAS | LiDAR業界標準。非圧縮でサイズ大 |
| 交換用（点群） | LAZ | LASの可逆圧縮版。1/5〜1/10程度に |
| 交換用（メッシュ） | glTF / GLB | 「3DのJPEG」と呼ばれる汎用3Dモデル形式。テクスチャ・マテリアル込み |
| 配信用 | 3D Tiles | Cesium発のOGC標準。glTFをタイル化して階層配信 |
| 配信用 | Potree形式 | 点群専用。octree構造で分割済み |
| 配信用 | COPC | LAZ 1.4の中にoctree索引を埋め込んだ単一ファイル |

<div class="note">第1回のPMTilesと同様、COPCも「単一ファイル + Range Request」という設計思想。系譜としてはCOG（第5回で扱う）の点群版にあたる。</div>

---

## 主要フォーマットの整理（2/2）：使い分けの目安

| やりたいこと | 選択肢 |
|--------------|--------|
| スキャンした点群をまず手元で見る・編集する | LAS / LAZ + CloudCompare |
| 点群をWebで公開する（専用ビューア） | Potree形式 + Potreeビューア |
| 点群をWebで公開する（静的ファイル1個で） | COPC |
| 建物・都市モデルなどメッシュを配信する | 3D Tiles（中身はglTF） |
| 単体の3Dモデルを埋め込む | glTF / GLB |

- **Potree形式**：`metadata.json` + `octree.bin` + `hierarchy.bin` の構成（PotreeConverter 2系）
- **3D Tiles**：`tileset.json` がタイルの階層を記述。PLATEAUの建物データもこの形式で配信されている

---

## 3D Tilesをもう少しだけ

- Cesium社が策定し、**OGC Community Standard** として標準化
- ルートの `tileset.json` から子タイルを辿る階層構造
- 各タイルの中身は glTF（3D Tiles 1.1 以降）
- **PLATEAU**（国土交通省の3D都市モデル）の配信形式として国内でも実質標準

```json
// tileset.json の骨格（抜粋イメージ）
{
  "root": {
    "boundingVolume": { "region": [...] },
    "geometricError": 500,
    "content": { "uri": "building.glb" },
    "children": [ ... ]
  }
}
```

`geometricError` がLOD切替の閾値。「カメラから見てこの誤差が目立つ距離まで近づいたら子タイルを読む」という仕組み。

---

# 2. レンダリングエンジンの位置づけ

---

## WebGLベースの3D GISエンジン比較

| エンジン | 得意分野 | 特徴 |
|----------|----------|------|
| CesiumJS | 地球儀・3D Tiles | 3D Tilesの本家。地形・時間軸・衛星軌道まで扱える |
| deck.gl | データ可視化レイヤー | MapLibre等と重ねられる。点群はPointCloudLayer |
| Potree | 点群専用ビューア | 巨大点群の表示に特化。計測ツール内蔵 |
| Three.js | 汎用3D | GISではないが、上記全ての基盤的存在 |
| Re:Earth | ノーコードWebGIS | CesiumJSベース。国産OSS。プラグインで拡張 |

- CesiumJS：**「地球の上に載せる」ことが前提**の設計。座標系・地形・カメラ制御が最初から地理空間仕様
- deck.gl：**「地図の上にレイヤーを重ねる」**発想。第2回までのMapLibreの延長線上で使える
- 今日のハンズオンではPotree（①）とdeck.gl（②）を使う

---

## 活用事例：なぜ点群をWebで見せたいのか

**文化財**
- 文化財の3D計測・アーカイブ（劣化前の記録、修復の基礎資料）
- 公開・展示：現地に行けない人への提供、教育利用

**建築・BIM**
- 竣工時点群と設計モデル（BIM）の照合
- 改修工事前の現況把握（図面がない古い建物）

**インフラ点検**
- 橋梁・トンネル・法面のスキャンによる変状把握
- 定期点検結果の時系列比較

共通するのは「**現場に行かずに・複数人で・ブラウザだけで**確認したい」という要求。専用ソフトのインストールを関係者全員に求めるのは現実的でない場面が多い。

---

## リモートセンシングとの接点

- 航空LiDAR測量の成果は点群（LAS/LAZ）で提供される
  - 例：林野庁・自治体による森林資源解析用データ
- 衛星・航空写真からのSfM（Structure from Motion）でも点群が生成される
- 第5回で扱うDEM/DSMの多くは、**点群を内挿・ラスタライズしたもの**が起点

今日の内容は「ラスタライズされる前の生データを直接扱う」回とも言える。

<div class="note">静岡県の「VIRTUAL SHIZUOKA」のように、県単位で点群をオープンデータ公開する事例もある（G空間情報センターで配布）。</div>

---

<!-- _class: dark -->

# ハンズオン①

## CloudCompare → PotreeConverter → Web公開

<span class="note">目標：手元の点群をブラウザで見られる状態にする（35分）</span>

---

## ハンズオン①の全体像

```
モバイルLiDARスキャン（iPhone/iPad Pro + Scaniverse等）
        │  LAS / PLY / E57 でエクスポート
        ▼
CloudCompare        … 確認・間引き・ノイズ除去・座標調整
        │  LAS で書き出し
        ▼
PotreeConverter     … octree構造への変換
        │  metadata.json / octree.bin / hierarchy.bin
        ▼
静的Webサーバー      … Nginx / GitHub Pages / python -m http.server
        ▼
Potreeビューア（ブラウザ）
```

第2回でやった「PMTilesをNginxで静的配信」と構図は同じ。**変換さえ済めば、あとは静的ファイルを置くだけ**。

---

## 教材データについて

- 事前にスキャン済みの点群データ（LAS）を配布します
  - `handson/01_potree/data/` 以下に配置
- 自分のスキャンデータを使いたい方
  - iPhone Pro / iPad Pro（LiDAR搭載機）+ Scaniverse で取得可能
  - ScaniverseからLAS形式でエクスポート → AirDrop等でPCへ

<span class="warn">注意：</span>モバイルLiDARの点群は**ローカル座標系**（スキャン開始点が原点）。地図に重ねるには後で座標を与える必要がある。ハンズオン②で扱う。

---

## Step 1：CloudCompareで点群を開く

CloudCompareは点群処理のFOSSデファクト（GPL）。

1. `File > Open` でLASファイルを読み込み
2. Global Shift の確認ダイアログ → そのまま `Yes`
   - 座標値が大きい場合に精度落ちを防ぐための内部オフセット
3. 表示確認：マウスドラッグで回転、ホイールでズーム

確認するポイント：

- 点数（プロパティパネルの `Points` ）
- 明らかなノイズ（空中に浮いた点、鏡面反射由来の点）
- RGBが載っているか（Scaniverse由来なら通常あり）

---

## Step 2：間引きとノイズ除去

Webで扱いやすいサイズにするための前処理。

**間引き（Subsample）**
- `Edit > Subsample`
- `Space` を選び、点間の最小距離を指定（例：0.01 = 1cm間隔）
- 数千万点 → 数百万点程度まで落とすのが目安

**ノイズ除去（SOR Filter）**
- `Tools > Clean > SOR filter`
- 各点の近傍点との距離の統計から外れ値を除去
- デフォルト値（近傍6点・nSigma 1.00）でまず試す

処理後、`File > Save` でLAS形式で書き出し（例：`scan_clean.las`）。

---

## Step 3：PotreeConverterで変換

PotreeConverter 2系はシングルバイナリ。GitHubのReleasesから取得済みのものを配布します。

```sh
# 基本形
./PotreeConverter scan_clean.las -o ./potree_output

# 出力されるファイル
potree_output/
├── metadata.json    # 点群のメタ情報（範囲・属性・点数）
├── octree.bin       # 点データ本体（octreeノード順に格納）
└── hierarchy.bin    # octreeの階層構造の索引
```

- 変換時間の目安：数百万点で数十秒程度
- 出力は**この3ファイルだけ**。PMTilesと同じく「静的ファイル一式」になる

<div class="note">PotreeConverter 1系はディレクトリに大量の小ファイルを吐く方式だった。2系で単一binファイル + Range Request方式に変わり、配信効率が大きく改善された。</div>

---

## Step 4：Potreeビューアで表示

Potreeビューア本体（HTML/JS/CSS一式）は配布物に同梱しています。

```html
<!-- viewer.html の要点のみ抜粋 -->
<script>
  const viewer = new Potree.Viewer(
    document.getElementById("potree_render_area")
  );
  viewer.setPointBudget(2_000_000);  // 同時表示する最大点数

  Potree.loadPointCloud(
    "./potree_output/metadata.json",  // 変換結果を指定
    "scan",
    (e) => {
      viewer.scene.addPointCloud(e.pointcloud);
      viewer.fitToScreen();
    }
  );
</script>
```

ローカル確認は `python3 -m http.server 8000` などで。`file://` 直接開きは<span class="warn">不可</span>（fetchが失敗する。第1回のPMTilesと同じ理由）。

---

## Step 5：公開する

静的ファイルなので、第2回で構築した知識がそのまま使える。

| 公開先 | 備考 |
|--------|------|
| GitHub Pages | リポジトリに置くだけ。ただし1ファイル100MB制限に注意 |
| Nginx（自前サーバー） | Range Request対応は標準で問題なし |
| Raspberry Pi | 第2回のPi構成にディレクトリを足すだけ |

`pointBudget` の値と初期視点（`fitToScreen` か固定カメラか）は、見せたい相手の回線・端末に合わせて調整する。

**ここまでで「スキャン → Web公開」の一連のパイプラインが完成。**

---

<!-- _class: dark -->

# 休憩（10分）

## 再開後：deck.glで点群を「地図の上に」置く

---

<!-- _class: dark -->

# ハンズオン②

## deck.gl PointCloudLayer で点群を地図上に表示

<span class="note">目標：MapLibreの地図と点群を重ねて表示する（30分）</span>

---

## Potreeとdeck.glの役割の違い

| | Potree | deck.gl |
|---|--------|---------|
| 主目的 | 点群単体をじっくり見る | 地図・他レイヤーと組み合わせる |
| 背景地図 | なし（点群のみ） | MapLibre等と統合 |
| 巨大点群 | octreeで数億点も可 | メモリに載る規模（数百万点まで）が現実的 |
| 座標系 | ローカル座標のままでよい | 地理座標（経緯度）が必要 |

deck.glで地図に重ねるには、**点群に地理座標を与える**必要がある。ここがハンズオン②の山場。

---

## 点群に地理座標を与える

モバイルLiDARの点群はローカル座標（原点 = スキャン開始地点、単位 = m）。

今回の方針：**スキャン地点の経緯度を基準点として、ローカル座標をオフセットとして扱う**。

```js
// deck.glのcoordinateSystemを使う
new PointCloudLayer({
  id: "scan",
  data: points,
  coordinateSystem: COORDINATE_SYSTEM.METER_OFFSETS,
  coordinateOrigin: [131.2470, 33.9520],  // スキャン地点の経緯度
  getPosition: (d) => [d.x, d.y, d.z],    // ローカル座標（m）のまま渡せる
  getColor: (d) => [d.r, d.g, d.b],
  pointSize: 2,
});
```

`METER_OFFSETS` を使うと「基準点からのメートル単位のずれ」として解釈されるため、ローカル座標の点群を再投影なしで地図に載せられる。

<div class="note">厳密な位置合わせ（向きの回転・標高合わせ）が必要な場合はCloudCompareの Translate/Rotate で事前調整するか、modelMatrixで回転を与える。今日は概念の理解を優先する。</div>

---

## LASをブラウザで読む：loaders.gl

deck.glと同じ開発元の **loaders.gl** がLAS/LAZのパーサーを提供している。

```html
<script src="https://unpkg.com/deck.gl@9/dist.min.js"></script>
<script src="https://unpkg.com/@loaders.gl/las@4/dist/dist.min.js"></script>
```

```js
const {DeckGL, PointCloudLayer, COORDINATE_SYSTEM} = deck;
const {LASLoader} = loaders;

new PointCloudLayer({
  id: "scan",
  data: "./scan_clean.las",   // URLを直接渡す
  loaders: [LASLoader],        // パースはloaders.glに任せる
  coordinateSystem: COORDINATE_SYSTEM.METER_OFFSETS,
  coordinateOrigin: [131.2470, 33.9520],
  getColor: (d) => d.color ?? [100, 100, 100],
  pointSize: 2,
});
```

CSVやJSONへの変換を挟まず、**LASファイルをそのまま静的配信して直接読める**のが利点。

---

## MapLibreとの統合

第2回までのMapLibre構成に、deck.glをオーバーレイとして追加する。

```js
const map = new maplibregl.Map({
  container: "map",
  style: "https://demotiles.maplibre.org/style.json",
  center: [131.2470, 33.9520],
  zoom: 17,
  pitch: 60,          // 3D表示のため傾ける
});

const overlay = new deck.MapboxOverlay({
  interleaved: true,  // 地図と同じWebGLコンテキストで描画
  layers: [pointCloudLayer],
});
map.addControl(overlay);
```

- `pitch` を上げないと点群のZ方向が見えない
- `interleaved: true` で地形・建物との前後関係が正しく描画される

**完成形：宇部市の地図の上に、自分でスキャンした点群が立ち上がる。**

---

## つまずきポイント（先回りメモ）

| 症状 | 原因と対処 |
|------|-----------|
| 点群が表示されない | `coordinateOrigin` と地図の `center` が離れすぎている。まず両方を同じ値に |
| 点が真っ黒/真っ白 | 色属性が無い、または16bit RGB。`getColor` で `d.color` の中身を`console.log`で確認 |
| 点群が地面にめり込む | Z原点のずれ。`getPosition` で `d.z + オフセット` を足して調整 |
| ページが固まる | 点数が多すぎる。CloudCompareの間引きに戻る |
| CORSエラー | 第2回の復習。配信元のレスポンスヘッダーを確認 |

---

# 3. 3D Gaussian Splatting（3DGS）概説

---

## 3DGSとは何か

2023年のSIGGRAPH論文を起点に急速に普及した、新しい3Dシーン表現。

- 点群：シーンを「**色付きの点**」の集合で表す
- 3DGS：シーンを「**大きさ・向き・透明度を持つ楕円体（ガウシアン）**」の集合で表す

| | 点群（LiDAR） | 3DGS |
|---|--------------|------|
| 取得方法 | レーザー測距 | 複数枚の写真から学習 |
| 幾何精度 | 高い（測量に使える） | 見た目優先（寸法保証なし） |
| 見た目 | 点の隙間が見える | 写実的。反射・透過も再現 |
| データの性質 | 座標 + 色 | 座標 + 共分散 + 球面調和係数 |

**「測る」なら点群、「見せる」なら3DGS**、という住み分けが現時点の目安。

---

## 3DGSを体験する最短ルート：SaaS

学習（トレーニング）には本来GPUが必要だが、スマホアプリ・SaaSがその部分を肩代わりしてくれる。

| サービス | 特徴 |
|----------|------|
| Scaniverse | LiDARスキャンに加えて3DGSモードを搭載。端末内処理 |
| Luma AI | 動画をアップロードするとクラウドで3DGS化。Web埋め込み可 |
| Polycam | 写真測量・LiDAR・3DGSを統合したアプリ |

体験の手順（Scaniverseの例）：

1. アプリでSplatモードを選び、対象の周囲をゆっくり一周撮影
2. 端末内で処理（数分）
3. `.ply` / `.spz` 形式でエクスポート可能

---

## 3DGSとWebGIS：統合の動向

3DGSを「地図の上に置く」動きが2024年以降活発化している。

- **CesiumJS**：3D Tilesの拡張として3DGSタイルのサポートを進めている
  - 巨大な3DGSシーンをタイル分割・ストリーミングする方向性
- **SPZ形式**：Niantic（現Niantic Spatial）が公開した3DGS圧縮形式。PLYの1/10程度
- **deck.gl / Three.js**：コミュニティ製のsplatレンダラーが複数存在

現状の整理：

- フォーマットの標準化は**まだ過渡期**（PLY派生・SPZ・3D Tiles拡張が並立）
- 「点群のPotreeConverter」に相当する定番変換ツールは確立途上
- ただし方向性は明確：**3D Tilesのエコシステムに合流していく**見込み

<div class="note">数年前のベクタータイル（MVT前夜）に似た状況。標準が固まる前でも、パイプラインの考え方（取得 → 変換 → 階層化 → 静的配信）は共通しているので、今日学んだ構図はそのまま応用できる。</div>

---

## 振り返り：今日の到達点

- **フォーマット**：交換用（LAS/LAZ/glTF）と配信用（3D Tiles/Potree/COPC）を区別できる
- **パイプライン**：スキャン → CloudCompare → PotreeConverter → 静的配信、を自分の手で完走した
- **地図統合**：deck.gl の `METER_OFFSETS` でローカル座標の点群を地図に載せた
- **3DGS**：点群との使い分けと、3D Tilesエコシステムへの合流という潮流を把握した

一貫していたのは第1回からの構図：

**巨大なデータを、階層化して、静的ファイルとして配信する。**

---

## 次回予告：第5回 高さデータ①

- リモートセンシングによる高さデータ（DEM/DSM）の生成原理
  - InSAR・LiDAR・SfM
- GeoTIFF / COG / LAS / LAZ のフォーマット構造
- GDALによる変換パイプライン：座標変換 → クリッピング → Terrain RGBタイル化

今日扱った点群は、内挿・ラスタライズを経てDEM/DSMになる。**第4回と第5回はデータの連続体**として見てほしい。

7/24（金）同時刻・同会場。

---

<!-- _class: title -->

# お疲れさまでした

## 質疑応答

### ハンズオンで完走できなかった方は `handson/` 以下のREADMEに全手順があります

リポジトリ：github.com/alt9800/2026-RemoteSensingSeminar