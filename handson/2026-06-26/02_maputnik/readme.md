# Maputnik でスタイルを編集する

MapLibre Style Spec を GUI で編集できるオープンソースのスタイルエディタ。
編集結果を JSON でエクスポートし、そのまま MapLibre に渡せる。

---

## Maputnik が扱う「スタイル」と「データソース」の分離

Maputnik は**スタイルエディタ**であり、地図データそのものは持っていない。必要なものが2つある：

```
① スタイル定義（style.json）
    「どのデータを、どんな色・形で描くか」のルール集

② タイルデータ
    「実際の道路・建物・水域の形状データ」
    → どこかのサーバーから URL で取得する
```

この2つは独立していて、スタイルの中に「どこからデータを取るか（URL）」が書かれている構造になっている。

---

## OSM・ベクタータイル・Maputnik の関係

OSM の生データをそのまま読んでいるわけではなく、ベクタータイルに変換・整理済みのものを参照している。

```
OSM（生データ：ノード・ウェイ・リレーション）
  ↓ tilemaker / tippecanoe 等で変換
ベクタータイル（MVT/PMTiles）
  source-layer: "road", "building", "water" ... に整理済み
  ↓ URL でアクセス
Maputnik の Data Sources に登録
  ↓ style.json で「road レイヤーをこの色で描く」と指定
MapLibre がレンダリング
```

---

## Maputnik での読み込みパターン

Maputnik の「Open」ダイアログには3つの読み込み方がある。

| 方法 | 使い方 | 用途 |
|---|---|---|
| ローカルファイル（Upload） | `style.json` をドラッグ＆ドロップ | 手元の style.json を編集したいとき |
| URL から読み込む | style.json の URL を入力（CORS 必要） | 地理院地図等の公開スタイルを読み込むとき |
| ギャラリー（Gallery） | Americana・Dark Matter 等を選択 | 既製スタイルをベースに始めるとき |

「公開ソースから選択」は別の操作で、Thunderforest・LocationIQ 等の有料/無料タイル API をデータソースとして追加するもの。スタイルではなくデータの参照先を追加する。

---

## 想定される開発スタイル

**A. 既製スタイル + 公開タイル（最も手軽）**
ギャラリーから Americana 等を選ぶ → OSM ベースのタイルがセットで付いてくる → 色を変えるだけ

**B. 既製スタイル + 自前タイル**
地理院地図の `std.json` を URL から読み込む → データソースは地理院サーバーの MVT → レイヤーの色・太さを編集する
→ デモ②（地理院地図ベクタータイルのカスタマイズ）のパターン

**C. 空スタイル + 自前 PMTiles**
Empty Style から始める → Data Sources に `localhost:8000/fude.pmtiles` を追加 → レイヤーを自分で定義する
→ 本ハンズオンのパターン

**D. 既存 style.json を編集してエクスポート**
手元の `style.json` をアップロード → 編集 → エクスポートして MapLibre に渡す

---

## Maputnik と PMTiles の関係

Maputnik はスタイルエディタなので、直接読み込めるのは `style.json` のみ。

| 操作 | 読み込めるか |
|---|---|
| style.json を Upload | ✓ 直接読み込める |
| fude.pmtiles を Upload | ✗ 読み込めない |
| fude.pmtiles を URL で参照 | ✓ ローカルサーバー経由で参照できる |

PMTiles はデータソースなので、Data Sources に URL を指定して参照する。
このとき `app.maputnik.com`（外部）が `localhost:8000`（ローカル）へリクエストするため、
**別オリジン間の通信が発生し CORS 設定が必要**になる。

---

## 推奨の出発点：OSM OpenMapTiles ギャラリーから始める

ハンズオンの入り口として最も手軽で直感的なパターン。
タイルデータもスタイルも揃っているため、ローカルサーバーも CORS 設定も不要でいきなり触れる。

**手順**

1. https://app.maputnik.com/ を開く
2. 「Open」→「ギャラリー」→「OSM OpenMapTiles」を選択
3. 左パネルのレイヤー一覧を眺める
4. `waterway`・`transportation` 等のレイヤーを選択して色を変えてみる

**色を変えた瞬間にリアルタイムで反映される** ので、スタイルとデータの関係が直感的に分かる。

### OpenMapTiles のスキーマと OSM タグの対応

OpenMapTiles は OSM の生タグをそのまま使わず、独自のレイヤー構造に整理している。

| OSM タグ | OpenMapTiles の source-layer | 補足 |
|---|---|---|
| `highway=rail` | `transportation` | `class=rail` でフィルター |
| `waterway=river` | `waterway` | そのまま |
| `amenity=station` | `poi` | `class=railway` でフィルター |
| `building=yes` | `building` | そのまま |
| `natural=water` | `water` | そのまま |

「railway」という source-layer は存在しない点に注意。地理院地図ベクタータイルでは `source-layer: "railway"` が存在するので、両者を見比べると構造の違いが分かりやすい。

---

## 自前の PMTiles を読み込む

OSM・地理院地図と同様に、自分で用意した PMTiles もデータソースとして読み込める。
ただし PMTiles はファイルとして直接アップロードできないため、**ホスティングが必要**。

```bash
# fude.pmtiles と同じディレクトリでローカルサーバーを起動
python3 -m http.server 8000
```

