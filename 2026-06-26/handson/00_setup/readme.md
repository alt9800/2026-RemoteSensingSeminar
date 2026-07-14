# 事前セットアップ — 第2回

現地開催です。当日までに以下を確認してください。

---

## 第1回からの持ち物

- 生成した `fude.pmtiles`（第1回ハンズオンの成果物）
- 第1回で動作確認済みの `index.html`

どちらも USB メモリまたはクラウドストレージ経由で持参してください。

---

## Nginx

### macOS

```bash
brew install nginx
nginx -v
# nginx/1.x.x
```

起動・停止：

```bash
brew services start nginx
brew services stop nginx
# または
nginx
nginx -s stop
```

設定ファイルの場所：`/opt/homebrew/etc/nginx/nginx.conf`（Apple Silicon）

### Linux (Ubuntu / Debian)

```bash
sudo apt install nginx
nginx -v
sudo systemctl start nginx
sudo systemctl status nginx
```

設定ファイルの場所：`/etc/nginx/nginx.conf`

### Windows

WSL 内で Linux の手順を実行してください。

---

## Martin（当日インストール）

第1回ではデモ確認にとどめましたが、今回は手元で起動します。

### macOS / Linux

```bash
brew install martin
# または
cargo install martin

martin --version
```

### Linux（バイナリ取得）

```bash
curl -L https://github.com/maplibre/martin/releases/latest/download/martin-aarch64-unknown-linux-gnu.tar.gz \
  | tar xz   # ARM の場合
# x86_64 の場合は x86_64-unknown-linux-gnu
sudo mv martin /usr/local/bin/
martin --version
```

### Windows

WSL 内で Linux の手順を実行してください。

---

## Maputnik（インストール不要）

Web 版をブラウザで使います。

```
https://app.maputnik.com/
```

ローカルの PMTiles を Maputnik から参照するには、
ローカルサーバーが起動している必要があります（後述）。

---

## 動作確認チェックリスト

当日の開始前に以下を確認してください。

- [ ] `nginx -v` でバージョンが表示される
- [ ] `fude.pmtiles` が手元にある
- [ ] `python3 -m http.server 8000` でローカルサーバーが起動する
- [ ] `https://app.maputnik.com/` がブラウザで開ける