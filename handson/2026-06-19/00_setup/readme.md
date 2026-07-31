# 事前環境構築ガイド — 第1回

ハンズオンで使用するツールの確認手順です。  
時間があるときに `動作確認` の欄のコマンドが通ることを確認してください。

---

## 1. GDAL / ogr2ogr

座標変換（JGD2011 → WGS84）に使います。

### macOS

```bash
brew install gdal
```

### Linux (Ubuntu / Debian)

```bash
sudo apt update && sudo apt install gdal-bin
```

### Windows

**OSGeo4W インストーラー**（推奨）：  
https://trac.osgeo.org/osgeo4w/

QGIS をインストール済みの場合、`OSGeo4W Shell` から `ogr2ogr` が使えます。

### 動作確認

```bash
ogr2ogr --version
# GDAL 3.x.x, released ...
```

---

## 2. tippecanoe

GeoJSON → PMTiles（ベクタータイル）の変換に使います。

### macOS

```bash
brew install tippecanoe
```

### Linux (Ubuntu / Debian)

```bash
sudo apt install tippecanoe
```

リポジトリにない場合はソースビルド：

```bash
git clone https://github.com/felt/tippecanoe.git
cd tippecanoe
make -j
sudo make install
```

### Windows

**ネイティブビルドは存在しません。WSL を使用してください。**

WSL のインストール（PowerShell を管理者権限で実行）：

```powershell
wsl --install
# 再起動後、Ubuntu が起動したら上記 Linux 手順を実行
```

WSL がすでに有効な場合：

```bash
# WSL の Ubuntu 内で
sudo apt update && sudo apt install tippecanoe
```

### 動作確認

```bash
tippecanoe --version
# tippecanoe v2.x.x
```

---

## 3. Python（ローカル HTTP サーバー用）

`pmtiles://` プロトコルは `file://` では動作しないため、ローカルサーバーが必要です。

### macOS / Linux

Python 3 が標準搭載されているため追加インストール不要。

### Windows

https://www.python.org/downloads/ からインストーラーをDL。  
インストール時に「Add Python to PATH」にチェックを入れる。

### 動作確認

```bash
# macOS / Linux
python3 --version

# Windows
python --version
```

### 代替：Node.js の serve

```bash
npx serve .
# → http://localhost:3000 で起動
```

---

## 4. ブラウザの DevTools

Chrome または Edge を推奨します。  
ハンズオン中に以下のタブを使います：

- **Network タブ**：PMTiles への Range Request を観察
- **Memory タブ**：GeoJSON source 使用時のメモリ展開を確認
- **Console タブ**：MapLibre のエラーログ確認

---

## 5. テキストエディタ

HTML・JS を編集できるものであれば何でも構いません。  
VSCode を推奨（拡張機能 `Live Server` があると便利）。

---

## 事前データのダウンロード

農林水産省「農業用地利用状況調査（筆ポリゴン）」  
https://open.fude.maff.go.jp/

山口県のShapefileをダウンロードして、`handson/01_pmtiles/` に展開してください。  
ファイル群（`.shp` / `.dbf` / `.prj` / `.shx`）がそろっていることを確認してください。