「Data Sources」→「Add New Source」→ 以下を入力：

```
Source ID  : fude
Source Type: Vector（TileJSON / PMTiles）
URL        : http://localhost:8000/fude.pmtiles
```

このとき `app.maputnik.com`（外部）から `localhost:8000`（ローカル）へのリクエストになるため、
Nginx に CORS 設定が必要になる（`01_nginx/README.md` 参照）。

---

## 3つのデータソースの比較

| データソース | 読み込み方法 | ホスティング | CORS |
|---|---|---|---|
| OSM OpenMapTiles | ギャラリーから選択 | 不要 | 不要 |
| 地理院地図ベクタータイル | URL（style.json）から読み込む | 不要 | 不要 |
| 自前 PMTiles | Data Sources に URL を入力 | **必要** | **必要** |

---

## 地理院地図ベクタータイルを読み込む

OSM 以外に、地理院地図のベクタータイルも Maputnik で編集できる。

「Open」→「URL から読み込む」→ 以下を入力：

```
https://gsi-cyberjapan.github.io/gsivectortile-mapbox-gl-js/std.json
```

こちらは地理院が公開しているスタイル JSON で、タイルデータも地理院サーバーから取得する。
OpenMapTiles とは異なる source-layer 名が使われているため、レイヤー一覧を眺めて構造を確認するとよい。

| source-layer | 内容 |
|---|---|
| `road` | 道路 |
| `railway` | 鉄道（OpenMapTiles とは異なり独立したレイヤーとして存在） |
| `waterarea` | 水域（池・湖等） |
| `river` | 河川 |
| `building` | 建物 |
| `boundary` | 行政境界 |

**OpenMapTiles との比較で気づくこと**

- 地理院地図は `railway` が独立したレイヤー → `transportation` の `class` フィルター不要
- 日本固有のデータ（海岸線・標高由来の地形表現等）が含まれる
- レイヤー数は地理院地図の方が多く、スタイル JSON も大きい

---

## 準備

```bash
# fude.pmtiles と同じディレクトリでローカルサーバーを起動
python3 -m http.server 8000
```

ブラウザで https://app.maputnik.com/ を開く。

---

## Step 1：スタイルを読み込む

「Open」→「From URL」→ 以下を入力して読み込む：

```
https://gsi-cyberjapan.github.io/gsivectortile-mapbox-gl-js/std.json
```

地理院地図ベクタータイルのスタイルが Maputnik 上に展開される。
左パネルにレイヤー一覧、中央にプレビューが表示される。

白紙から始める場合は「New Style」→「Empty Style」を選ぶ。

---

## Step 2：自前のデータソースを追加する

右上の「Data Sources」→「Add New Source」

```
Source ID  : fude
Source Type: Vector（TileJSON / PMTiles）
URL        : http://localhost:8000/fude.pmtiles
```

---

## Step 3：レイヤーを追加する

左パネル下部「＋ Add Layer」

```
Layer ID    : fude-fill
Layer Type  : Fill
Source      : fude
Source Layer: fude       ← tippecanoe の -l に対応
```

---

## Step 4：色と透明度を設定する

レイヤーを選択 →「Paint」タブ

```
fill-color   : #6ab04c
fill-opacity : 0.5
```

ズームに応じて透明度を変化させる場合：
`fill-opacity` の右の「＋」→「Zoom」を選択

```
zoom 10 → 0.2
zoom 17 → 0.7
```

---

## Step 5：エクスポートして MapLibre に渡す

「Export」→ `style.json` をダウンロード。

```js
// 初期化時にそのまま渡す
const map = new maplibregl.Map({
  container: 'map',
  style: './style.json'
});

// 後から切り替える場合
fetch('./style.json')
  .then(r => r.json())
  .then(style => {
    map.once('idle', () => map.setStyle(style));
  });
```

---

## 補足：スタイルの渡し方2パターン

Maputnik のエクスポートは**パターン①**の形になる。

| | パターン① URL / JSON ファイル | パターン② インラインオブジェクト |
|---|---|---|
| 向いている場面 | Maputnik で作ったスタイルを使う | コードで全部管理したい |
| レイヤー定義 | JSON 側 | コード側 |
| `pmtiles://` | URL に書けば可 | `addProtocol()` の事前登録が必要 |
| タイルの中身 | MVT（PBF） | MVT（PBF）← 同じ |

パターン②（インライン）の例：

```js
const protocol = new pmtiles.Protocol();
maplibregl.addProtocol('pmtiles', protocol.tile);

const map = new maplibregl.Map({
  container: 'map',
  style: {
    version: 8,
    sources: {
      fude: { type: 'vector', url: 'pmtiles://./fude.pmtiles' }
    },
    layers: [
      {
        id: 'fude-fill', type: 'fill', source: 'fude',
        'source-layer': 'fude',
        paint: { 'fill-color': '#6ab04c', 'fill-opacity': 0.5 }
      }
    ]
  }
});
```

---

## 補足：setStyle() のタイミング

スタイル切り替え後にソースやレイヤーを追加する場合は `styledata` より `idle` を使う。

```js
map.setStyle(newStyle);
map.once('idle', () => {
  // ここでソース・レイヤーを追加する
});
```

地理院地図ベクタータイルのカスタマイズで確認済み。
詳細 → `2026-06-19/handson/04_gsi_vector/NOTES.md`