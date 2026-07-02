# タイルのデータ構造とレンダリングパターン

第1回補足資料。

---

## MBTiles vs PMTiles の内部構造

### MBTiles

SQLite データベースファイル（`.mbtiles`）。
タイルは `tiles` テーブルに格納される。

```sql
-- MBTiles のスキーマ（抜粋）
CREATE TABLE tiles (
  zoom_level  INTEGER,
  tile_column INTEGER,
  tile_row    INTEGER,
  tile_data   BLOB,
  PRIMARY KEY (zoom_level, tile_column, tile_row)
);
```

- タイルへのアクセスは SQL クエリ経由
- インデックスは B-Tree（SQLite の標準構造）
- `tile_row` は TMS 形式（y 軸が南から）のため、MapLibre に渡す際は反転が必要な場合がある
- ブラウザから直接読み出せないため、タイルサーバーが必要（Martin・tileserver-gl 等）

### PMTiles

単一バイナリファイル（`.pmtiles`）。
タイルは**ヒルベルト曲線順**に連続配置される。

```
[ヘッダー（インデックス）]
  → タイル座標 → ファイル内バイトオフセット の対応表

[タイルデータ]
  → 各タイルのバイナリ（gzip または zstd 圧縮）が連続して格納
     配置順はヒルベルト曲線に従う
```

ブラウザは以下の手順でタイルを取得する：

```
1. ヘッダーを Range Request で取得（数KB程度）
2. 必要なタイルのバイトオフセットをインデックスから計算
3. そのバイト範囲だけを Range Request で取得
```

**ヒルベルト曲線を使う理由**

ヒルベルト曲線は空間的に近い座標を連続したインデックスに写す性質を持つ。
地図のズーム・パン操作で参照されるタイルは空間的に近傍に集まるため、
ヒルベルト曲線順の配置によりシーケンシャルな I/O で済む確率が上がる。

### 比較表

| | MBTiles | PMTiles |
|---|---|---|
| アーカイブ形式 | SQLite | 単一バイナリ |
| タイルのインデックス | B-Tree | ヒルベルト曲線ベースのオフセット表 |
| タイルへのアクセス | SQL クエリ | Range Request |
| ブラウザから直接配信 | 不可 | 可（HTTP サーバーのみで動作） |
| タイル圧縮 | gzip（列単位） | タイルごとに gzip / zstd |
| タイルサーバー | 必要（Martin・tileserver-gl 等） | 不要（Nginx・S3 等で静的配信可） |
| y 軸 | TMS（南が 0） | XYZ（北が 0） |
| ツールサポート | tippecanoe・GDAL・QGIS | tippecanoe（`-o *.pmtiles`）・GDAL 3.8+ |

---

## タイルの中身：MVT（Mapbox Vector Tile）

MBTiles・PMTiles のどちらであっても、ベクタータイルの場合の中身は MVT（protobuf バイナリ）で共通。

```
タイル 1 枚（.pbf / protobuf）
└── layer: "building"
    ├── extent: 4096          ← タイル座標系の解像度（0–4096）
    ├── feature
    │    ├── geometry: [移動コマンド + 座標のデルタ列]
    │    └── properties: {height: 20}
    └── feature ...
└── layer: "road"
    └── ...
```

座標は実際の緯度経度ではなく、タイル内の相対整数座標（0–4096）で格納される。
実座標への変換はクライアント（MapLibre 等）が担う。

---

## レンダリングパターン

地図をブラウザに表示する際のアーキテクチャは4パターンに分類できる。

### パターン A：ラスタータイル（画像配信）

```
サーバー側でレンダリング済みの PNG/JPEG をクライアントに送る

[データ] → [レンダリングサーバー] → PNG タイル → [ブラウザ]
                                                    ↓
                                              並べるだけ
```

- スタイルはサーバー側で固定される
- クライアントの処理は軽い
- 地図のカスタマイズはサーバー側の再生成が必要
- 代表例：地理院タイル・OSM tile.openstreetmap.org

### パターン B：ベクタータイル + クライアントレンダリング（本講義の主軸）

```
[データ] → tippecanoe → MVT/PMTiles → [ブラウザ]
                                         ↓
                                    MapLibre GL JS
                                    （WebGL でレンダリング）
                                         ↑
                                    style.json（スタイル定義）
```

- スタイルはクライアント側で自由に変更できる
- ズーム・パンが滑らか（GPU 描画）
- タイルサーバー不要（PMTiles ならば）
- 代表例：本講義の fude.pmtiles・地理院地図ベクタータイル

### パターン C：サーバーサイドレンダリング（ベクター→ラスター変換）

```
[MVT データ] → [tileserver-gl / MapLibre Native]
                    ↓ サーバー側でレンダリング
                PNG タイル → [ブラウザ]
```

- クライアントが WebGL を持たない環境（古いブラウザ・低スペック端末）向け
- tileserver-gl がこのパターンに対応
- スタイル変更のたびにサーバー側の再生成が必要

### パターン D：COG（Cloud Optimized GeoTIFF）による直接配信

```
[GeoTIFF（COG 形式）] → Range Request → [ブラウザ]
                                              ↓
                                        georaster-layer-for-leaflet
                                        / deck.gl BitmapLayer 等
```

- DEM（高さデータ）・衛星画像などラスターデータを PMTiles と同様の思想で配信する
- タイル化が不要な分、前処理コストが低い
- 第3〜4回（高さデータ）で扱う予定の COG と関連する

### 比較表

| | A：ラスタータイル | B：ベクター＋クライアント | C：サーバーサイド | D：COG |
|---|---|---|---|---|
| レンダリング場所 | サーバー | クライアント（GPU） | サーバー | クライアント |
| スタイル変更 | サーバー再生成が必要 | クライアントで即時 | サーバー再生成が必要 | 限定的 |
| クライアント負荷 | 低 | 中〜高 | 低 | 中 |
| データ形式 | PNG/JPEG タイル | MVT/PMTiles | MVT → PNG | GeoTIFF（COG） |
| タイルサーバー | 必要 | 不要（PMTiles の場合） | 必要 | 不要 |
| 主な用途 | 背景地図・衛星画像 | 地物・インタラクション | WebGL 非対応環境 | DEM・衛星画像 |

---

## tippecanoe が担う役割の整理

誤解されやすい点として、tippecanoe はベクターデータ（GeoJSON 等）をベクタータイル（MVT/PMTiles）に変換するツールであり、ラスターデータを扱えない。

```
対応：GeoJSON / FlatGeobuf / Newline-delimited GeoJSON
        ↓ tippecanoe
      MVT（.mbtiles または .pmtiles）

非対応：GeoTIFF・PNG・ラスターデータ一般
```

ラスターデータをタイル化する場合は GDAL（`gdal2tiles`・`rio-cogeo` 等）を使う。
この区別は第3〜4回（DEM/ラスター処理）で重要になる。