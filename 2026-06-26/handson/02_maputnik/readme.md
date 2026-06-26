# Maputnik でスタイルを編集する

---

## 準備

```bash
# fude.pmtiles と同じディレクトリでローカルサーバーを起動
python3 -m http.server 8000
```

ブラウザで https://app.maputnik.com/ を開く。

---

## 手順

### 1. ベーススタイルを読み込む

「Open」→「From URL」→ 以下を入力：

```
https://gsi-cyberjapan.github.io/gsivectortile-mapbox-gl-js/std.json
```

または「Empty Style」から白紙で始めて自前の PMTiles だけ使う。

### 2. データソースを追加する

「Data Sources」→「Add New Source」

```
Source ID  : fude
Source Type: Vector（TileJSON / PMTiles）
URL        : http://localhost:8000/fude.pmtiles
```

### 3. レイヤーを追加する

「Add Layer」→ 以下を設定：

```
ID          : fude-fill
Type        : Fill
Source      : fude
Source Layer: fude
```

Paint プロパティで色を設定：

```
fill-color  : #6ab04c
fill-opacity: 0.5
```

### 4. ズームに応じて透明度を変化させる

`fill-opacity` の右の「＋」→「Zoom」を選択：

```
zoom 10 → 0.2
zoom 17 → 0.7
```

### 5. スタイルをエクスポートして MapLibre に渡す

「Export」→ `style.json` をダウンロード。

```js
const map = new maplibregl.Map({
  container: 'map',
  style: './style.json'   // エクスポートしたファイルをそのまま渡す
});
```

---

## 補足：スタイルの渡し方

MapLibre へのスタイルの渡し方は2パターンある。
Maputnik のエクスポートはパターン①の形になる。

### パターン①：スタイル JSON の URL（またはオブジェクト）を渡す

```js
// URL を渡す（Maputnik エクスポートの利用）
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

ソースもレイヤーも JSON 側に書かれているため、コード側はシンプルになる。
カスタマイズは JSON を直接編集するか、Maputnik で再編集する。

### パターン②：インラインでオブジェクトを書く（PMTiles を直接扱う場合）

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

`pmtiles://` は独自プロトコルなので `addProtocol()` の事前登録が必要。
ソースもレイヤーも自分で書くため、細かいカスタマイズがしやすい。

### どちらを選ぶか

| | パターン① | パターン② |
|---|---|---|
| 向いている場面 | Maputnik で作ったスタイルを使う | コードで全部管理したい |
| レイヤー定義 | JSON 側 | コード側 |
| PMTiles 直参照 | URL で書けば可 | `addProtocol()` が必要 |
| タイルの中身 | MVT（PBF） | MVT（PBF）← 同じ |

---

## 参考

`setStyle()` 後にソースやレイヤーを追加する場合は `styledata` より `idle` イベントを使う
（地理院地図ベクタータイルの試行錯誤で確認済み → `../../../2026-06-19/handson/04_gsi_vector/NOTES.md` 参照）。