# ハンズオン② 観測ポイントAR

位置情報ベースのARで、周囲の観測ポイント（ラベル）と圃場区画（押し出したブロック）を
カメラ映像に重ねて表示する。AR.js のロケーションベースを使う。

## 学習目標

- AR.js のロケーションベースで、緯度・経度に紐づけたオブジェクトをカメラ映像に重ねられる。
- GPS の現在地を基準に、AR空間へオブジェクトが配置される流れを説明できる。
- 位置情報ベースARの精度（数メートル）の範囲でできること・できないことを理解する。

## 動かすもの

アプリ本体は [`app/index.html`](./app/)。`app/observation_points.geojson` を読み込み、
Point はラベル付きのブロック、Polygon は NDVI に応じた色・高さで押し出したブロックとして表示する。

- 使用ライブラリ：A-Frame 1.6.0、AR.js 3.4.7（`gps-new-camera` / `gps-new-entity-place`）。
- NDVI 値で色分け（水域は青、低NDVIは黄、高NDVIは緑）。値のない点は灰。

## 必要環境

- iOS（Safari）または Android（Chrome）。GPS・加速度・地磁気センサーを持つ端末。
- **HTTPS 配信**（カメラ・位置・方位は Secure Context 必須）。GitHub Pages のURLを使う。
- **屋外**での実行。GPS が取得できない屋内では位置が定まらない。
- Firefox はロケーションベースARが正しく動かない（絶対方位が取れない）ため使わない。

## データの差し替え

`app/observation_points.geojson` の `base` は概算値。当日は実測GPSに合わせて再生成する。
手順とスクリプトは [`faculty/readme.md`](./faculty/) の「データの再生成」節を参照。

## ファイル

- `app/index.html` — 実装本体（`./02_ar/app/`）
- `app/observation_points.geojson` — 観測ポイント（ダミー）
- `faculty/readme.md` — 講師用（配信・iOS対応・トラブルシュート・実装の限界）
- `participants/readme.md` — 受講者用（操作手順）
