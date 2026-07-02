# Nginx による PMTiles 静的配信

---

## インストール

```bash
# Ubuntu / Debian
sudo apt install nginx

# macOS
brew install nginx

# Windows → WSL 内で Ubuntu の手順を実行
```

---

## 設定ファイル

`/etc/nginx/sites-available/tiles` を作成する。

```nginx
server {
    listen 80;
    server_name _;          # IP アドレスでのアクセスも受け付ける
    root /var/www/tiles;    # PMTiles を置くディレクトリ

    location / {
        # CORS — MapLibre からのクロスオリジンリクエストを許可
        add_header Access-Control-Allow-Origin "*";
        add_header Access-Control-Allow-Methods "GET, OPTIONS";
        add_header Access-Control-Allow-Headers "Range";

        # Range Request を受け付けると宣言（PMTiles に必須）
        add_header Accept-Ranges bytes;

        # OPTIONS プリフライトリクエストへの対応
        if ($request_method = OPTIONS) {
            return 204;
        }

        try_files $uri $uri/ =404;
    }
}
```

有効化：

```bash
sudo ln -s /etc/nginx/sites-available/tiles /etc/nginx/sites-enabled/
sudo nginx -t        # 文法チェック
sudo nginx -s reload
```

---

## ファイルの配置

```bash
sudo mkdir -p /var/www/tiles
sudo cp fude.pmtiles /var/www/tiles/
sudo chown -R www-data:www-data /var/www/tiles
```

---

## 動作確認

```bash
# Range Request が通るか確認
curl -I -H "Range: bytes=0-511" http://localhost/fude.pmtiles
# HTTP/1.1 206 Partial Content が返れば OK
```

MapLibre からの接続：

```js
map.addSource('fude', {
  type: 'vector',
  url: 'http://サーバーIP/fude.pmtiles'
  // pmtiles:// プロトコルが不要（Martin と異なりファイル直参照）
  // → ただし pmtiles.Protocol() の登録は引き続き必要
});
```

---

## よくあるエラー

| 症状 | 原因 | 対処 |
|---|---|---|
| `CORS error` | `Access-Control-Allow-Origin` がない | Nginx の設定を確認 |
| `206` が返らない | `Accept-Ranges bytes` がない | ヘッダーを追加 |
| `404` | ファイルパスが違う | `root` と実ファイルの場所を確認 |
| 表示されない | `pmtiles.Protocol()` を登録していない | JS 側の設定を確認 |