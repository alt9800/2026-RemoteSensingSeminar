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

次回以降は `source .venv/bin/activate` だけ実行すれば OK。

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

### 4. GeoJSON エクスポート

```bash
osmium export \
  --geometry-types=linestring,polygon \
  --config=export.json \
  --output=ube.geojson \
  ube.osm.pbf

ls -lh ube.geojson
```

### 5. タイル生成

```bash
# z10/z13 で先に動作確認してから z16 を流す
python generate_tiles.py --input ube.geojson --zooms 10,13
python generate_tiles.py --input ube.geojson --zooms 10,13,16

find tiles -name "*.png" | wc -l
du -sh tiles/
```

| zoom | 表示内容 | 枚数目安 | 所要時間 |
|---|---|---|---|
| z10 | 水域・森林・主要道路 | ~4 枚 | 数秒 |
| z13 | z10 + 河川・生活道路・鉄道・公園 | ~45 枚 | 数分 |
| z16 | z13 + 建物 | ~1,500 枚 | 20〜40 分 |

カラーパレット（トポ風）：

| レイヤー | 色 |
|---|---|
| 陸地 | `#f2ede4` |
| 森林・公園 | `#b8d4a8` |
| 水域・湖 | `#89bdd3` |
| 河川 | `#6aaec6` |
| 主要道路 | `#e8c87a` |
| 生活道路 | `#cfc9bf` |
| 建物 | `#dcd2c6` |

---

## Pi セットアップ

### 1. Nginx インストール・設定

```bash
sudo apt update && sudo apt install -y nginx
sudo systemctl status nginx
```

`/etc/nginx/sites-available/default` を以下で置き換える：

```nginx
server {
    listen 80;
    server_name _;
    root /var/www/html;
    index index.html;

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

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 2. Tailscale セットアップ

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# → ブラウザで認証 URL が表示されるので Mac で開いて認証

tailscale ip -4   # → 100.x.x.x
```

Mac から疎通確認：

```bash
curl http://<TAILSCALE_IP>/
```

### 3. ファイル転送（Mac → Pi）

```bash
# Pi の IP 確認（Pi 上で）
hostname -I

# Mac から rsync
rsync -avz --progress \
  ~/Desktop/experiments/2026-06-20/ube-map/tiles/ \
  pi@<PI_IP>:/var/www/html/tiles/

rsync -avz --progress \
  ~/Desktop/experiments/2026-06-20/ube-map/fude.pmtiles \
  pi@<PI_IP>:/var/www/html/fude.pmtiles

rsync -avz --progress \
  raster.html vector.html \
  pi@<PI_IP>:/var/www/html/
```

---

## 当日の接続：三段フォールバック

### ① 会場 WiFi + ローカル IP（優先）

```
http://<PI_LOCAL_IP>/raster.html
http://<PI_LOCAL_IP>/vector.html
```

条件：会場 WiFi が AP isolation なし（デバイス間通信を許可）。

### ② Tailscale 経由

```
http://100.66.201.10/raster.html
http://100.66.201.10/vector.html
```

条件：Pi がインターネットに出られること。

### ③ Pi をアクセスポイント化（完全オフライン）

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

> ③ に切り替えると Pi 自身がインターネットに出られなくなり Tailscale SSH も不可になる。
> 切り替え前に設定を完全に済ませておくこと。緊急時は有線 LAN（eth0）経由の SSH を確保。

---

## 参照

- GB-map ノウハウ（generate_tiles.py のベース）: `2026-06-19/handson/05_gb_map/NOTES.md`
- Martin の位置づけ：Pi + Martin の実機ハンズオンは FOSS4G Hiroshima 2026 で別途実施予定