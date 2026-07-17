# 02. PotreeConverterによる変換とWeb公開

01で書き出したLASファイルをoctree形式に変換し、ブラウザで見られる状態にします。

## Potreeエコシステムの整理

- **Potree**：Webビューア本体のJavaScriptライブラリ。Three.jsベースで、Octree LODにより大量の点群を高速表示できる
- **PotreeConverter**：CLIの変換ツール。LAS/LAZをPotreeが読めるoctree形式に変換する
- **PotreeDesktop**：Electronベースのデスクトップアプリ。GUIで点群を閲覧できる

## PotreeConverterの入手

GitHubのReleasesからダウンロードするか、npmでインストールします。バイナリは**WindowsとLinux向け**に提供されています。macOSはDockerでLinuxバイナリを使います（後述）。

https://github.com/potree/PotreeConverter

## 変換（Windows / Linux）

```sh
PotreeConverter input.las -o ./output --generate-page index
```

`--generate-page index` を指定すると、ビューア付きの index.html が生成されます。

出力ディレクトリの構成：

```sh
output/
├── metadata.json    # メタデータ（バウンディングボックス、属性定義等）
├── hierarchy.bin    # octreeの階層構造
├── octree.bin       # 点群データ本体
└── index.html       # ビューア付きHTMLページ
    （+ libs/ 等のPotreeビューア用リソース）
```

PotreeConverterには圧縮オプションがないため、実運用ではWebサーバー側でBrotli/gzip圧縮を行って配信するとよいでしょう（GitHub Pagesは自動で圧縮配信されます）。

## macOSでの利用（Docker）

以下のDockerfileでLinux環境ごと用意します。

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    git cmake build-essential libtbb-dev curl && \
    rm -rf /var/lib/apt/lists/*

# PotreeConverter のビルド
RUN git clone --branch 2.1.1 --depth 1 https://github.com/potree/PotreeConverter.git /tmp/PotreeConverter && \
    cd /tmp/PotreeConverter && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release && \
    make -j$(nproc) && \
    mkdir -p /opt/PotreeConverter && \
    cp PotreeConverter /opt/PotreeConverter/ && \
    cp -r /tmp/PotreeConverter/resources /opt/PotreeConverter/ && \
    find /tmp/PotreeConverter/build -name "*.so*" -exec cp {} /usr/local/lib/ \; && \
    ldconfig && \
    rm -rf /tmp/PotreeConverter

# Potree 1.8 ビューアの libs をテンプレートに追加
RUN curl -L https://github.com/potree/potree/archive/refs/tags/1.8.tar.gz -o /tmp/potree.tar.gz && \
    tar -xzf /tmp/potree.tar.gz -C /tmp/ && \
    cp -r /tmp/potree-1.8/libs/* /opt/PotreeConverter/resources/page_template/libs/ && \
    rm -rf /tmp/potree.tar.gz /tmp/potree-1.8

WORKDIR /data
ENTRYPOINT ["/opt/PotreeConverter/PotreeConverter"]
```

ビルド：

```sh
docker build -t potreeconverter .

# Appleシリコンの場合はamd64向けにビルドすることを明示する
docker build --platform linux/amd64 -t potreeconverter .
```

変換の実行：

```sh
docker run --rm -v $(pwd):/work potreeconverter \
  /work/data/{データ名}.las -o /work/potree_output --generate-page index
```

### 既知の問題：libsのコピー失敗

環境によっては、変換時に `resources/page_template/` の中身（HTMLテンプレートとlibsディレクトリ一式）を出力先にコピーする段階で、ファイル権限の問題により失敗することがあります。

変換自体は正常に完了しているはずなので、出力の `libs` に関連ファイルが含まれていない場合は、`docker cp` などでテンプレートからライブラリを取り出してください。

## ローカルでの確認

`file://` での直接オープンは不可です（fetchが失敗します。第1回のPMTilesと同じ理由）。以下のいずれかで確認します。

- `python3 -m http.server 8000`
- npm の `http-server`
- VSCode拡張「Live Server」

ブラウザで `http://localhost:8000/output/index.html` を開くと、Potreeビューアで点群が表示されます。左パネルのPoint budget（同時表示する最大点数）やEye-Dome-Lighting等を触ってみてください。

## 公開

静的ファイル一式なので、ホスティングサーバーに転送するだけで公開できます。

| 公開先 | 備考 |
|--------|------|
| GitHub Pages | リポジトリに置くだけ。1ファイル100MB制限に注意 |
| Nginx（自前サーバー） | 第2回で構築したRaspberry Pi構成にディレクトリを足すだけ |

→ 次：[03_deckgl](../03_deckgl/) で点群を地図の上に重ねます。
