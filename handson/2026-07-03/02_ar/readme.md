# ハンズオン② 農地レイヤーAR（筆ポリゴン・半径250m）

位置情報ベースのARで、現在地から半径250m以内の農地区画（筆ポリゴンから変換したGeoJSON）を、
輪郭線とラベルとしてカメラ映像に重ねて表示する。AR.js のロケーションベース系コンポーネント
（`gps-new-camera` / `gps-new-entity-place`）は使わず、GPS座標からのオフセット計算と方位
センサーによるカメラ回転を組み合わせて実装している。

## 学習目標

- 緯度経度で表現された地物を、GPSの現在地を基準にAR空間の座標へ変換する処理を、
  ライブラリの自動配置に頼らず自分で実装できる。
- 位置情報ベースARの精度上の限界（GPS誤差数メートル、方位センサーの系統的なズレ）を理解し、
  現場での較正で対処する判断ができる。
- GeoJSONの構造要件（`polygon_uuid` / `point_lat` / `point_lng`）を理解し、他の地域・
  他のデータセットにも適用できる。

## 動かすもの

アプリ本体は [`app/index.html`](./app/)。既定では `app/ube.geojson` を読み込むが、開始画面
でファイルを選択すれば任意のGeoJSONに差し替えられる。

- 使用ライブラリ：A-Frame 1.6.0、AR.js 3.4.7（`arjs-device-orientation-controls`のみ使用。
  GPSによる配置はAR.jsの機能を使わず自前で計算する）、MapLibre GL JS（ミニマップ表示）。
- 現在地から半径250m以内（開始画面で変更可能）の筆のみを描画する。データ全体は読み込み
  時に一度パースするが、描画対象はこの範囲に絞り込む。
- 各筆は地面レベルの輪郭線として表示する。立ち上げ（押し出し表示）は行わない。
- ラベルは`properties.name`があればそれを、なければ`properties.polygon_uuid`を表示する。
- 画面右下に、north-up固定のミニマップ（MapLibre GL JS、`osm-bright-ja`スタイル）。現在地
  と方位を反映したビーコンを表示し、タップで全画面表示に切り替わる。AR側で絞り込んだ筆と
  同じ内容をGeoJSONレイヤーとしても表示する。
- 画面左下に方位補正パネル（普段は折りたたみ）。AR.js側のカメラ回転と、こちらの座標計算
  との間に生じる体系的なズレを、配置済みオブジェクト側を逆方向に回転させることで打ち消す。

## 必要環境

- iOS（Safari）または Android（Chrome）。GPS・加速度・地磁気センサーを持つ端末。
- **HTTPS 配信**（カメラ・位置・方位はSecure Context必須）。GitHub PagesのURLを使う。
- **屋外**での実行。GPSが取得できない屋内では位置が定まらない。
- FirefoxはロケーションベースARが正しく動かないため使わない。

## データの構造要件

```
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "polygon_uuid": "一意な文字列（ラベルに使用。nameがあれば優先される）",
        "point_lat": 代表点の緯度（半径判定に使用。必須）,
        "point_lng": 代表点の経度（半径判定に使用。必須）
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [ [ [lng,lat], ..., 先頭と同じ点 ] ]
      }
    }
  ]
}
```

`point_lat` / `point_lng`が欠けているフィーチャーは、距離判定ができないため無条件に
描画対象から外れる。ジオメトリは`Polygon`のみに対応し、`Point`は現状扱えない。

## 既知の技術的制約

- AR.jsの位置情報系コンポーネントは`THREEx`というグローバル名前空間に依存しており、
  `aframe-ar.js`より前に`ar-threex-location-only.js`を読み込む必要がある。
- 方位センサーの値そのものが、実際の向きと系統的にずれることがある。原因はAR.js内部の
  座標変換、画面の向き（縦横）切り替え時の処理、地磁気センサーへの周辺環境の影響など、
  複数考えられる。詳細は`faculty/readme.md`を参照。
- 半径絞り込みは、開始後の最初のGPS取得時に一度だけ実行する。以降現在地が動いても、
  対象範囲の再計算は行わない。

## ファイル構成


./02_ar
├── app
│   ├── [index.html](./app)
│   └── [ube.geojson](./app/ube.geojson)
├── faculty
│   └── [readme.md](./faculty)
├── participants
│   └── [readme.md](./participants)
└── readme.md
