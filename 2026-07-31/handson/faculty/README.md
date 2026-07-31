# 第6回 講師用引き継ぎ書（事前検証・当日運用）

本ドキュメントは講義前の動作検証を、別の作業環境・別のモデル（Claude Code等）で分担するための内部資料。参加者向けではない。

作成日: 2026-07-31 / 前提資料: 「広域DEMデータ処理の試行錯誤記録」（第5回パイプラインの広域適用メモ）

---

## 1. データの現在地

| 項目 | 状態 |
|------|------|
| `terrain_composite_ube_yamaguchi.pmtiles`（本番・5m基本層＋1m差し替え） | **未生成**。Claude Codeでの実行待ち |
| `terrain_1m_503172.pmtiles`（単一メッシュサンプル） | 生成済み・検分済み（下記2参照） |
| `terrain_rgb_503172.tif`（Terrain RGB化済みGeoTIFF） | 生成済み・検分済み（下記2参照） |
| NDWIラスタータイル | **未確認**。生成状況を要確認 |
| `tameike.geojson`（属性リネーム済み） | **未確認**。国土数値情報からの抽出・属性付け替えの実施有無を要確認 |
| PLATEAUの対象都市tileset URL | **未確認**（下記6参照） |

## 2. サンプルデータの検分結果（2026-07-31実施・確定事実）

### terrain_1m_503172.pmtiles

- z14–17、34タイル、PNG、非圧縮タイル
- bounds: 131.2500–131.2625 / 33.9750–33.9917（DEM1A実測範囲と整合。メタデータパッチは効いている）
- **既知の異常**: ヘッダの `center_lon` が **-83.49°**。boundsパッチ時にcenterが未修正とみられる。スタイル側でcenterを指定する限り実害はないが、`pmtiles show` で不審に見えるため、`fix_mbtiles_meta.py` にcenter書き込みを追加するのが望ましい（center = boundsの中点、center_zoom = minzoom）

### terrain_rgb_503172.tif

- EPSG:3857、1391x2237px、1m解像度、3バンドuint8。デコード検算済み（有効域の標高 0〜82.8m、宇部市沿岸部として妥当）
- **要注意**: 全ピクセルの**68%が(0,0,0)＝デコード値-10000m**。メモの `VALID_PERCENT≈32%` と整合。エンコード時にNoDataが黒（-10000m）として埋まっている
  - hillshadeではデータ縁が崖状ノイズになる
  - **terrain 3D表示では深さ10kmの穴になる。単一メッシュサンプルをそのまま3Dデモに使ってはいけない**
  - 本番の合成データでは5m基本層が埋めるため解消される見込みだが、合成後に必ず全域でNoData残りがないか確認すること（対象範囲の外周は5mでも埋まらない）
  - 単独サンプルを見せる用途では、NoDataを標高0mのエンコード値 **RGB=(1,134,160)** で置換する前処理を挟む（-10000 + (1*65536+134*256+160)*0.1 = 0.0）

### アップロードされていた検証ビューア（index.html）の不具合（修正済み）

`01_terrain3d/index.html` は以下を修正した版。旧版を配布しないこと。

1. ソース `minzoom: 8` に対し実データはz14開始 → 初期zoom 12で何も表示されない。**minzoom/maxzoomを実データに一致させ、初期zoomを14に変更**
2. クリック標高のズームが下限にクランプされていない → z14未満で常に「タイルなし」。`Math.max(MINZOOM, ...)` を追加
3. クリックのたびに `new pmtiles.PMTiles()` を生成していた → インスタンスを再利用に変更（動作には影響しないが無駄）
4. -10000m近傍を「NoData（被覆外）」表示に変更（生の数値を出すと質問が集中する）

## 3. 事前検証チェックリスト

検証環境ごとに以下を上から順に実施。コマンドと期待値を併記する。

### 3-1. 合成データ生成後の検分（最優先・composite生成が終わり次第）

```sh
pmtiles show terrain_composite_ube_yamaguchi.pmtiles
```

- [ ] minzoom=8 / maxzoom=17 になっているか（設計値）
- [ ] boundsが13メッシュの外接（概算 131.25–131.50 / 33.916–34.083 付近）になっているか
- [ ] **centerが(0,0)や負の経度になっていないか**（サンプルで再現した異常。fix_mbtiles_meta.pyの修正状況次第）
- [ ] ファイルサイズ。**GitHub Pagesに置く場合は100MB制限**。超える場合はSlack配布＋`pmtiles extract`での分割を検討

```sh
# デコード検算（rasterio。タイルを数枚読んで標高レンジを見る）
# 期待値: 対象範囲の標高レンジ（概ね0〜300m台）。-10000が出たらNoData残り
```

- [ ] 対象範囲の外周・海域で-10000mの穴が出ないか（`01_terrain3d`のクリック標高で抜き取り確認）
- [ ] 1m差し替え域（503172等）と5m域の境界が不自然な段差になっていないか（hillshadeで目視）

### 3-2. ハンズオン01（terrain3d）

