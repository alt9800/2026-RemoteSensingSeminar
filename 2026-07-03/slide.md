---
marp: true
theme: default
header: "衛星データ解析技術研究会<br>技術セミナー（応用編）第三回 2026/07/03"
footer: "第3回 3D技術①：スマホセンサーとAR"
paginate: true
style: |
  /* ── カラー変数 ──────────────────────────────────────────
     講義全体で使うブランドカラーを一元管理する。
     変更する場合はここだけ編集すればよい。              */
  :root {
    --navy:       #1C3A4A;   /* 見出し・テーブルヘッダー */
    --teal:       #028090;   /* アクセント・ラベル・リンク */
    --green:      #2D7D46;   /* 正例・OKの強調 */
    --red:        #B91C1C;   /* 警告・注意事項 */
    --gray:       #374151;   /* 本文グレー */
    --light:      #F8FAFB;   /* テーブル偶数行・薄い背景 */
    --teal-light: #E6F4F6;   /* h2 の下線・カード背景 */
    --brand:      #9DE371;   /* ロゴのイエローグリーン：タイトル・区切りスライドのアクセント */
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
  h1 {
    font-size: 2em;
    color: var(--navy);
    border: none;
    margin-bottom: 0.5em;
  }
  h2 {
    /* セクション内の中見出し。下線でセクションの切れ目を示す */
    font-size: 1.3em;
    color: var(--teal);
    border-bottom: 2px solid var(--teal-light);
    padding-bottom: 0.2em;
  }
  h3 {
    font-size: 1.05em;
    color: var(--navy);
  }

  /* ── コードブロック ──────────────────────────────────── */
  code {
    /* インラインコード（コマンド名・変数名など） */
    font-family: "Courier New", monospace;
    background: #F0F0F0;
    padding: 0.1em 0.4em;
    border-radius: 3px;
    font-size: 0.88em;
    color: #2B2B2B;
  }
  pre {
    /* フェンスコードブロック（コマンド・スクリプト全体） */
    background: #F0F0F0;
    border-radius: 6px;
    padding: 0.8em 1em;
    font-size: 0.82em;
    line-height: 1.55;
  }
  pre code {
    background: none;
    padding: 0;
  }

  /* ── テーブル ────────────────────────────────────────── */
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88em;
  }
  th {
    background: var(--navy);
    color: #ffffff;
    padding: 0.4em 0.7em;
    font-weight: bold;
  }
  td {
    padding: 0.4em 0.7em;
    border-bottom: 1px solid #e0e0e0;
    vertical-align: top;
  }
  tr:nth-child(even) td { background: var(--light); }

  /* ── ユーティリティクラス ────────────────────────────── */
  .label {
    /* スライド上部に置くセクション名ラベル（小さめの大文字） */
    font-size: 0.7em;
    font-weight: bold;
    color: var(--teal);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.2em;
  }
  .note {
    /* 補足・注意書き。スライド下部に配置することが多い */
    font-size: 0.78em;
    color: #6B7280;
    font-style: italic;
    margin-top: 0.6em;
  }
  .warn { color: var(--red);   font-weight: bold; }  /* 警告テキスト */
  .ok   { color: var(--green); font-weight: bold; }  /* OK・正解テキスト */

  /* ── タイトルスライド（_class: title） ─────────────────
     プロジェクター投影を考慮して白背景。
     ブランドカラー（--brand）を左帯として使い視認性を確保。 */
  section.title {
    background: #ffffff;
    color: var(--navy);
    justify-content: flex-start;
    padding-top: 60px;
    border-left: 14px solid var(--brand);
  }
  section.title h1 { color: var(--navy); font-size: 1.4em; margin-bottom: 0.1em; }
  section.title h2 { color: var(--navy); font-size: 2.2em; border: none; margin-bottom: 0.2em; font-weight: bold; }
  section.title h3 { color: var(--teal); font-size: 1.2em; font-weight: normal; }
  section.title p  { color: var(--gray); font-size: 0.85em; }

  /* ── アクセントスライド（_class: dark）─ ハンズオン導入・予告などに使用
     名称は dark のまま互換性を保つが、プロジェクター向けに白背景へ変更。
     上部にブランドカラーの帯を入れてセクション区切りを示す。          */
  section.dark {
    background: #ffffff;
    color: var(--navy);
    justify-content: flex-start;
    border-top: 12px solid var(--brand);
    padding-top: 52px;
  }
  section.dark h1   { color: var(--gray); font-size: 1.1em; margin-bottom: 0.2em; font-weight: normal; }
  section.dark h2   { color: var(--navy); font-size: 1.9em; border: none; margin-bottom: 0.5em; font-weight: bold; }
  section.dark li   { color: var(--gray); }
  section.dark .note { color: var(--teal); font-style: italic; }
