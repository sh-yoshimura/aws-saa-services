## しくみ

**DDoS 攻撃**（大量の通信を送りつけてサービスを止める攻撃）からアプリを守るサービスです。

| プラン | 料金 | 内容 |
|---|---|---|
| **Shield Standard** | **無料**（全利用者に自動で適用） | よくある L3/L4 の攻撃（SYN フラッド、UDP リフレクションなど）を防ぐ |
| **Shield Advanced** | 有料（月額＋データ転送） | より大規模・高度な攻撃への対策、L7 の攻撃の検知、**DDoS 対応チーム（SRT）**の 24 時間支援、攻撃で増えた料金の補償（コスト保護）、[[waf]] の利用料込み |

Advanced で守れるリソース：[[cloudfront]]、[[route53]]、[[global-accelerator]]、[[elb]]、Elastic IP（EC2）

## 試験でのポイント

- 「DDoS 攻撃からの保護」→ Shield
- 「DDoS の専門チームの支援」「攻撃によるスケールアウトの料金を補償」→ **Shield Advanced**
- DDoS に強い構成：CloudFront や Route 53 を前に置き、[[ec2-auto-scaling]] で吸収、WAF のレートベースルール

## よくあるひっかけ

- Standard は何もしなくても有効。「Shield Standard を有効化する」手順は不要