- [ ] `python3 -m http.server` 配下で `01_terrain3d/index.html` が開き、初期表示で地形が出る
- [ ] TERRAIN_URLをcompositeに差し替え、CENTER/ZOOM/MINZOOM/MAXZOOMを更新（現状はサンプル用の値）
- [ ] 誇張スライダー・terrainトグル・hillshadeトグルが動く
- [ ] クリック標高が地理院地図の標高と±数m以内で一致（3点程度）
- [ ] iOS Safari / Android Chrome実機で表示・pitch操作ができる（terrain表示のフレームレートも見る）

### 3-3. ハンズオン02（Mapterhorn）

- [ ] `https://tiles.mapterhorn.com/{z}/{x}/{y}.webp` が会場ネットワークから到達できるか（**当日朝にも確認**。外部依存はここだけ）
- [ ] encoding=terrarium / tileSize=512 で正常表示、encoding=mapboxに変えると壊れることの再現（デモで見せる用）
- [ ] 到達不可時のフォールバック：Mapterhornの`pmtiles extract`で対象範囲を事前に切り出しローカル配布（bbox: 131.2,33.9,131.55,34.1 程度、数MB想定）。**切り出しファイルを事前に作っておくこと**

### 3-4. ハンズオン03（hazard_viewer）

- [ ] NDWIタイルの生成・配置（`ndwi/{z}/{x}/{y}.png`、z10–14）。**生成手順が現状どこにも記録されていなければ、生成時に手順をfacultyに追記**
- [ ] `tameike.geojson` の属性キーがreadme記載の `name` / `height` / `volume` になっているか。国土数値情報原本（W09_xxx系）のままなら付け替えスクリプトを実行
- [ ] ポップアップの属性が実データで正しく出る（欠損時に "-" 表示になることも確認）
- [ ] 現在位置トグル：HTTPS環境またはlocalhostでのみ動く（GeolocationはセキュアコンテキストPが必要）。**会場のIPアドレス配信で開く場合は動かない**ので、当日はlocalhost推奨と案内

### 3-5. 発展資料（04/05）

- [ ] 04: `pmtiles serve . --port 8080` のURL形式（`/{name}/{z}/{x}/{y}.png`）が手元のpmtiles CLIバージョンで一致するか実行して確認（CLIのバージョンによりパス形式が異なる可能性。readmeの記載は要実機確認）
- [ ] 05: **PLATEAUに宇部市（または近隣都市）の建物3D Tilesが収録されているか未確認**。PLATEAU配信サービスで確認し、tileset.json URLをreadmeの当日案内欄に記入。収録がなければ広島市等の収録都市に題材を差し替え（FOSS4G Hiroshimaワークショップとの連続性の観点でも広島は候補）
- [ ] 05のdeck.gl v9 + MapboxOverlay(interleaved) + Tile3DLayerの組み合わせは**コード未検証**。動作確認し、必要ならloaders.glのスクリプトタグを追記

## 4. 既知の障害と対処（第5回からの持ち越し・再掲）

詳細は試行錯誤記録を参照。要点のみ。

1. **rio-rgbify**: Python 3.14＋新GDALで `densify_pts must be at least 2` で停止（上流バグ、修正見込み薄）。EPSG:4326経由の回避策は例外握りつぶしでさらに悪化する。→ `gdal_calc.py` によるR/G/B個別エンコード＋`gdal_merge.py -separate` に切り替え済み
2. **gdal_translate -of MBTILES + gdaladdo**: bounds/minzoom/maxzoomメタデータが欠落することがある（原因未確証）。→ `fix_mbtiles_meta.py` でsqlite3直接パッチ。**centerの書き込み追加を推奨（2参照）**
3. **DEM1Aの被覆**: 2次メッシュの箱を埋めておらず、実測範囲内でも有効率3割程度。→ 5m基本層＋1m差し替えの合成方針（gdal_merge.pyのNoData非上書き挙動を利用）
4. **fgd2tif.pyのメモリ**: 全入力をMemoryFileで同時保持するため、メッシュ数に比例して消費。13メッシュは大きめのマシン前提

## 5. 当日運用メモ

- 配布経路: Slack `#seminar-2026` ＋ 静的ファイルURL（GitHub Pagesは100MB制限に注意。compositeが超えるならR2等の代替か、`pmtiles extract`で会場範囲のみの縮小版を配る）
- 会場ネットワークのAP分離時は第2回で確立した5段階フォールバック（Cloudflare Tunnel優先）
- 外部依存は地理院タイル・Mapterhorn・PLATEAU配信の3つ。すべてフォールバック（ローカル切り出し・題材変更）を用意しておく
- 時間が押した場合の削り順: 02（Mapterhorn比較は口頭＋デモに縮退）→ 発展紹介（資料参照の案内のみ）

## 6. 未解決事項（優先度順）

1. composite生成の完了と3-1の検分
2. NDWIタイル・tameike.geojsonの実データ確認（3-4）
3. PLATEAU対象都市の確認とURL確定（3-5）
4. pmtiles serveのURL形式・deck.gl統合コードの実機確認（3-5）
5. fix_mbtiles_meta.pyへのcenter書き込み追加
6. MBTILESメタデータ欠落のGDALバージョン依存性（余裕があれば。講義には影響しない）
