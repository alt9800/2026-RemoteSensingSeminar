# 02. PotreeConverterによる変換とWeb公開

01で書き出したLASファイルをoctree形式に変換し、ブラウザで見られる状態にします。

## Potreeエコシステムの整理

Potree（読みは「ポトリー」。point cloud + octree に由来する造語）は、Three.jsベースのオープンソース点群Webビューアです。Octree LODにより大量の点群を高速表示できます。

- **Potree**：Webビューア本体のJavaScriptライブラリ
- **PotreeConverter**：CLIの変換ツール。LAS/LAZをPotreeが読めるoctree形式に変換する
- **PotreeDesktop**：Electronベースのデスクトップアプリ。GUIで点群を閲覧できる

## PotreeConverterの入手

GitHubのReleasesからダウンロードします。バイナリは**WindowsとLinux（x86_64）向け**に提供されています。

https://github.com/potree/PotreeConverter

macOSの方はDockerでLinuxバイナリを使います。手順と既知の問題は [faculty/readme.md](./faculty/) にまとめてあります。当日はこちらでサポートしますので、Docker Desktopの導入だけ済ませておいてください。

## 変換（Windows / Linux）

```sh
PotreeConverter input.las -o ./output --generate-page index
```

`--generate-page index` を指定すると、ビューア付きの index.html も生成されます。

出力ディレクトリの構成：

```sh
output/
├── metadata.json    # メタデータ（バウンディングボックス、属性定義等）
├── hierarchy.bin    # octreeの階層構造
├── octree.bin       # 点群データ本体
└── index.html       # ビューア付きHTMLページ
    （+ libs/ 等のPotreeビューア用リソース）
```

変換時間の目安：Scaniverseのスキャンデータ（80万点・20MB程度）で数秒です。出力される `octree.bin` は入力LASと同程度かやや小さくなります。

PotreeConverterには圧縮オプションがないため、実運用ではWebサーバー側でBrotli/gzip圧縮を行って配信するとよいでしょう（GitHub Pagesは自動で圧縮配信されます）。

## 注意：CloudCompareで編集したLASが「0点」扱いになる場合

CloudCompareでGlobal Shiftが適用された状態でエクスポートすると、LASのバウンディングボックスがすべて0になり、PotreeConverterが `#points: 0` として扱うことがあります。

- 変換結果が空になった場合は、まずこれを疑ってください
- CloudCompareのエクスポート時の座標オフセット設定を確認します（01の手順で「シフトを保持したまま」保存していれば通常は問題ありません）
- 切り分けとして、Scaniverseからエクスポートした元のLASファイルは問題なく変換できます

## ローカルでの確認

`file://` での直接オープンは不可です（fetchが失敗します。第1回のPMTilesと同じ理由）。

```sh
python3 -m http.server 8080 -d output
# または
npx serve output
```

ブラウザで `http://localhost:8080/index.html` を開くと、Potreeビューアで点群が表示されます。左パネルのPoint budget（同時表示する最大点数）やEye-Dome-Lighting等を触ってみてください。

## 公開

静的ファイル一式なので、ホスティングサーバーに転送するだけで公開できます。

| 公開先 | 備考 |
|--------|------|
| GitHub Pages | リポジトリに置くだけ。1ファイル100MB制限に注意 |
| Nginx（自前サーバー） | 第2回で構築したRaspberry Pi構成にディレクトリを足すだけ |

→ 次：[03_deckgl](../03_deckgl/) で点群を地図の上に重ねます。
