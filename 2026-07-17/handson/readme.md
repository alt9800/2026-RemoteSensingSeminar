# 第4回ハンズオン：点群・3DGSのWeb可視化

本日のハンズオンの手順書一式です。01〜03が本編、04〜05は自習用の補足資料です。

| ディレクトリ | 内容 | 当日の扱い |
|--------------|------|-----------|
| [01_cloudcompare](./01_cloudcompare/) | CloudCompareによる点群の前処理 | ハンズオン① 前半 |
| [02_potree](./02_potree/) | PotreeConverterによる変換とWeb公開 | ハンズオン① 後半 |
| [03_deckgl](./03_deckgl/) | deck.glで点群を地図に重ねる | ハンズオン② |
| [04_cesium_3dtiles](./04_cesium_3dtiles/) | CesiumJSと3D Tiles（PLATEAU）の読み込み | 補足（自習用） |
| [05_3dgs](./05_3dgs/) | 3DGSの取得・閲覧・編集 | 補足（自習用） |

## 事前準備

- 配布データ：スキャン済みLASファイル（当日ローカルサブネット経由で配布します）
- 自分のスキャンデータを使いたい方：LiDAR搭載のiPhone Pro / iPad ProとScaniverse（無料）でLASエクスポートまで済ませておいてください
- ローカルWebサーバー：以下のいずれかが動けばOKです
  - `python3 -m http.server`
  - `npx http-server`
  - VSCode拡張「Live Server」
- macOSの方：ハンズオン①の変換にDockerを使います。Docker Desktopを導入しておいてください（詳細は02_potreeのREADME参照）
