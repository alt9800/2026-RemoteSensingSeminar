# Rust と地理空間情報処理ツールの動向

---

## なぜ地理空間情報処理ツールで Rust が増えているのか

ここ数年、地理空間処理ツールの実装言語として Rust の採用が目立って増えています。

| ツール | 言語 | 備考 |
|---|---|---|
| Martin | Rust | 本講義で使うタイルサーバー |
| PMTiles（仕様実装） | Rust / Go / JS | Rust 実装が最も成熟 |
| GeoArrow | Rust | 地理空間データの列指向フォーマット |
| GDAL（Rust バインディング） | Rust + C | `gdal` クレートで GDAL をラップ |
| OGR / PROJ（バインディング） | Rust + C | `proj` クレート |

共通する理由は「C/C++ 相当のパフォーマンスをメモリ安全に実現できる」点です。  
大規模な地理空間データ処理はメモリを大量に使うため、Rust の所有権モデルが適合しやすい。

---

## WASM 化の流れ

Rust は WebAssembly（WASM）へのコンパイルを正式にサポートしており、  
ブラウザ上で C/C++ 相当の処理を動かす流れが加速しています。

```
Rust コード
  └─ wasm-pack でビルド
       └─ .wasm + JS グルーコード
            └─ ブラウザで動作
```

**FOSS4G(地理空間情報処理ツール) エコシステムでの具体例：**

- `gdal3.js`：GDAL を Emscripten でコンパイル → ブラウザで `ogr2ogr` 相当が動く
- `GeoRust/geo` の WASM ビルド：ブラウザ内で座標変換・空間演算が可能
- PMTiles の JS ライブラリ（`pmtiles`）：Rust 実装の移植を含む

---

## Rust 環境のセットアップ

今すぐ書く必要はありませんが、`cargo install martin` が動くかどうかの確認として。

### インストール（全 OS 共通）

```bash
# macOS / Linux
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Windows
# https://rustup.rs/ から rustup-init.exe をDL・実行
```

インストール後：

```bash
rustup update          # ツールチェーンを最新に
rustc --version        # rustc 1.x.x (...)
cargo --version        # cargo 1.x.x (...)
```

### Martin を cargo でインストールしてみる

```bash
cargo install martin
# → ~/.cargo/bin/martin にインストールされる
martin --version
```

`brew install martin` の代替として使えます。  
インストール時間はネットワーク速度に依存しますが、初回は数分かかります。

---

## 関連クレート（Rust のパッケージ）

興味があれば眺めてみてください。

```toml
# Cargo.toml の例
[dependencies]
geo       = "0.28"   # 空間演算（交差・バッファ・面積計算など）
proj      = "0.27"   # 座標変換（EPSG:6668 → EPSG:4326 など）
gdal      = "0.16"   # GDAL バインディング（ラスター・ベクター読み書き）
pmtiles   = "0.5"    # PMTiles の読み書き
geojson   = "0.24"   # GeoJSON のパース・生成
```

---

## 今の時点での立ち位置

Rust を書けなくても、本講義の内容は問題なく進められます。  
ただし、今後 地理空間情報処理ツールを深く使っていくと：

- ツールのソースを読む場面が増える（Martin・tippecanoe の issue など）
- WASM 化されたライブラリをフロントエンドに組み込む機会が出てくる
- パフォーマンスが必要な処理を自分で書きたくなる

という場面で Rust の知識が役に立ちます。