---
marp: true
theme: default
header: "衛星データ解析技術研究会<br>技術セミナー（応用編）第一回 2026/06/19"
footer: "第1回：タイル配信①：データ構造とパース"

paginate: true

style: |
    section.title {
        justify-content: center;
        text-align: center;
    }
    .round-icon {
      position: absolute;
      top: 50px;
      right: 50px;
      width: 400px;
      height: 400px;
      border-radius: 20%;
      object-fit: cover;
      z-index: 10;
    }
    .tiny-text {
      font-size: 0.6em;
    }
    /* 画像グリッド用 */
    .grid-4 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 20px;
      height: 70%;
    }
    .grid-4 > p {
      margin: 0;
      height: 100%;
    }
    .grid-4 img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }


---
---
## 衛星データ解析技術研究会<br>技術セミナー（応用編）
### Webアプリケーションの開発技術の習得

# 第1回：タイル配信①：データ構造とパース

第一回 2026/06/19

担当講師 : 田中聡至

---

## 本日のテーマ

第1回：タイル配信①：データ構造とパース

1. ガイダンス（全6回の位置づけ、到達目標の確認）
1. WebGISタイル配信エコシステムの概論
1. ラスタータイルとベクタータイル（MVT/PMTiles）の違い
1. タイルサーバー比較環境の構築・起動
1. タイルピラミッド／XYZ・TMS・WMTSの仕組み
1. GISレンダリングエンジンのタイル読み込み処理を読む
1. ハンズオン：tippecanoeによるMVT生成
1. まとめ・次回への接続

---