---

## 第3回：3D技術① スマホセンサーとAR（140分）
 
 ---

| 時間 | 内容 |
|------|------|
| 10分 | イントロ・スマホセンサーの全体像 |
| 20分 | GeolocationAPI / DeviceOrientationEvent の特性と制約整理 |
| 10分 | WebXR / A-Frame / AR.js のエコシステム概観 |
| 35分 | ハンズオン①：Geolocation + DeviceOrientation での方位取得・確認 |
| 10分 | **休憩** |
| 35分 | ハンズオン②：AR.js + A-Frame で観測ポイントラベルをカメラ映像に重畳 |
| 10分 | デバイス差異・パーミッション周りの注意点整理 |
| 10分 | 振り返り・Q&A |


---

<div class="label">SESSION 3 / 3D技術①</div>

## 本セッションの位置づけとゴール

- 全6回のうち、ここから **3Dパート（第3・4回）** が始まる。第5・6回の高さデータ処理へ接続する起点。
- ゴール：スマホの各種センサーを **Web API から直接** 触り、地理座標とAR空間の対応関係を理解する。
- 一貫する問い：**外部SDKに丸投げせず、「センサー → API → 座標 → 描画」のデータフローを自分で追えるか。**

<div class="note">本日の実装はすべてブラウザ内で完結する。ネイティブアプリ（ARKit/ARCore）は使わない。</div>

---

## スマホセンサーの全体像

| センサー | 取得する物理量 | Web API | 代表的な用途 |
|----------|----------------|---------|--------------|
| GNSS（GPS等） | 緯度・経度・高度・速度 | Geolocation API | 現在地・移動追跡 |
| 加速度センサー | 3軸の加速度 | DeviceMotionEvent | 歩数・振動・傾き |
| ジャイロスコープ | 3軸の角速度 | DeviceMotionEvent（rotationRate） | 姿勢変化 |
| 地磁気センサー | 磁北方向 | DeviceOrientationEvent | 方位 |
| カメラ | 映像 | getUserMedia（MediaDevices） | ARの背景映像 |

<div class="note">本日主に扱うのは Geolocation・DeviceOrientation・getUserMedia の3つ。</div>

---

## なぜブラウザから触るのか — 前提の整理

- **配布の容易さ**：URLひとつで動く。アプリストアの審査・インストールが不要。
- **代償**：センサーへのアクセスに制約がある（精度・権限・OS差異）。ここを理解しておくことが本日の主眼。
- **全APIに共通する前提**：<span class="warn">Secure Context（HTTPS もしくは localhost）でしか動かない。</span>
- **権限モデルは分かれている**：位置・カメラ・モーション（方位）はそれぞれ別に許可を取る。

---

<div class="label">SENSORS / API</div>

## Geolocation API の基礎

```js
// 位置を継続的に監視する
const watchId = navigator.geolocation.watchPosition(
  (pos) => {
    const { latitude, longitude, accuracy } = pos.coords;
    // accuracy は「半径 accuracy メートルの円内にいる確度」
    console.log(latitude, longitude, accuracy);
  },
  (err) => console.error(err.code, err.message),
  { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
);
```

- `getCurrentPosition`（1回）／`watchPosition`（継続）の2系統。
- `coords` に含まれる主な値：`latitude` / `longitude` / `accuracy` / `altitude` / `altitudeAccuracy` / `heading` / `speed`。

---

## Geolocation の制約

- <span class="warn">HTTPS 必須</span>（Secure Context）。ローカル開発では localhost のみ例外。
- **精度は環境依存**：屋内・ビル街で大きく劣化する。`accuracy` は誤差半径（メートル）で返るので、値として扱う。
- **`heading` / `speed` は移動中のみ有効**なことが多く、静止時は `null`。<span class="warn">方位は Geolocation ではなく DeviceOrientation 側で取る。</span>
- 一度権限を拒否されると、再要求はブラウザ設定からになり難しい。最初の要求タイミングの設計が重要。

