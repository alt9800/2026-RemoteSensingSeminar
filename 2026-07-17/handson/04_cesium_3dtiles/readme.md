# 04.【補足】CesiumJSを試す・3D Tilesを読み込む

本日のハンズオンでは扱いませんが、3D Tiles（PLATEAU等）をブラウザで表示するまでの最短経路をまとめておきます。

## CesiumJSの最小構成

CesiumJSはCDNから読み込めます。HTMLファイル1つで動きます。

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <script src="https://cesium.com/downloads/cesiumjs/releases/1.119/Build/Cesium/Cesium.js"></script>
  <link href="https://cesium.com/downloads/cesiumjs/releases/1.119/Build/Cesium/Widgets/widgets.css" rel="stylesheet" />
  <style>
    html, body, #cesiumContainer { width: 100%; height: 100%; margin: 0; padding: 0; }
  </style>
</head>
<body>
<div id="cesiumContainer"></div>
<script>
  // Cesium ionのアセット（World Terrain等）を使わない構成。
  // 背景はOSMタイル、地形は楕円体のみ。トークン不要で動く。
  const viewer = new Cesium.Viewer("cesiumContainer", {
    imageryProvider: new Cesium.OpenStreetMapImageryProvider({
      url: "https://tile.openstreetmap.org/"
    }),
    baseLayerPicker: false,
    geocoder: false,
    timeline: false,
    animation: false
  });
</script>
</body>
</html>
```

注意点：

- CesiumJSのバージョンは更新が速いので、CDNのURLは公式サイト（cesium.com）で最新のリリース番号を確認してください
- Cesium ion（クラウドサービス）のアセット（World Terrain・Bing衛星画像等）を使う場合はアカウント登録とアクセストークンが必要です。無料枠があります
- ionを使わなくても、上記のようにOSM等の外部タイルと組み合わせれば動作します

## 3D Tilesの読み込み

`tileset.json` のURLを指定するだけです。

```js
const tileset = await Cesium.Cesium3DTileset.fromUrl(
  "https://（配信元のURL）/tileset.json"
);
viewer.scene.primitives.add(tileset);
viewer.zoomTo(tileset);
```

## PLATEAUの建物データを表示する

PLATEAU（国土交通省の3D都市モデル）は建物モデルを3D Tiles形式で配信しています。

- 配信URLの一覧はG空間情報センターの「3D都市モデル（Project PLATEAU）」の各都市ページ、またはPLATEAUの配信サービスのドキュメントで確認できます
- 都市・年度ごとに `tileset.json` のURLが公開されているので、上記の `fromUrl` に渡すだけで表示されます
- 表示位置は自動でジオリファレンスされているため、座標変換は不要です（3D Tilesが位置情報を内包しているため）

第2回で扱った「タイルのURLさえ分かれば自前で表示できる」という構図が、3Dでもそのまま成立していることが確認できます。

## Re:Earthについて

Re:EarthはCesiumJSベースの国産OSSのノーコードWebGISです。コードを書かずにブラウザ上で3D Tilesやデータの重ね合わせ・公開ができます。「コードを書くほどではないが3D地図を共有したい」という場面の選択肢として覚えておくとよいでしょう。

https://reearth.io/
