---
marp: true
theme: default
header: "衛星データ解析技術研究会<br>技術セミナー（応用編）第二回 2026/06/26"
footer: "第2回：タイル配信②：自前配信とカートグラフィック"

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

# 第2回：タイル配信②：自前配信とカートグラフィック

第二回 2026/06/26

担当講師 : 田中聡至

---

## 本日のテーマ

第2回：タイル配信②：自前配信とカートグラフィック

1. 前回成果物（MVT/PMTiles）の確認
1. Nginxによる静的配信設定
1. Maputnikでのスタイル設計
1. MapLibre GL JSによるレンダリング実装
1. 地図スタイリングサービス群の整理（MapTiler／Carto／Felt）
1. OSMエコシステムにおける自データの位置づけ
1. 「どのレベルで自作するか」の判断基準・配信形態の考察
1. ハンズオン：Nginx＋PMTiles構成の自前タイルサーバー構築
1. まとめ・到達目標確認


---
