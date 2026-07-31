# ハンズオン① 位置・方位の確認

スマートフォンの GPS と方位センサーを、Web API から直接読む。取得した値を画面に表示し、
iOS と Android で方位（heading）の取得方式が変わることを実機で確認する。

## 学習目標

- Geolocation API と DeviceOrientationEvent の値を、自分で取り出して表示できる。
- alpha / beta / gamma と「方位」の関係、および iOS / Android の差異を説明できる。
- 位置・方位センサーが HTTPS と権限を前提とすることを理解する。

## 動かすもの

アプリ本体は [`app/index.html`](./app/) 一枚で完結する。外部ライブラリは使わない。

- 「センサーを開始」ボタンで、位置と方位の取得を始める。
- 緯度・経度・精度、alpha / beta / gamma、算出した方位（と取得方式）を表示する。
- 方位ダイヤルの針が常に北を指す。端末を回して実際の北と一致するか確認する。

## 必要環境

- iOS（Safari）または Android（Chrome）のスマートフォン。
- **HTTPS 配信**。位置・方位センサーは Secure Context でしか動かない。
  本リポジトリの GitHub Pages に置けば HTTPS で配信されるため、そのURLをスマホで開く。
  （`localhost` も Secure Context だが、別端末のスマホからは到達できない点に注意。）

## 確認する点

- iOS は `webkitCompassHeading`、Android は `deviceorientationabsolute` を使う。
- alpha が相対値か絶対値かで、方位の意味が変わる。
- 端末を横持ちにすると方位がずれることがある（画面回転の補正が要る）。

## ファイル

- `app/index.html` — 実装本体（`./01_sensor/app/` で配信される）
- `faculty/readme.md` — 講師用（配信準備・OS別挙動・トラブルシュート）
- `participants/readme.md` — 受講者用（当日の操作手順）
