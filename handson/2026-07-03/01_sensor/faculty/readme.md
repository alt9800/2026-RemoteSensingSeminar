# ハンズオン① 講師用メモ

## 配信の準備

位置・方位センサーは Secure Context（HTTPS もしくは localhost）でしか動かない。スマホから開く以上、HTTPS 配信が前提になる。

- 既存の GitHub Pages に `index.html` を置き、そのURLをスマホで開くのが最も簡単（push で自動デプロイ）。
- `localhost` も Secure Context 扱いだが、講師PCの localhost に受講者のスマホは到達できない。同一LANのIP（`http://192.168.x.x`）は HTTP なので方位センサーが動かない。
- 会場ネットワークの都合で Pages が使えない場合は、HTTPS トンネル（例：ローカルサーバを一時的に公開する類のツール）で代替する。

## OS別の挙動（当日の説明ポイント）

- **iOS（Safari）**：`DeviceOrientationEvent.requestPermission()` が必要。**ユーザージェスチャ（ボタンタップ）の中**で呼ばないと拒否される。方位は `webkitCompassHeading`（0=北、時計回り）で真北基準の値が得られる。
- **Android（Chrome）**：権限ダイアログは基本不要。ただし HTTPS は必須。`deviceorientationabsolute` で絶対方位が得られ、`heading = (360 - alpha) % 360` で方位へ変換する。

## 期待される観察結果

- iOS では取得方式が `webkitCompassHeading`、Android では `deviceorientationabsolute` と表示される。同じアプリでも端末で分岐している、という点を見せる。
- alpha の値と方位の対応を、端末を回しながら確認する。相対 alpha しか出ない端末では、針が北を指さないことがある。
- 横持ちにすると方位がずれる → 画面回転の補正（`screen.orientation.angle` の加算）が要る、という話につなげられる。方位取得は「生値をそのまま使えない」典型例。

## トラブルシュート

- **何も表示されない**：HTTPS で開いているか。HTTP や file:// では動かない。
- **iOS で権限ダイアログが出ない**：タップ以外の場所で `requestPermission()` を呼んでいないか。HTTPS か。`設定 > Safari > モーションと画面の向きのアクセス` が無効になっていないか。
- **針が北を指さない**：地磁気センサーの未キャリブレーション。端末を8の字に振ると改善することが多い。周囲の金属・磁気の影響も受ける。
- **位置精度が悪い**：屋内・建物際では accuracy が数十m以上に劣化する。`accuracy` の値そのものを見せて、GPS の限界を体感させる。
