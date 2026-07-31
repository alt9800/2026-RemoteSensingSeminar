# Pi Zero 2W + Martin タイルサーバー検証メモ

FOSS4G 2026 Hiroshima ワークショップに向けた検証記録。
参加者に Pi を貸し出し、SSH 接続 → Martin 操作 → MapLibre GL JS で可視化する 3 時間構成を想定。


[index.html](./foryourpc)をつけているので、これを自分のPCで動かして、martinから配信されるタイルを取得する

---

## 検証済み構成

| 項目 | 内容 |
|---|---|
| ハードウェア | Raspberry Pi Zero 2W（ARM Cortex-A53 x4, 512MB RAM） |
| OS | Raspberry Pi OS Lite 64-bit（aarch64 必須） |
| タイルサーバー | Martin v1.11.0（`martin-aarch64-unknown-linux-musl`） |
| データ | PMTiles（MBTiles も可）。PostGIS は RAM 不足のため除外 |
| フロントエンド | MapLibre GL JS v4（Mac 側で配信） |

Martin + PMTiles の配信が Pi Zero 2W 上で動作することを確認済み。
宇部市の筆ポリゴン PMTiles（zoom 10–17）を Martin で配信し、MapLibre GL JS から描画できた。

---

## 接続構成

```
Mac（HTML を http.server 等で配信）
  ↓ ブラウザで index.html を開く
  ↓ Martin のタイルエンドポイントにリクエスト
Pi Zero 2W（Martin:3000 でタイルを配信）
```

Pi 側には HTML を置かない。Mac 側の HTML が Pi の Martin に接続する構成。

---

## Raspberry Pi Imager の注意点

- SSH 認証方式は「パスワード認証を使う」を選択する
  - 「Use public key authentication」はバグがあり誤った鍵が複数登録されることがある
- パスワードは事前にメモ帳等で用意してコピーする
- ユーザー名とホスト名は独立した設定項目であることに注意
- 焼き直した場合は `ssh-keygen -R <IP>` で known_hosts を削除する

---

## SSH 鍵設定

```bash
# 鍵転送（ユーザー名@ホスト名 を明示すること）
ssh-copy-id -i ~/.ssh/id_ed25519.pub zero2w@zero2w-2026
```

```
# ~/.ssh/config
Host zero2w-2026
  HostName 192.168.2.103
  User zero2w
  IdentityFile ~/.ssh/id_ed25519
```

---

## Martin のインストール（Pi 上で実行）

```bash
curl -OL https://github.com/maplibre/martin/releases/latest/download/martin-aarch64-unknown-linux-musl.tar.gz
tar -xzf martin-aarch64-unknown-linux-musl.tar.gz
chmod +x martin
sudo mv martin /usr/local/bin/
martin --version
# martin 1.11.0
```

---

## 起動と確認

```bash
# Pi 上で
martin ~/fude.pmtiles

# ブラウザ or curl で確認
http://<PI_IP>:3000/catalog
http://<PI_IP>:3000/fude        # TileJSON
http://<PI_IP>:3000/fude/{z}/{x}/{y}  # タイル本体
```

---

## 今後の検討事項

### 1. タイルデータの準備（FOSS4G Hiroshima 向け）

広島市周辺の PMTiles を用意する。

```bash
# OpenFreeMap の planet.pmtiles から抽出する場合
pmtiles extract planet.pmtiles hiroshima.pmtiles \
  --bbox=132.2,34.2,133.0,34.6

# tilemaker + OSM データから生成する場合
tilemaker --input hiroshima.osm.pbf --output hiroshima.pmtiles
```

### 2. systemd による自動起動

```bash
# /etc/systemd/system/martin.service
[Unit]
Description=Martin tile server
After=network.target

[Service]
User=zero2w
ExecStart=/usr/local/bin/martin /home/zero2w/fude.pmtiles
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable martin
sudo systemctl start martin
```

### 3. リソース計測

```bash
free -h      # メモリ使用量
htop         # CPU 使用率（同時接続時）
```

### 4. ワークショップのコンテンツ拡張

chiitiler（ラスタータイルサーバー）との比較を検討中。
chiitiler は MapLibre Style → PNG/WebP を生成するため Pi Zero 2W では重い可能性があり、Pi 4 との役割分担になる見込み。

| 機材 | 役割 | 状態 |
|---|---|---|
| Pi Zero 2W | Martin + PMTiles（ベクター配信） | 確認済み |
| Pi 4 | chiitiler（ラスター生成） | 未検証 |

「ラスター配信 vs ベクター配信のアーキテクチャの違い」を体験で示す切り口になる。

---

## 参照

- Martin ドキュメント: https://maplibre.org/martin/
- `04_raspi/SETUP.md`（Pi 3B+ の構成・Nginx による静的配信）