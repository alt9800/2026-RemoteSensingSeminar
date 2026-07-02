# OSM・iD エディタ・現地調査への応用

---

## OSM のデータモデル

| 要素 | 説明 | 例 |
|---|---|---|
| ノード | 点。単独でPOI、ウェイの頂点としても使う | 駐車場・店舗・木 |
| ウェイ | ノードを繋いだ線。閉じると面になる | 道路・建物・公園 |
| リレーション | 複数要素の集合 | 行政区域・バス路線 |

タグは `key=value` の自由記述。よく使うタグは OSM Wiki で標準化されている。

```
amenity=parking     駐車場
capacity=20         収容台数
building=yes        建物（形状のみ）
highway=residential 住宅地の道路
name=○○公園         名称
```

---

## iD エディタ デモ手順

OSM アカウントが必要：https://www.openstreetmap.org/user/new

### POI の追加（駐車場を例に）

1. https://www.openstreetmap.org/ を開き「編集」をクリック
2. 左パネルの「ポイント」を選択してクリックで配置
3. 検索欄に「駐車場」と入力 → `Parking` を選択
4. `capacity`（収容台数）を入力
5. 「保存」→ チェンジセットコメントを入力して送信

### 建物の修正

1. 既存の建物をクリックして選択
2. 頂点をドラッグして実際の形状に合わせる
3. 保存

### 道路の属性編集

1. 道路をクリックして選択
2. 右パネルで `highway` タグの値を確認・変更
3. `name` タグに道路名を追加
4. 保存

---

## 現地調査ツールとしての iD エディタ

スマートフォンのブラウザからも編集できるため、現地でそのまま使える。

**向いているユースケース**

- 駐車台数・スペースの種別（障害者用・二輪等）の確認と入力
- 施設の営業時間・アクセス路の状態（舗装・未舗装）
- 登山道・作業道の存在確認と属性付与
- 建物用途の確認（`building:use` 等）

**向いていないユースケース**

- 高精度な測量が必要な境界線の編集（GPSの精度に依存）
- 大量データの一括入力（JOSM の方が向いている）

---

## OSM データをパイプラインに組み込む

```bash
# 1. GeoFabrik から対象エリアの PBF を取得
curl -L -o japan-latest.osm.pbf \
  https://download.geofabrik.de/asia/japan-latest.osm.pbf

# 2. osmium で対象エリアを切り出し
osmium extract \
  --bbox 130.8,33.8,131.3,34.3 \
  --output target.osm.pbf \
  japan-latest.osm.pbf

# 3. GeoJSON にエクスポート
osmium export \
  --geometry-types=linestring,polygon \
  --output=target.geojson \
  target.osm.pbf

# 4. tippecanoe で PMTiles 生成
tippecanoe \
  -o target.pmtiles \
  --force -z 17 -Z 10 \
  --drop-densest-as-needed \
  target.geojson
```

自分たちが iD エディタで整備したデータが数分〜数十分後に GeoFabrik に反映され、このパイプラインで取り込める。

---

## オフライン設計と PWA

### Service Worker によるタイルキャッシュ（概要）

```js
// service-worker.js
self.addEventListener('fetch', event => {
  // PMTiles へのリクエストをキャッシュから返す
  if (event.request.url.includes('.pmtiles')) {
    event.respondWith(
      caches.match(event.request)
        .then(cached => cached || fetch(event.request))
    );
  }
});
```

### 判断基準

| 状況 | 推奨設計 |
|---|---|
| 都市部・常時接続 | 通信前提（タイルサーバーに都度リクエスト） |
| 山岳・地下・海上 | PMTiles バンドル＋Service Worker キャッシュ |
| 更新頻度が高いデータ | 通信前提（キャッシュすると古くなる） |
| 現地調査アプリ | オフライン設計＋OSM 還元のハイブリッド |

---

## 参考リンク

- [OpenStreetMap](https://www.openstreetmap.org/)
- [iD エディタ ヘルプ](https://learnosm.org/ja/beginner/id-editor/)
- [OSM Wiki（タグ一覧）](https://wiki.openstreetmap.org/wiki/JA:Main_Page)
- [GeoFabrik ダウンロード](https://download.geofabrik.de/)
- [osmium-tool](https://osmcode.org/osmium-tool/)