---

## DeviceOrientationEvent の座標系

端末の姿勢を3つの角度で表す。

- **alpha**：Z軸まわりの回転。`0–360`（≒ 方位に相当）
- **beta**：X軸まわりの回転。`-180–180`（前後の傾き）
- **gamma**：Y軸まわりの回転。`-90–90`（左右の傾き）

<div class="note">実機で値を出しながら端末を傾けて見せると直感的に伝わる。デモ推奨箇所。</div>

---

## 核心：方位取得の落とし穴

同じ「北」を出すのに、iOSとAndroidで処理が異なる。

```js
function extractHeading(e) {
  if (typeof e.webkitCompassHeading === "number") {
    // iOS: 0 = 北、時計回り。真北基準の値がそのまま得られる
    return e.webkitCompassHeading;
  }
  if (e.absolute && e.alpha != null) {
    // Android(絶対): alpha は反時計回り。方位へ変換する
    return (360 - e.alpha) % 360;
  }
  return null; // 取得不可
}
```

- <span class="warn">iOS の `alpha` は相対値</span>（リスニング開始時が基準）。真北が欲しければ `webkitCompassHeading` を使う。
- <span class="warn">Android の `deviceorientation` は絶対方位を保証しない</span>。`deviceorientationabsolute` イベントを使う。
- 上の変換式・挙動は端末とOSで揺れる。<span class="warn">値を鵜呑みにせず、ハンズオン①で必ず実機検証する。</span>

---

## パーミッション（iOS 13+ の追加要件）

```js
async function enableOrientation() {
  // iOS 13+ のみ requestPermission が存在する
  if (typeof DeviceOrientationEvent.requestPermission === "function") {
    const res = await DeviceOrientationEvent.requestPermission();
    if (res !== "granted") return;
  }
  // Android はこの分岐を通らず、そのまま登録される
  window.addEventListener("deviceorientationabsolute", extractHeading);
  window.addEventListener("deviceorientation", extractHeading);
}
```

- iOS では <span class="warn">`requestPermission()` を必ず「ユーザージェスチャ（ボタンタップ等）の中」で呼ぶ</span>。ページ読み込み時の自動実行は拒否される。
- Android は基本的に許可ダイアログ不要（ただし HTTPS は必須）。

---

<div class="label">ECOSYSTEM</div>

## 3つの層 — WebXR / A-Frame / AR.js

- **WebXR Device API**：ブラウザ標準の低レベルAR/VR API。WebGLで描画。
- **A-Frame**：Three.js の上に載る宣言的HTMLフレームワーク。`<a-scene>` などのタグで3D空間を書ける。
- **AR.js**：A-Frame等と組み合わせるWebARライブラリ。**マーカーベース**と**ロケーションベース**の2系統を持つ。

<div class="note">「標準API」「3D記述フレームワーク」「ARの位置合わせ」で役割が分かれている、と整理すると見通しがよい。</div>

---

## WebXRの現状と、今回AR.jsを採用する理由

| 環境 | WebXR immersive-ar |
|------|--------------------|
| Android Chrome（ARCore対応機） | 動作する |
| iPhone / iPad Safari | 実質非対応（利用不可） |
| visionOS Safari | VRのみ。ARは非対応 |

- **iPhoneとAndroidの両方で同じ教材を動かしたい** → WebXRだけに依存できない。
- そこで、**getUserMedia（カメラ）+ DeviceOrientation（方位）** で成立する **AR.js のロケーションベース** を実装の主軸にする。
- WebXRは「標準として概観する」位置づけにとどめる。

<div class="note">iOSのWebXR対応状況はOSアップデートで変わりうる領域。本日時点の前提として扱う。</div>

---

## AR.jsの2系統

- **マーカーベース**：ARマーカー（Hiroマーカー等）を基準に3Dオブジェクトを配置。屋内・展示・印刷物との連動に向く。
- **ロケーションベース**：GPS + 方位で **地理座標そのもの** にオブジェクトを配置。屋外・現地調査に向く。

→ 本日のハンズオン②では **ロケーションベース** を使い、観測ポイントのラベルをカメラ映像に重ねる。

<div class="note">第2回までで扱った「地理座標を扱う」感覚が、そのままAR空間の配置につながる。</div>