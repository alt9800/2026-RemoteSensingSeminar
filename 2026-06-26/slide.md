---
marp: true
theme: default
header: "衛星データ解析技術研究会<br>技術セミナー（応用編）第二回 2026/06/26"
footer: "第2回：タイル配信②：自前配信とカートグラフィック"
paginate: true
style: |
  /* ── カラー変数 ──────────────────────────────────────────
     第1回から継続。変更する場合はここだけ編集する。      */
  :root {
    --navy:       #1C3A4A;
    --teal:       #028090;
    --green:      #2D7D46;
    --red:        #B91C1C;
    --gray:       #374151;
    --light:      #F8FAFB;
    --teal-light: #E6F4F6;
    --brand:      #9DE371;
  }

  /* ── 通常スライドの基本スタイル ──────────────────────── */
  section {
    font-family: "Noto Sans JP", "Hiragino Sans", sans-serif;
    font-size: 20px;
    color: #1A1A1A;
    background: #ffffff;
    padding: 40px 56px;
  }

  /* ── 見出し ──────────────────────────────────────────── */
  h1 { font-size: 1.9em; color: var(--navy); border: none; margin-bottom: 0.4em; }
  h2 {
    font-size: 1.2em; color: var(--teal);
    border-bottom: 2px solid var(--teal-light); padding-bottom: 0.2em;
  }
  h3 { font-size: 1.0em; color: var(--navy); }

  /* ── コードブロック ──────────────────────────────────── */
  code {
    font-family: "Courier New", monospace;
    background: #F0F0F0; padding: 0.1em 0.4em;
    border-radius: 3px; font-size: 0.85em; color: #2B2B2B;
  }
  pre {
    background: #F0F0F0; border-radius: 6px;
    padding: 0.7em 1em; font-size: 0.78em; line-height: 1.5;
    margin: 0.4em 0;
  }
  pre code { background: none; padding: 0; }

  /* ── テーブル ────────────────────────────────────────── */
  table { width: 100%; border-collapse: collapse; font-size: 0.85em; }
  th { background: var(--navy); color: #ffffff; padding: 0.35em 0.6em; font-weight: bold; }
  td { padding: 0.35em 0.6em; border-bottom: 1px solid #e0e0e0; vertical-align: top; }
  tr:nth-child(even) td { background: var(--light); }

  /* ── ユーティリティ ──────────────────────────────────── */
  .label {
    font-size: 0.68em; font-weight: bold; color: var(--teal);
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.15em;
  }
  .note {
    font-size: 0.75em; color: #6B7280; font-style: italic; margin-top: 0.5em;
  }
  .warn { color: var(--red); font-weight: bold; }
  .ok   { color: var(--green); font-weight: bold; }

  /* ── タイトル・アクセントスライド ───────────────────── */
  section.title {
    background: #ffffff; color: var(--navy);
    justify-content: flex-start; padding-top: 60px;
    border-left: 14px solid var(--brand);
  }
  section.title h1 { color: var(--navy); font-size: 1.4em; margin-bottom: 0.1em; }
  section.title h2 { color: var(--navy); font-size: 2.2em; border: none; margin-bottom: 0.2em; font-weight: bold; }
  section.title h3 { color: var(--teal); font-size: 1.2em; font-weight: normal; }
  section.title p  { color: var(--gray); font-size: 0.85em; }

  section.dark {
    background: #ffffff; color: var(--navy);
    justify-content: flex-start;
    border-top: 12px solid var(--brand); padding-top: 48px;
  }
  section.dark h1   { color: var(--gray); font-size: 1.05em; margin-bottom: 0.2em; font-weight: normal; }
  section.dark h2   { color: var(--navy); font-size: 1.8em; border: none; margin-bottom: 0.5em; font-weight: bold; }
  section.dark li   { color: var(--gray); }
  section.dark .note { color: var(--teal); font-style: italic; }
---

<!-- _class: title -->
<!-- _paginate: false -->

<div class="label">リモセン応用セミナー WebGIS実装講座</div>

# 第2回

## タイル配信②
### 自前配信とカートグラフィック

---

<div class="label">本日の構成</div>

# タイムライン

| 時間 | 項目 |
|---|---|
| 0:00–0:10 | 前回成果物の確認・接続 |
| 0:10–0:30 | Nginx による静的配信設定（CORS 含む） |
| 0:30–0:50 | Maputnik でのスタイル設計 |
| **0:50–1:00** | **── 中休み ──** |
| 1:00–1:15 | MapLibre Style Spec とスタイルの渡し方 |
| 1:15–1:35 | デモ①：ラズパイタイルサーバーへの接続体験 |
| 1:35–1:55 | OSM エコシステム・iD エディタデモ |
| 1:55–2:20 | デモ②：地理院地図ベクターの試行錯誤 |
| 2:20–2:30 | まとめ・次回への接続 |

---

<div class="label">ガイダンス</div>

# 本日の到達目標

- 外部タイルサービスに依存しない地図配信環境を自分で構築できる
- MapLibre Style Spec の構造を理解してスタイルを編集できる
- OSM のデータモデルを理解し、iD エディタで地物を編集できる

<br>

> 前回生成した `fude.pmtiles` を持参・共有してください。

---

<div class="label">Nginx 静的配信</div>

# Nginx のインストール

```bash
# macOS
brew install nginx

# Linux (Ubuntu / Debian)
sudo apt install nginx

# Windows → WSL 内で Linux の手順を実行
```

動作確認：

```bash
nginx -v
# nginx/1.x.x

# macOS
brew services start nginx

# Linux
sudo systemctl start nginx
sudo systemctl status nginx
```

---

<div class="label">Nginx 静的配信</div>

# PMTiles を配信する設定

```nginx
server {
    listen 80;
    server_name _;
    root /var/www/tiles;

    location / {
        # CORS — MapLibre からのクロスオリジンリクエストを許可
        add_header Access-Control-Allow-Origin "*";
        add_header Access-Control-Allow-Methods "GET, OPTIONS";
        add_header Access-Control-Allow-Headers "Range";

        # Range Request を受け付けると宣言（PMTiles に必須）
        add_header Accept-Ranges bytes;

        if ($request_method = OPTIONS) { return 204; }
        try_files $uri $uri/ =404;
    }
}
```

```bash
sudo nginx -t        # 文法チェック
sudo nginx -s reload
```

---

<div class="label">Nginx 静的配信</div>

# CORS とは何か

**Cross-Origin Resource Sharing** — ブラウザのセキュリティ機構。

```
ブラウザ（example.com のページ）
  → tiles.example.com へリクエスト  ← 異なるオリジン
  → Access-Control-Allow-Origin がないとブロック
```

PMTiles の Range Request は必ずクロスオリジンになるため CORS 設定が必要。

| ヘッダー | 設定値 | 意味 |
|---|---|---|
| `Access-Control-Allow-Origin` | `*` | どのオリジンを許可するか |
| `Accept-Ranges` | `bytes` | Range Request を受け付けると宣言 |

<div class="note">本番環境では * ではなく許可ドメインを明示することを推奨。</div>

---

<div class="label">Nginx 静的配信</div>

# 動作確認

PMTiles をサーバーに配置して Range Request が通るか確認する。

```bash
sudo mkdir -p /var/www/tiles
sudo cp fude.pmtiles /var/www/tiles/

# Range Request の確認
curl -I -H "Range: bytes=0-511" http://localhost/fude.pmtiles
# HTTP/1.1 206 Partial Content が返れば OK
```

MapLibre からの接続：

```js
map.addSource('fude', {
  type: 'vector',
  url: 'pmtiles://http://サーバーIP/fude.pmtiles'
});
```

<div class="note">よくあるエラー：CORS error → ヘッダー確認 / 206 が返らない → Accept-Ranges 確認</div>

---

<div class="label">Maputnik</div>

# Maputnik とは

MapLibre Style Spec を GUI で編集できるオープンソースのスタイルエディタ。
編集結果を `style.json` でエクスポートし、そのまま MapLibre に渡せる。

```
# Web 版（インストール不要・本日はこちらを使用）
https://app.maputnik.com/

# ローカル版（Docker）
docker run -p 8888:8888 maputnik/editor
```

**今日の流れ**

1. 地理院地図ベクタータイルのスタイルを読み込む
2. 自前の `fude.pmtiles` をデータソースとして追加
3. レイヤーを追加して色・透明度を設定
4. `style.json` をエクスポートして MapLibre に渡す

---

<div class="label">Maputnik — Step 1</div>

# スタイルを読み込む

「Open」→「From URL」→ 以下を入力：

```
https://gsi-cyberjapan.github.io/gsivectortile-mapbox-gl-js/std.json
```

地理院地図ベクタータイルのスタイルが展開される。
左パネルにレイヤー一覧、中央にプレビューが表示される。

<br>

白紙から始める場合：「New Style」→「Empty Style」

---

<div class="label">Maputnik — Step 2</div>

# データソースを追加する

右上「Data Sources」→「Add New Source」

| フィールド | 入力値 |
|---|---|
| Source ID | `fude` |
| Source Type | Vector（TileJSON / PMTiles） |
| URL | `http://localhost:8000/fude.pmtiles` |

<br>

ローカルの PMTiles を参照するには事前にローカルサーバーが必要：

```bash
# fude.pmtiles と同じディレクトリで実行
python3 -m http.server 8000
```

---

<div class="label">Maputnik — Step 3</div>

# レイヤーを追加する

左パネル下部「＋ Add Layer」

| フィールド | 入力値 |
|---|---|
| Layer ID | `fude-fill` |
| Layer Type | Fill |
| Source | `fude` |
| Source Layer | `fude` |

<p class="warn">Source Layer の名前は tippecanoe の -l で指定した文字列と一致させる。</p>

---

<div class="label">Maputnik — Step 4</div>

# 色と透明度を設定する

レイヤーを選択 →「Paint」タブ

| プロパティ | 値 |
|---|---|
| `fill-color` | `#6ab04c` |
| `fill-opacity` | `0.5` |

**ズームに応じて変化させる：**

`fill-opacity` の右「＋」→「Zoom」を選択

| Zoom | 値 |
|---|---|
| 10 | 0.2 |
| 17 | 0.7 |

---

<div class="label">Maputnik — Step 5</div>

# エクスポートして MapLibre に渡す

「Export」→ `style.json` をダウンロード。

```js
// 初期化時に渡す
const map = new maplibregl.Map({
  container: 'map',
  style: './style.json'
});

// 後から切り替える
fetch('./style.json')
  .then(r => r.json())
  .then(style => {
    map.once('idle', () => map.setStyle(style));
  });
```

<div class="note">setStyle() 後にソース追加する場合は styledata より idle を使う。</div>

---

<div class="label">MapLibre Style Spec</div>

# スタイルファイルの構造

```json
{
  "version": 8,
  "sources": {
    "fude": { "type": "vector", "url": "pmtiles://./fude.pmtiles" }
  },
  "layers": [
    {
      "id": "fude-fill",
      "type": "fill",
      "source": "fude",
      "source-layer": "fude",
      "paint": {
        "fill-color": "#6ab04c",
        "fill-opacity": ["interpolate", ["linear"], ["zoom"], 10, 0.2, 17, 0.7]
      }
    }
  ]
}
```

- `sources` — データソースの定義
- `layers` — 下から順に描画
- 式（`["interpolate", ...]`）でズームや属性に応じて値を変化させられる

---

<div class="label">MapLibre Style Spec</div>

# スタイルの渡し方：2パターン

| | パターン① URL / JSON | パターン② インライン |
|---|---|---|
| 向いている場面 | Maputnik で作ったスタイルを使う | コードで管理したい |
| レイヤー定義 | JSON 側 | コード側 |
| PMTiles 直参照 | URL に書けば可 | `addProtocol()` が必要 |
| タイルの中身 | MVT（PBF） | MVT（PBF）← 同じ |

パターン②（インライン）：

```js
const protocol = new pmtiles.Protocol();
maplibregl.addProtocol('pmtiles', protocol.tile);

const map = new maplibregl.Map({
  container: 'map',
  style: {
    version: 8,
    sources: { fude: { type: 'vector', url: 'pmtiles://./fude.pmtiles' } },
    layers: [{ id: 'fude-fill', type: 'fill', source: 'fude',
               'source-layer': 'fude',
               paint: { 'fill-color': '#6ab04c', 'fill-opacity': 0.5 } }]
  }
});
```

---

<!-- _class: dark -->

# デモ①

## ラズパイタイルサーバーへの接続体験

会場内の Raspberry Pi 3B+ に接続して、オフライン配信を体感してください。

**接続先：（当日アナウンス）**

- 同一 Wi-Fi に接続した状態でブラウザからアクセス
- DevTools の Network タブでレスポンスタイムを確認
- ベクタータイルとラスタータイルの両方を配信しています

<div class="note">接続先は当日アナウンスします。</div>

---

<div class="label">デモ① — 補足</div>

# ラズパイタイルサーバーの構成

```
Raspberry Pi 3B+（OS Lite 64-bit）
├── Martin（Rust製タイルサーバー）
├── PMTiles（宇部市エリア：ベクター・ラスター）
├── Nginx（静的配信・CORS・Range Request 設定済み）
└── Tailscale（デモ前の動作確認・SSH用）
```

**ユースケース想定**：

- 遭難の多い山岳エリアの山小屋に設置
- 電波が届かない現地でも Wi-Fi 経由でタイル配信
- 登山者のスマートフォンから接続 → オフライン地図として機能

<div class="note">Pi 3B+ は消費電力が低くバッテリー運用も現実的。山小屋・避難小屋への常設を想定したサイズ感。</div>

---

<div class="label">OSM エコシステム</div>

# OpenStreetMap とは

**誰でも編集できる地理空間データベース。**

| 項目 | 内容 |
|---|---|
| ライセンス | ODbL（Open Database License） |
| データ形式 | ノード・ウェイ・リレーションの3要素 |
| タグ体系 | `key=value` の自由記述（Wiki で標準化） |
| 主な利用形態 | タイル配信・データエクスポート・ルーティング |

```
ノード（点）  → POI・交差点
ウェイ（線）  → 道路・河川 / 閉じたウェイ → 建物・土地利用
リレーション  → 複数要素の集合（行政区域・路線など）
```

---

<div class="label">OSM エコシステム</div>

# iD エディタ デモ（5分）

ブラウザで動作する OSM の標準エディタ。現地調査ツールとしても使える。

1. **POI の追加**：ノードを置いて `amenity=parking` + `capacity=20` を付与
2. **建物の修正**：ウェイの頂点をドラッグして形状を整える
3. **道路の属性編集**：`highway=residential` を確認・変更

**現地調査ツールとして**

- GPS でノードを打ち、その場で属性を入力して OSM に還元できる
- 駐車場の台数・アクセス路の状態など現地でないと分からない情報の整備に向く
- 収集データは GeoFabrik でエクスポートして自前 GIS に取り込める

<div class="note">編集には OSM アカウントが必要。事前に作成しておくとデモに参加できます。</div>

---

<div class="label">OSM エコシステム</div>

# オフライン地図・PWA への応用

| | 通信前提 | オフライン設計 |
|---|---|---|
| 仕組み | タイルサーバーに都度リクエスト | PMTiles を端末にバンドル |
| 更新頻度 | 高い（常に最新） | 低い（バンドル更新が必要） |
| 適したケース | 都市部・屋内 | 山岳・地下・海上 |

**PWA との組み合わせ**

Service Worker で PMTiles をキャッシュ → 初回通信後はオフラインで動作。  
現地調査アプリ（POI 入力 + 地図表示）が通信なしで完結する。

**第1回からの流れと接続**

```
iD エディタで現地編集 → OSM に還元 → GeoFabrik でエクスポート
  → tippecanoe で PMTiles 生成 → Nginx / Martin で配信
```

---

<!-- _class: dark -->

# デモ②

## 地理院地図ベクターの試行錯誤

地理院地図ベクタータイルのスタイルカスタマイズをソースコードを見ながら解説します。

参考実装：https://alt9800.github.io/sample-maps/maplibre-catalog/

<div class="note">詳細な試行錯誤のメモは 2026-06-19/handson/04_gsi_vector/NOTES.md を参照。</div>

---

<div class="label">まとめ</div>

# 本日の到達確認

- [ ] Nginx で PMTiles を静的配信できた
- [ ] CORS の設定が必要な理由を説明できる
- [ ] Maputnik でスタイルを編集して MapLibre に反映できた
- [ ] スタイルの渡し方2パターンの違いを説明できる
- [ ] OSM のデータモデル（ノード・ウェイ・リレーション）を説明できる
- [ ] 通信前提とオフライン設計のトレードオフを説明できる

---

<!-- _class: dark -->
<!-- _paginate: false -->

# 第3回（7/3）予告

## 高さデータ① リモートセンシングと高さデータのフォーマット・変換処理

- InSAR・LiDAR・SfM による DEM 生成の背景
- GeoTIFF / COG / LAS / LAZ フォーマットの整理
- GDAL を中心とした変換パイプライン
- Terrain RGB 形式への変換・タイル書き出し

<div class="note">使用データ（GeoTIFF）は事前に配布します。</div>