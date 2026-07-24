#!/usr/bin/env python3
"""fgd2tif.py — 基盤地図情報 数値標高モデル(JPGIS GML)をGeoTIFFへ一括変換する。

用途:
    fgd.gsi.go.jp からダウンロードした zip（FG-GML-*-DEM10B-*.zip 等)を
    そのまま渡すと、展開・パース・結合して 1枚の dem_src.tif を出力する。

使い方:
    pip install rasterio numpy
    python3 fgd2tif.py FG-GML-*.zip -o dem_src.tif
    python3 fgd2tif.py *.xml -o dem_src.tif        # 展開済みxmlでも可

仕様メモ:
    - 出力CRSは EPSG:6668（地理座標）。2025年以降のデータは srsName が
      jgd2024.bl だが、JGD2024は鉛直基準の改定で緯度経度は不変のため
      EPSG:6668 の継続使用が正しい（標高値はJGD2024基準になる点に留意）。
    - 「データなし」等の非数値・海水面等は NoData(-9999) にする。
    - tupleList は startPoint オフセット + "+x-y" 順(西→東、北→南)を前提とする。
      DEM10B/5A/5B/1m(DEM1A) いずれも同一構造。
"""

import argparse
import glob
import io
import re
import sys
import zipfile
from pathlib import Path

import numpy as np

try:
    import rasterio
    from rasterio.merge import merge as rio_merge
    from rasterio.transform import from_bounds
except ImportError:
    sys.exit("rasterio が必要です: pip install rasterio numpy")

NODATA = -9999.0

# 名前空間に依存しないタグ抽出（fgd/gmlのprefix揺れを吸収する）
def _find(text, tag):
    m = re.search(rf"<(?:\w+:)?{tag}(?:\s[^>]*)?>(.*?)</(?:\w+:)?{tag}>", text, re.S)
    return m.group(1).strip() if m else None


def parse_fgd_xml(text):
    """1枚のFGD DEM XMLを (array, bounds) に変換する。bounds=(w,s,e,n)。"""
    lower = _find(text, "lowerCorner")  # "lat lon"
    upper = _find(text, "upperCorner")
    low = _find(text, "low")            # "0 0"
    high = _find(text, "high")          # "ncols-1 nrows-1"
    if not all([lower, upper, low, high]):
        raise ValueError("必須タグ(lowerCorner/upperCorner/low/high)が見つからない")

    s_lat, w_lon = map(float, lower.split())
    n_lat, e_lon = map(float, upper.split())
    x0, y0 = map(int, low.split())
    x1, y1 = map(int, high.split())
    ncols, nrows = x1 - x0 + 1, y1 - y0 + 1

    # startPoint: 先頭何セルが省略されているか（"x y"）
    sp = _find(text, "startPoint")
    sx, sy = (map(int, sp.split()) if sp else (0, 0))
    start_index = sy * ncols + sx

    tuples = _find(text, "tupleList") or ""
    arr = np.full(nrows * ncols, NODATA, dtype=np.float32)
    i = start_index
    for line in tuples.splitlines():
        line = line.strip()
        if not line:
            continue
        # "地表面,135.42" / "データなし,-9999." など
        parts = line.split(",")
        try:
            v = float(parts[-1])
        except ValueError:
            v = NODATA
        if v <= -9998:  # -9999. 系の欠測表現
            v = NODATA
        if i < arr.size:
            arr[i] = v
        i += 1

    grid = arr.reshape(nrows, ncols)  # 北→南、西→東 = そのまま行順でよい
    return grid, (w_lon, s_lat, e_lon, n_lat)


def iter_xml_sources(paths):
    """引数(zip/xml/グロブ)からxmlテキストを順に取り出す。"""
    for p in paths:
        for f in sorted(glob.glob(p)) or [p]:
            fp = Path(f)
            if fp.suffix.lower() == ".zip":
                with zipfile.ZipFile(fp) as z:
                    for name in z.namelist():
                        if name.lower().endswith(".xml") and "DEM" in name.upper():
                            yield name, z.read(name).decode("utf-8", "replace")
            elif fp.suffix.lower() == ".xml":
                yield fp.name, fp.read_text(encoding="utf-8", errors="replace")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("inputs", nargs="+", help="FGDのzipまたはxml（複数可・グロブ可）")
    ap.add_argument("-o", "--output", default="dem_src.tif")
    args = ap.parse_args()

    tmp_datasets = []
    count = 0
    for name, text in iter_xml_sources(args.inputs):
        try:
            grid, (w, s, e, n) = parse_fgd_xml(text)
        except ValueError as err:
            print(f"skip {name}: {err}", file=sys.stderr)
            continue
        transform = from_bounds(w, s, e, n, grid.shape[1], grid.shape[0])
        mem = rasterio.io.MemoryFile()
        ds = mem.open(
            driver="GTiff", height=grid.shape[0], width=grid.shape[1],
            count=1, dtype="float32", crs="EPSG:6668",
            transform=transform, nodata=NODATA,
        )
        ds.write(grid, 1)
        # merge用に読み直し可能な状態で保持
        ds.close()
        tmp_datasets.append(mem.open())
        count += 1
        print(f"parsed {name}: {grid.shape[1]}x{grid.shape[0]}")

    if not tmp_datasets:
        sys.exit("変換対象が見つかりませんでした")

    mosaic, out_transform = rio_merge(tmp_datasets, nodata=NODATA)
    meta = tmp_datasets[0].meta.copy()
    meta.update(height=mosaic.shape[1], width=mosaic.shape[2],
                transform=out_transform, compress="deflate")
    with rasterio.open(args.output, "w", **meta) as dst:
        dst.write(mosaic)
    for d in tmp_datasets:
        d.close()
    print(f"OK: {count}メッシュ -> {args.output}")
    print("次: gdalinfo -stats で確認（01の手順へ）")


if __name__ == "__main__":
    main()
