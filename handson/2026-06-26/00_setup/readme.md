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
    --brand:      #9DE371;   /* ロゴのイエローグリーン */
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
  h1 { font-size: 2em; color: var(--navy); border: none; margin-bottom: 0.5em; }
  h2 {
    /* セクション内の中見出し */
    font-size: 1.3em; color: var(--teal);
    border-bottom: 2px solid var(--teal-light); padding-bottom: 0.2em;
  }
  h3 { font-size: 1.05em; color: var(--navy); }

  /* ── コードブロック ──────────────────────────────────── */
  code {
    font-family: "Courier New", monospace;
    background: #F0F0F0; padding: 0.1em 0.4em;
    border-radius: 3px; font-size: 0.88em; color: #2B2B2B;
  }
  pre {
    background: #F0F0F0; border-radius: 6px;
    padding: 0.8em 1em; font-size: 0.82em; line-height: 1.55;
  }
  pre code { background: none; padding: 0; }

  /* ── テーブル ────────────────────────────────────────── */
  table { width: 100%; border-collapse: collapse; font-size: 0.88em; }
  th { background: var(--navy); color: #ffffff; padding: 0.4em 0.7em; font-weight: bold; }
  td { padding: 0.4em 0.7em; border-bottom: 1px solid #e0e0e0; vertical-align: top; }
  tr:nth-child(even) td { background: var(--light); }

  /* ── ユーティリティクラス ────────────────────────────── */
  .label {
    /* スライド上部に置くセクション名ラベル */
    font-size: 0.7em; font-weight: bold; color: var(--teal);
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.2em;
  }
  .note {
    /* 補足・注意書き */
    font-size: 0.78em; color: #6B7280; font-style: italic; margin-top: 0.6em;
  }
  .warn { color: var(--red); font-weight: bold; }
  .ok   { color: var(--green); font-weight: bold; }

  /* ── タイトルスライド（_class: title）───────────────────
     白背景＋左帯でプロジェクター投影に配慮              */
  section.title {
    background: #ffffff; color: var(--navy);
    justify-content: flex-start; padding-top: 60px;
    border-left: 14px solid var(--brand);
  }
  section.title h1 { color: var(--navy); font-size: 1.4em; margin-bottom: 0.1em; }
  section.title h2 { color: var(--navy); font-size: 2.2em; border: none; margin-bottom: 0.2em; font-weight: bold; }
  section.title h3 { color: var(--teal); font-size: 1.2em; font-weight: normal; }
  section.title p  { color: var(--gray); font-size: 0.85em; }

  /* ── アクセントスライド（_class: dark）──────────────────
     名称は dark のまま互換性を保つ。
     白背景＋上帯でセクション区切りを示す。              */
  section.dark {
    background: #ffffff; color: var(--navy);
    justify-content: flex-start;
    border-top: 12px solid var(--brand); padding-top: 52px;
  }
  section.dark h1   { color: var(--gray); font-size: 1.1em; margin-bottom: 0.2em; font-weight: normal; }
  section.dark h2   { color: var(--navy); font-size: 1.9em; border: none; margin-bottom: 0.5em; font-weight: bold; }
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
| 0:10–0:25 | Nginx による静的配信設定（CORS 含む） |
| 0:25–0:45 | Maputnik でのスタイル設計 |
| **0:45–0:55** | **── 中休み ──** |
| 0:55–1:15 | MapLibre GL JS によるレンダリング実装 |
| 1:15–1:35 | デモ①：ラズパイタイルサーバーへの接続体験 |
| 1:35–1:55 | OSM エコシステム・iDエディタデモ・現地調査への応用 |
| 1:55–2:20 | デモ②：地理院地図ベクターの試行錯誤 |
| 2:20–2:30 | まとめ・次回への接続 |

---

<div class="label">ガイダンス</div>

# 本日の到達目標

- 外部タイルサービスに依存しない地図配信環境を自分で構築できる
- MapLibre Style Spec の構造を理解してスタイルを編集できる
- OSM のデータモデルを理解し、iD エディタで地物を編集できる

<br>

> 今日生成した PMTiles ファイルを持参・共有してください。前回の続きから始めます。

---

<div class="label">Nginx 静的配信</div>

# Nginx による PMTiles 配信

第1回で生成した `fude.pmtiles` を Nginx で配信する。

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/tiles;

    location / {
        # CORS 設定（MapLibre からのリクエストを許可）
        add_header Access-Control-Allow-Origin "*";
        add_header Access-Control-Allow-Methods "GET, OPTIONS";

        # PMTiles は Range Request が必須
        add_header Accept-Ranges bytes;

        try_files $uri $uri/ =404;
    }
}
```

```bash
sudo nginx -t      # 設定ファイルの文法チェック
sudo nginx -s reload
```

<div class="note">CORS を設定しないと MapLibre からのリクエストがブロックされる。詳細は handson/01_nginx/ を参照。</div>

---

<div class="label">Nginx 静的配信</div>

# CORS とは何か

**Cross-Origin Resource Sharing** — ブラウザのセキュリティ機構。

```
ブラウザ（example.com のページ）
  → tiles.example.com へリクエスト   ← 異なるオリジン
  → サーバーが Access-Control-Allow-Origin を返さないとブロック
```

PMTiles の Range Request は必ず異なるオリジンからの取得になるため CORS 設定が必要。

| ヘッダー | 設定値 | 意味 |
|---|---|---|
| `Access-Control-Allow-Origin` | `*` または特定ドメイン | どのオリジンを許可するか |
| `Accept-Ranges` | `bytes` | Range Request を受け付けると宣言 |

<div class="note">本番環境では `*`（ワイルドカード）ではなく許可ドメインを明示することを推奨。</div>

---

<div class="label">Maputnik</div>

# Maputnik でのスタイル設計

MapLibre Style Spec を GUI で編集できるオープンソースのスタイルエディタ。

```bash
# Web 版（インストール不要）
https://app.maputnik.com/

# ローカル版（Docker）
docker run -p 8888:8888 maputnik/editor
# → http://localhost:8888
```

### 基本的な操作の流れ

1. 「Open」→ URL から地理院地図ベクタータイルのスタイルを読み込む
2. レイヤーパネルで対象レイヤーを選択
3. Paint プロパティ（色・太さ・透明度）を変更
4. 「Export」→ `style.json` をダウンロード

```js
// エクスポートしたスタイルを MapLibre に渡す
map.setStyle('./style.json');
```

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
- `layers` — 描画レイヤーの定義（下から順に描画）
- `paint` — 色・サイズ・透明度（`layout` はシンボルの配置）
- 式（`["interpolate", ...]`）でズームや属性に応じて値を変化させられる

---

<!-- _class: dark -->

# デモ①

## ラズパイタイルサーバーへの接続体験

会場内の Raspberry Pi（Zero 2W / 3B+）に接続して、  
レスポンス速度の違いを体感してください。

接続先：（当日アナウンス）

- 同一 Wi-Fi に接続した状態でブラウザからアクセス
- DevTools の Network タブでレスポンスタイムを確認

<div class="note">Pi Zero 2W と 3B+ のサイドバイサイド比較も行います。</div>

---

<div class="label">デモ① — 補足</div>

# ラズパイタイルサーバーの構成

```
Raspberry Pi（OS Lite 64-bit）
├── Martin（Rust製タイルサーバー）
├── PMTiles（当該エリアの筆ポリゴン等）
├── Nginx（リバースプロキシ）
└── Tailscale（VPN・インターネット越しのアクセスに使用）
```

**ユースケース想定**：

- 遭難の多い山岳エリアの山小屋に設置
- 電波が届かない現地でも Wi-Fi 経由でタイル配信
- 登山者のスマートフォンから接続 → オフライン地図として機能

<div class="note">Pi Zero 2W（約2,000円）でも Martin は動作する。消費電力が低いためバッテリー運用も現実的。</div>

---

<div class="label">OSM エコシステム</div>

# OpenStreetMap とは

**誰でも編集できる地理空間データベース。**

| 項目 | 内容 |
|---|---|
| ライセンス | ODbL（Open Database License） |
| データ形式 | ノード・ウェイ・リレーションの3要素 |
| タグ体系 | `key=value` の自由記述（wiki で標準化） |
| 主な利用形態 | タイル配信・データエクスポート・ルーティング |

**データモデル**

```
ノード（点）  → POI・交差点
ウェイ（線）  → 道路・河川 / 閉じたウェイ → 建物・土地利用
リレーション  → 複数要素の集合（行政区域・路線など）
```

---

<div class="label">OSM エコシステム</div>

# iD エディタ デモ

ブラウザで動作する OSM の標準エディタ。現地調査ツールとしても使える。

**デモの流れ（5分）**

1. **POI の追加**：ノードを置いて `amenity=parking` + `capacity=20` を付与
2. **建物の修正**：ウェイの頂点をドラッグして形状を整える
3. **道路の属性編集**：既存のウェイを選択して `highway=residential` を確認・変更

**現地調査ツールとしての iD エディタ**

- GPS でノードを打ち、その場で属性を入力して OSM に還元できる
- 駐車場の台数・施設の開閉情報・アクセス路の状態など、現地でないと分からない情報の整備に向いている
- 収集したデータは GeoFabrik 等でエクスポートして自前の GIS に取り込める

<div class="note">編集には OSM アカウントが必要。事前に作成しておくとデモに参加できます。</div>

---

<div class="label">OSM エコシステム</div>

# OSM をデータパイプラインに組み込む

**第1回ハンズオンとの接続**

```
現地調査（iD エディタ）
  ↓ OSM に還元
  ↓ GeoFabrik でエクスポート（.osm.pbf）
  ↓ osmium extract で対象エリアを切り出し
  ↓ ogr2ogr で GeoJSON に変換
  ↓ tippecanoe で PMTiles 生成
  ↓ Nginx / Martin で配信
```

自分たちで整備したデータが、そのままタイル配信に乗る流れ。

---

<div class="label">OSM エコシステム</div>

# オフライン地図・PWA への応用

**タイルを事前にバンドルする設計**

```
通信前提の設計          オフライン設計
─────────────          ──────────────
タイルサーバーに         PMTiles を端末に
リクエスト              バンドルしておく
  ↓                       ↓
通信が必要             通信なしで動作
  ↓                       ↓
電波ない場所で不可     山小屋・地下でも可
```

**PWA（Progressive Web App）との組み合わせ**

- Service Worker で PMTiles をキャッシュ
- 初回通信時にタイルをダウンロード → 以降はオフラインで動作
- 現地調査アプリ（POI 入力 + 地図表示）が通信なしで完結

**判断基準：どちらを選ぶか**

| | 通信前提 | オフライン設計 |
|---|---|---|
| 更新頻度 | 高い（常に最新） | 低い（バンドル更新が必要） |
| インフラ | タイルサーバーが必要 | 静的ファイルのみ |
| 適したケース | 都市部・屋内 | 山岳・地下・海上 |

---

<!-- _class: dark -->

# デモ②

## 地理院地図ベクターの試行錯誤

地理院地図ベクタータイルのスタイルカスタマイズを  
ソースコードを見ながら解説します。

参考実装：https://alt9800.github.io/sample-maps/maplibre-catalog/

<div class="note">詳細な試行錯誤のメモは handson/02_maputnik/ および 04_gsi_vector/NOTES.md を参照。</div>

---

<div class="label">まとめ</div>

# 本日の到達確認

- [ ] Nginx で PMTiles を静的配信できた
- [ ] CORS の設定が必要な理由を説明できる
- [ ] Maputnik でスタイルを編集して MapLibre に反映できた
- [ ] OSM のデータモデル（ノード・ウェイ・リレーション）を説明できる
- [ ] iD エディタで POI・建物・道路を編集できた
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