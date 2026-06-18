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

1. オリエンテーション
1. 昨年度研究会の内容を振り返る 
1. WebGISについて
1. WebGISを構成する技術


---