# 02-faculty. PotreeConverter Docker環境（macOS / トラブルシューティング）

macOS（Intel / Apple Silicon）でPotreeConverterを動かすための講師用資料です。各Dockerコマンドが**何をするのか**を明示しながら手順を追います。

## 前提

- PotreeConverter 2.1.1（安定版）
- Potree 1.8（ビューアライブラリ）
- Docker Desktop for Mac（Intel / Apple Silicon 対応）

## Dockerfile

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

## Step 1：イメージのビルド

```bash
docker build -t potreeconverter .
```

**何が起きるか**：カレントディレクトリのDockerfileに従って、Ubuntu 22.04の中でPotreeConverterをソースからコンパイルし、Potree 1.8のビューアライブラリを組み込んだ「イメージ」（実行環境の雛形）を作成します。`-t potreeconverter` はイメージに付ける名前です。初回のみ必要で、数分かかります。以降の変換ではこのイメージを使い回します。

Apple Siliconの場合はプラットフォームを明示します（公式バイナリも本Dockerfileのビルド対象もx86_64のため）。

```bash
docker build --platform linux/amd64 -t potreeconverter .
```

Rosettaエミュレーション経由での実行になりますが、iPhone LiDARスキャン程度の規模（数百万点）であれば実用上問題ありません。

## Step 2：変換の実行

```bash
docker run --rm -v $(pwd):/work potreeconverter \
  /work/data/origin.las -o /work/potree_output --generate-page index
```

**何が起きるか**：イメージから使い捨てのコンテナを起動し、その中でPotreeConverterを1回実行して、終了と同時にコンテナを破棄します（`--rm`）。

- `-v $(pwd):/work`：ホストのカレントディレクトリをコンテナ内の `/work` として見せる（マウント）。これによりコンテナ内での出力がホスト側に残る
- **コマンド中のパスはすべてコンテナ側**（`/work/...`）で書く。ホスト側のパスと混同しないこと
- ホスト側で `./data/origin.las` にあるファイルは、コンテナからは `/work/data/origin.las` に見える

処理時間の実測：Scaniverseのテストデータ（832,411点、20.6MB）で約3秒。

## 既知の問題：`--generate-page` の Permission denied

`--generate-page` は変換時に `resources/page_template/` の中身（HTMLテンプレートとlibsディレクトリ一式）を出力先へコピーしようとしますが、ボリュームマウント環境ではファイル権限の問題で失敗することがあります。

```
ERROR(main.cpp:453): filesystem error: cannot copy: Permission denied
  [/opt/PotreeConverter/resources/page_template] [/work/potree_output]
```

**変換自体は正常に完了しています。** 失敗するのはビューア関連ファイルのコピーだけで、点群データ（metadata.json / hierarchy.bin / octree.bin）は正しく出力されています。

## Step 3：ビューアファイルの取り出し（Permission denied対策）

イメージの中に入っているテンプレートを、`docker cp` でホスト側に取り出します。1行ずつ実行して、各コマンドの効果を確認しながら進めるのが確実です。

```bash
# 1. イメージから一時コンテナを「作成」する（起動はしない。
#    ファイルシステムだけが用意され、docker cp の対象にできる状態になる）
docker create --name tmp potreeconverter

# 2. コンテナ内のlibs一式をホスト側にコピーする
#    書式は docker cp <コンテナ名>:<コンテナ内パス> <ホスト側パス>
docker cp tmp:/opt/PotreeConverter/resources/page_template/libs potree_output/libs_full

# 3. index.htmlも変換時にコピーされていなければ同様に取り出す
docker cp tmp:/opt/PotreeConverter/resources/page_template/index.html potree_output/

# 4. 一時コンテナを削除する（コピーが済めば不要）
docker rm tmp

# 5. 失敗時に中途半端に残ったlibsを除去し、完全版に差し替える
rm -rf potree_output/libs
mv potree_output/libs_full potree_output/libs

# 6. 確認：potreeのビューア本体が入っていればOK
ls potree_output/libs/potree/
```

補足：`docker cp $(docker create --name tmp potreeconverter):...` のようにコマンド置換で1行にまとめる書き方も見かけますが、`docker create` の出力（コンテナID）が `docker cp` の第1引数に化ける挙動が読みにくく、失敗時の切り分けも難しくなるため、上記のように段階を分けることを推奨します。

## 一括実行スクリプト

毎回手動で行うのは手間なので、スクリプトにまとめておきます。

```bash
#!/bin/bash
# convert.sh — PotreeConverter 変換 + ビューアファイル配置
# 使い方: ./convert.sh input.las output_dir

INPUT=$1
OUTPUT=$2

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
  echo "使い方: ./convert.sh <入力LASファイル> <出力ディレクトリ>"
  exit 1
fi

rm -rf "$OUTPUT"

# 変換実行
docker run --rm -v $(pwd):/work potreeconverter \
  "/work/$INPUT" -o "/work/$OUTPUT" --generate-page index

# ビューアファイルの配置（Permission denied 対策）
docker create --name tmp potreeconverter
docker cp tmp:/opt/PotreeConverter/resources/page_template/libs "$OUTPUT/libs_tmp"
docker cp tmp:/opt/PotreeConverter/resources/page_template/index.html "$OUTPUT/"
docker rm tmp
rm -rf "$OUTPUT/libs"
mv "$OUTPUT/libs_tmp" "$OUTPUT/libs"

echo "変換完了: $OUTPUT"
echo "確認: python3 -m http.server 8080 -d $OUTPUT"
```

```bash
chmod +x convert.sh
./convert.sh data/origin.las potree_output
```

## ローカルでの確認

```bash
python3 -m http.server 8080 -d potree_output
# または
npx serve potree_output
```

`http://localhost:8080/index.html` をブラウザで開きます。`file://` では動作しません。

## 運用上のポイント

### ボリュームマウントのパス

- Docker Desktop for Macでは `/Users` 配下はデフォルトでマウント可能
- 外付けドライブ（`/Volumes/...`）を使う場合は Docker Desktop → Settings → Resources → File sharing でパスを追加する

### CloudCompareからのLASエクスポート

- CloudCompareでGlobal Shiftが適用されている場合、エクスポートしたLASのバウンディングボックスがすべて0になり、PotreeConverterが `#points: 0` として扱うことがある
- ScaniverseからエクスポートしたオリジナルのLASファイルであれば問題なく変換できる（切り分けに使える）
- CloudCompareで編集したLASを使う場合は、エクスポート時の座標オフセット設定を確認する
