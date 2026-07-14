# Maputnik でスタイルを編集する

MapLibre Style Spec を GUI で編集できるオープンソースのスタイルエディタ。
編集結果を JSON でエクスポートし、そのまま MapLibre に渡せる。

---

## Maputnik と PMTiles の関係

Maputnik はスタイルエディタなので、直接読み込めるのは `style.json` のみ。

| 操作 | 読み込めるか |
|---|---|
| style.json を Upload | ✓ 直接読み込める |
| fude.pmtiles を Upload | ✗ 読み込めない |
| fude.pmtiles を URL で参照 | ✓ ローカルサーバー経由で参照できる |

PMTiles はデータソースなので、Data Sources に URL を指定して参照する。
このとき `app.maputnik.com`（外部）が `localhost:8000`（ローカル）へリクエストするため、
**別オリジン間の通信が発生し CORS 設定が必要**になる。

---

## 準備

```bash
# fude.pmtiles と同じディレクトリでローカルサーバーを起動
python3 -m http.server 8000
```

ブラウザで https://app.maputnik.com/ を開く。

---

## Step 1：スタイルを読み込む

「Open」→「From URL」→ 以下を入力して読み込む：

```
https://gsi-cyberjapan.github.io/gsivectortile-mapbox-gl-js/std.json
```

地理院地図ベクタータイルのスタイルが Maputnik 上に展開される。
左パネルにレイヤー一覧、中央にプレビューが表示される。

白紙から始める場合は「New Style」→「Empty Style」を選ぶ。

---

## Step 2：自前のデータソースを追加する

右上の「Data Sources」→「Add New Source」

```
Source ID  : fude
Source Type: Vector（TileJSON / PMTiles）
URL        : http://localhost:8000/fude.pmtiles
```

---

## Step 3：レイヤーを追加する

左パネル下部「＋ Add Layer」

```
Layer ID    : fude-fill
Layer Type  : Fill
Source      : fude
Source Layer: fude       ← tippecanoe の -l に対応
```

---

## Step 4：色と透明度を設定する

レイヤーを選択 →「Paint」タブ

```
fill-color   : #6ab04c
fill-opacity : 0.5
```

ズームに応じて透明度を変化させる場合：
`fill-opacity` の右の「＋」→「Zoom」を選択

```
zoom 10 → 0.2
zoom 17 → 0.7
```

---

## Step 5：エクスポートして MapLibre に渡す

「Export」→ `style.json` をダウンロード。

```js
// 初期化時にそのまま渡す
const map = new maplibregl.Map({
  container: 'map',
  style: './style.json'
});

// 後から切り替える場合
fetch('./style.json')
  .then(r => r.json())
  .then(style => {
    map.once('idle', () => map.setStyle(style));
  });
```

---

## 補足：スタイルの渡し方2パターン

Maputnik のエクスポートは**パターン①**の形になる。

| | パターン① URL / JSON ファイル | パターン② インラインオブジェクト |
|---|---|---|
| 向いている場面 | Maputnik で作ったスタイルを使う | コードで全部管理したい |
| レイヤー定義 | JSON 側 | コード側 |
| `pmtiles://` | URL に書けば可 | `addProtocol()` の事前登録が必要 |
| タイルの中身 | MVT（PBF） | MVT（PBF）← 同じ |

パターン②（インライン）の例：

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

---

## 補足：setStyle() のタイミング

スタイル切り替え後にソースやレイヤーを追加する場合は `styledata` より `idle` を使う。

```js
map.setStyle(newStyle);
map.once('idle', () => {
  // ここでソース・レイヤーを追加する
});
```

地理院地図ベクタータイルのカスタマイズで確認済み。
詳細 → `2026-06-19/handson/04_gsi_vector/NOTES.md`