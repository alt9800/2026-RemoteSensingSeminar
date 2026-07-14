# ラズパイタイルサーバー セットアップ手順

第2回（2026/06/26）デモ①の構築メモ。講師側の作業記録。

---

## 構成概要

Nginx のみで完結（Martin 不要）。PMTiles は Range Request 対応の静的配信、PNG タイルは XYZ ディレクトリ配信、どちらも Nginx で処理できる。

```
Raspberry Pi 3B+（OS Lite 64-bit）
├── Nginx
│    ├── /var/www/html/raster.html
│    ├── /var/www/html/vector.html
│    ├── /var/www/html/fude.pmtiles   ← ベクタータイル（41MB）
│    └── /var/www/html/tiles/         ← ラスタータイル（~10MB）
└── Tailscale（外部接続・SSH用）
```

---

## データパイプライン（Mac 側作業）

### 0. 作業ディレクトリと osmium-tool の準備

```bash
mkdir -p ~/Desktop/experiments/2026-06-20/ube-map
cd ~/Desktop/experiments/2026-06-20/ube-map

brew install osmium-tool
osmium version
```

### 1. Python 仮想環境のセットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install Pillow shapely pyproj
pip list | grep -E "Pillow|shapely|pyproj"
```

次回以降は `source .venv/bin/activate` だけ実行すれば OK。`deactivate` で venv を抜けられる。

### 2. OSM データの取得とクリップ

```bash
curl -L -o chugoku-latest.osm.pbf \
  https://download.geofabrik.de/asia/japan/chugoku-latest.osm.pbf

osmium extract \
  --bbox 131.18,33.92,131.37,34.17 \
  --output ube.osm.pbf \
  chugoku-latest.osm.pbf

ls -lh ube.osm.pbf
```

### 3. export.json の作成

`osmium export` はこの設定ファイルで OSM タグを線（LineString）として扱うか面（Polygon）として扱うかを判断する。ファイルがないか空だとエラーになる。

```bash
cat > export.json << 'EXPORTEOF'
{
    "attributes": {
        "type": false, "id": false, "version": false,
        "changeset": false, "timestamp": false,
        "uid": false, "user": false, "way_nodes": false
    },
    "linear_tags": ["highway", "waterway", "railway"],
    "area_tags": ["building", "landuse", "natural", "leisure"]
}
EXPORTEOF
```

`attributes` はメタデータを GeoJSON に含めるかどうかのフラグ。すべて `false` にすることで geometry と properties だけの軽量な出力になる。

### 4. GeoJSON エクスポート

```bash
osmium export \
  --geometry-types=linestring,polygon \
  --config=export.json \
  --output=ube.geojson \
  ube.osm.pbf

ls -lh ube.geojson
```

`--geometry-types=linestring,polygon` でポイントを除外している。

### 5. タイル生成

```bash
# z10/z13 で先に動作確認してから z16 を流す
python generate_tiles.py --input ube.geojson --zooms 10,13
python generate_tiles.py --input ube.geojson --zooms 10,13,16

find tiles -name "*.png" | wc -l
du -sh tiles/
```

z10 は水域・森林・主要道路のみ、約4枚・数秒。z13 は河川・生活道路・鉄道・公園が追加、約45枚・数分。z16 は建物が追加、約1,500枚・20〜40分。

---

## Pi セットアップ

### 1. Nginx インストール・設定

```bash
sudo apt update && sudo apt install -y nginx
sudo systemctl status nginx
```

`/etc/nginx/sites-available/default` を以下で置き換える。既存の設定ブロックは削除し、このブロックだけにすること（2ブロック共存すると想定外の方が優先される）。

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html;
    server_name _;

    add_header Access-Control-Allow-Origin *;
    add_header Access-Control-Allow-Methods 'GET, OPTIONS';
    add_header Access-Control-Allow-Headers 'Range';

    location ~* \.pmtiles$ {
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Expose-Headers 'Content-Length, Content-Range';
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
```

設定後、`sites-enabled/` にシムリンクがあるか確認する。ないと 404 になる。

```bash
ls -la /etc/nginx/sites-enabled/
# default へのシムリンクがなければ作る
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

sudo nginx -t
sudo systemctl reload nginx
```

### 2. 自動起動の有効化

再起動後も Tailscale と Nginx が上がるよう、事前に設定しておく。

```bash
sudo systemctl enable tailscaled
sudo systemctl enable nginx
```

### 3. Tailscale セットアップ

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# → ブラウザで認証 URL が表示されるので Mac で開いて認証

