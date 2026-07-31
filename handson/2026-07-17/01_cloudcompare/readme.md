# 01. CloudCompareによる点群の前処理

スキャンしたLASファイルを、Web表示に適した状態へ整えます。工程は次の5つです。

1. 読み込みとファイルの詳細確認
2. クリッピング（対象範囲の切り出し）
3. ノイズ除去（SORフィルタ）
4. サブサンプリング（点数の削減）
5. LAS形式でエクスポート

書き出したLASファイルは、02_potree（Potree）と03_deckgl（deck.gl）の両方で入力として使います。

## 0. CloudCompareの入手

https://www.cloudcompare.org/ からOS向けのインストーラを取得してください（GPL v2ライセンスのOSS）。

## 1. 読み込みとファイルの詳細確認

LASファイルをドラッグアンドドロップ等で読み込むと、「Open LAS file」ダイアログが表示されます。

**属性フィールドの選択**

Standard FieldsにIntensity、Return Number、Classification等が並びますが、iPhone LiDARのスキャンデータではこれらにデフォルト値（0）しか入っていないことがほとんどです。「Ignore fields with default values only」にチェックが入っていれば自動でスキップされるため、基本的にそのままで問題ありません。「Automatic GPS Time shift」も同様に無視して構いません。

**Global shift/scale ダイアログ**

続いて座標値の大きさを検知して表示されるダイアログです。左側「Point in original coordinate system」にディスク上の元の座標値、右側「Point in local coordinate system」にシフト適用後の値が表示されます。

- 元の座標値が x=625475, y=3715901 のような大きな値なら、UTM投影座標系で格納されています（ScaniverseのLAS出力はこのパターン）
- 大きな座標値を内部的にシフトするのは、float精度落ちを防ぐための仕組みです
- そのまま `Yes` で進めます

読み込み後、プロパティパネルで点数（Points）と、RGBが載っているかを確認しておきます。

## 2. クリッピング

対象の構造物の周囲に含まれる地面や周辺環境の点を除外します。

1. メニューの Tools > Segmentation > **Cross Section** を選択
2. 点群全体を囲むバウンディングボックスが表示される
3. 各面の矢印ハンドルをドラッグしてボックスを縮小（右パネルのBox thicknessで数値入力も可。Box moveの±X/±Y/±Zで位置調整も可）
4. 対象がボックス内に収まったら、パネル上部の「**Export selection as a new cloud**」を押す
5. ×ボタンでCross Sectionモードを閉じる

以降の作業はエクスポートされた新しい点群に対して行います。元の点群は不要なら選択してDeleteキーで削除できます。

なお、ポリゴンで囲んだ範囲を選択・削除するツール（Edit > Segment）もあります。複雑な形状の切り出しにはこちらが適していますが、初めのうちはCross Sectionの方が直感的です。

## 3. ノイズ除去（SORフィルタ）

対象物の表面から離れた孤立点を統計的に除去します。

1. データベースツリーでクリッピング済みの点群を選択
2. Tools > Clean > **SOR filter** を選択
3. パラメータを設定して実行

| パラメータ | 意味 | 目安 |
|-----------|------|------|
| Number of points for distance estimation | 各点の近傍として参照する点数 | 6〜10から始める |
| Standard deviation multiplier | 小さいほど判定が厳しい | 1.0で厳しめ、2.0〜3.0で穏やか |

## 4. サブサンプリング

Web表示に向けて点数を削減します。deck.glのPointCloudLayerでは読み込む点数がそのまま描画負荷に直結するため、**数十万点程度**を目安に間引きます。

1. 対象の点群を選択し、Edit > **Subsample** を選択
2. 方式を選んで実行

| 方式 | 挙動 | 使いどころ |
|------|------|-----------|
| Space（空間） | 指定した最小間隔でグリッド化し各セルから1点を残す | 空間的に均一になる。まずこれを試す |
| Random | 残す点数を直接指定 | 密度分布が元データに依存する |
| Octree | 八分木の指定レベルで間引く | Web表示用途ではSpaceの方がシンプル |

## 5. エクスポート

1. 対象の点群を選択し、File > Save As
2. 拡張子 `.las` を指定して保存（保存形式は拡張子で決まります）
3. 「Save LAS file」ダイアログでは**シフトを保持したまま**保存します

保存されたLASヘッダのoffset値は、03_deckglで座標変換の基準値として使います。

→ 次：[02_potree](../02_potree/) で変換とWeb公開を行います。
