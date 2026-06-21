
# 筆ポリゴン → PMTiles 変換マニュアル

農水省 筆ポリゴン（宇部市）を MapLibre で表示するまでの手順

---

## 全体フロー

```
筆ポリゴン公開サイト
        ↓ GeoJSON ダウンロード
ogr2ogr（座標変換 EPSG:6668 → 4326）
        ↓ fude.geojson
tippecanoe（タイル生成）
        ↓ fude.pmtiles
MapLibre GL JS（ブラウザ表示）
```

**ツールの対応環境：**

| ツール | Windows | macOS / Linux |
|---|---|---|
| ogr2ogr | OSGeo4W または WSL | Homebrew / apt |
| tippecanoe | **WSL 必須** | Homebrew / apt |
| python | Python for Windows | 標準搭載 |

---

## 事前準備（Windows）

**OSGeo4W（ogr2ogr 用）**
https://trac.osgeo.org/osgeo4w/ からインストーラーをDL・実行

または QGIS をインストール済みであれば `QGIS > OSGeo4W Shell` で使用可能

**WSL2（tippecanoe 用）**
```powershell
# PowerShell（管理者）
wsl --install
```
再起動後、Ubuntu を開いて以下を実行：
```bash
sudo apt update
sudo apt install -y gdal-bin tippecanoe
```

**macOS**
```bash
brew install gdal tippecanoe
```

---

## データDL：筆ポリゴン公開サイト

1. https://open.fude.maff.go.jp にアクセス
2. 地図を対象エリアまでズームイン（1km以下で筆ポリゴンが表示される）
3. 右上パネル「筆ポリゴンデータ」→ **≡（リスト）アイコン** をクリック
4. パネル下部に展開されるテーブルビューで **ダウンロードアイコン** をクリック
5. GeoJSON 形式でダウンロードされる（例：`2026_352021.json`）

> ログイン不要、ユーザー登録不要
> ダウンロードURLの有効期限は **30分**

---

## Step 1：座標変換（EPSG:6668 → EPSG:4326）

筆ポリゴンの配布座標系は **JGD2011（EPSG:6668）**。
GeoJSON 仕様（RFC 7946）が要求する WGS84（EPSG:4326）に変換する。

**Windows（OSGeo4W Shell）/ macOS / Linux / WSL 共通：**
```bash
ogr2ogr \
  -f GeoJSON fude.geojson \
  2026_352021.json \
  -s_srs EPSG:6668 \
  -t_srs EPSG:4326
```

**確認：**
```bash
# macOS / Linux / WSL
ls -lh fude.geojson

# Windows PowerShell
Get-Item fude.geojson | Select-Object Length
```

> JGD2011 と WGS84 の差はcmオーダーだが、仕様準拠のため変換を行う

---

## Step 2：tippecanoe で PMTiles 生成

**macOS / Linux / WSL：**
```bash
tippecanoe \
  -o fude.pmtiles \
  --force \
  -z 17 -Z 10 \
  --drop-densest-as-needed \
  -l fude \
  fude.geojson
```

**Windows（WSL）の場合のパス指定：**
```bash
# Windows の Downloads フォルダを WSL から参照する例
cd /mnt/c/Users/<ユーザー名>/Downloads/tmp
# 同じコマンドを実行
```

**オプション早見表：**

| オプション | 意味 |
|---|---|
| `-z 17` | 最大ズームレベル |
| `-Z 10` | 最小ズームレベル（これ未満はタイルなし） |
| `--drop-densest-as-needed` | 500KB 超時にフィーチャーを自動間引き |
| `-l fude` | source-layer 名（MapLibre 側で参照する） |

---

## Step 3：index.html を作成

作業フォルダに `index.html` を作成：

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.css" rel="stylesheet">
  <script src="https://unpkg.com/pmtiles@3/dist/pmtiles.js"></script>
  <style> body { margin: 0; } #map { width: 100vw; height: 100vh; } </style>
</head>
<body>
<div id="map"></div>
<script>
  const protocol = new pmtiles.Protocol();
  maplibregl.addProtocol('pmtiles', protocol.tile);
  const map = new maplibregl.Map({
    container: 'map',
    style: {
      version: 8,
      sources: {
        osm: { type: 'raster',
          tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'], tileSize: 256 },
        fude: { type: 'vector', url: 'pmtiles://./fude.pmtiles' }
      },
      layers: [
        { id: 'osm', type: 'raster', source: 'osm' },
        { id: 'fude-fill', type: 'fill', source: 'fude',
          'source-layer': 'fude',   // tippecanoe の -l に合わせる
          paint: { 'fill-color': '#6ab04c', 'fill-opacity': 0.5 } }
      ]
    },
    center: [131.25, 33.95], zoom: 12
  });
</script>
</body>
</html>
```

---

## Step 3：ローカルサーバーを起動して確認

**macOS / Linux / WSL：**
```bash
python3 -m http.server 8000
```

**Windows（PowerShell）：**
```powershell
python -m http.server 8000
# または
npx serve .
```

ブラウザで **http://localhost:8000** を開く

> `file://` で直接開いても PMTiles は読み込めない（CORS制限）。
> 必ずローカルサーバー経由でアクセスすること。

---

## よくあるはまりポイント

**ポリゴンが表示されない**
→ `source-layer` の名前を確認。tippecanoe の `-l` で指定した文字列と一致する必要がある。
今回は `fude`。

**WSL 内のファイルを Windows から参照したい**
→ エクスプローラーのアドレスバーに `\\wsl$\Ubuntu\home\<ユーザー名>\` と入力

**ダウンロードURLが期限切れ**
→ 有効期限30分。筆ポリゴン公開サイトでダウンロードボタンを再クリックする。

**tippecanoe が Windows ネイティブで動かない**
→ Windows 向けの公式バイナリは存在しない。WSL2 を使うこと。