tailscale ip -4   # → 100.x.x.x（今回は 100.66.201.10）
```

Tailscale は講師が Pi に SSH する手段として使う。参加者は Tailscale 不要。

### 4. ファイル転送（Mac → Pi）

転送前にパーミッションを確認する。

```bash
# Pi 上で
sudo chown -R pi3-2026:pi3-2026 /var/www/html/
```

Mac からイントラの IP（ローカル IP）を使って rsync で転送する。Tailscale IP ではなくローカル IP を使うこと。

```bash
rsync -avz --progress \
  ~/Desktop/experiments/2026-06-20/ube-map/tiles/ \
  pi3-2026@<LOCAL_IP>:/var/www/html/tiles/

rsync -avz --progress \
  ~/Desktop/experiments/2026-06-20/ube-map/fude.pmtiles \
  pi3-2026@<LOCAL_IP>:/var/www/html/fude.pmtiles

rsync -avz --progress \
  raster.html vector.html \
  pi3-2026@<LOCAL_IP>:/var/www/html/
```

---

## 当日の接続：フォールバック構成

会場ネットワークの制約はフタを開けるまでわからないため、順番に試せる準備をしておく。

### ① 会場 WiFi + ローカル IP（優先）

```
http://<PI_LOCAL_IP>/raster.html
http://<PI_LOCAL_IP>/vector.html
```

条件：会場 WiFi が AP isolation なし（デバイス間通信を許可）。LAN スキャンで Pi の IP を確認してからアナウンスする。mDNS が通る環境では `http://raspi3bp-2026/raster.html` でも届く場合がある。

### ② Cloudflare Tunnel（① が使えない場合の推奨）

Pi 側だけセットアップすれば参加者は普通のブラウザでアクセスできる。Tailscale のように参加者側の設定は一切不要。

```bash
# Pi 上で実行（アカウント不要、クイックトンネル）
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 \
  -o cloudflared && chmod +x cloudflared
./cloudflared tunnel --url http://localhost:80
# → https://xxxxxxxx.trycloudflare.com が発行される
```

発行された URL を QR コードにしてスクリーンに表示すれば参加者はそこにアクセスするだけ。

条件：Pi がインターネットに出られること（会場 WiFi 経由で OK）。

### ③ Tailscale 経由

```
http://100.66.201.10/raster.html
http://100.66.201.10/vector.html
```

参加者全員が Tailscale アカウントを持っている必要があるため、工数が大きく一般的なセミナーには不向き。講師の手元からの動作確認用として使う。

### ④ GL-SFT1200 を持ち込んで独自サブネットを作る（根本解決）

```
会場 WiFi（WAN 側）
    ↓ リピーターモード
GL-SFT1200（192.168.8.1）
    ├── LAN 有線 → Pi 3B+（安定）
    └── WiFi    → 参加者デバイス
```

Pi を有線 LAN で繋ぐことで WiFi の不安定さも解消される。参加者は GL-SFT1200 の WiFi に接続するだけで Pi への HTTP アクセスが通る。AP isolation の問題を根本から断てる。

### ⑤ Pi をアクセスポイント化（インターネット完全不要）

```bash
sudo apt install -y hostapd dnsmasq

sudo tee /etc/hostapd/hostapd.conf << 'HOSTAPDEOF'
interface=wlan0
driver=nl80211
ssid=ube-map
hw_mode=g
channel=6
auth_algs=1
wpa=2
wpa_passphrase=ubemap2026
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
HOSTAPDEOF

sudo tee -a /etc/dnsmasq.conf << 'DNSEOF'
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
DNSEOF

sudo ip addr add 192.168.4.1/24 dev wlan0
sudo systemctl unmask hostapd
sudo systemctl enable hostapd dnsmasq
sudo systemctl start hostapd dnsmasq
```

受講者への案内：

```
WiFi SSID : ube-map
パスワード : ubemap2026
地図 URL  : http://192.168.4.1/raster.html
            http://192.168.4.1/vector.html
```
過程のSSIDとパスワードです


この構成に切り替えると Pi 自身がインターネットに出られなくなり Tailscale SSH も不可になる。切り替え前に設定を完全に済ませ、緊急時の操作手段として有線 LAN（eth0）経由の SSH を確保しておくこと。

---

## 参照

- GB-map ノウハウ（generate_tiles.py のベース）: `2026-06-19/handson/05_gb_map/NOTES.md`
- Martin の位置づけ：Pi + Martin の実機ハンズオンは FOSS4G Hiroshima 2026 で別途実施予定