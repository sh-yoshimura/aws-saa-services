## しくみ

EC2 やオンプレミスのサーバー（**マネージドノード**）を、まとめて運用管理するためのサービス群です。各サーバーに入れた **SSM エージェント**が Systems Manager と通信して動きます。

## 主な機能

| 機能 | 何をするか |
|---|---|
| **Session Manager** | ブラウザや CLI から、**SSH のポートを開けずに**、踏み台なしでサーバーにログインする。操作ログを S3 や CloudWatch Logs に残せる |
| **Run Command** | 多数のサーバーで、コマンドやスクリプトを**今すぐ一斉に**実行する |
| **Patch Manager** | OS やソフトウェアの**パッチ適用**を自動化する（パッチベースライン、メンテナンスウィンドウ） |
| **State Manager** | サーバーの設定を、**決めた状態に保ち続ける** |
| **Automation** | AWS リソースへの複数ステップの操作を自動化する（ランブック）。[[config]] の修復アクションにも使う |
| **Parameter Store** | 設定値や秘密情報を階層的に保存する。標準パラメータは無料 |
| **Inventory** | サーバーに入っているソフトウェアなどの一覧を集める |
| **OpsCenter** | 運用上の問題（OpsItem）をまとめて管理する |

## 使うための準備（頻出）

1. **SSM エージェント**（Amazon Linux や Windows の公式 AMI には入っている）
2. EC2 に Systems Manager を使う権限の **IAM ロール**（例：`AmazonSSMManagedInstanceCore`）
3. Systems Manager への通信経路。プライベートサブネットなら [[nat-gateway]] か [[vpc-endpoint]]（インターフェイス型）

## 試験でのポイント

- 「SSH のポートを開けずに」「踏み台サーバーをなくしたい」「操作ログを残したい」→ **Session Manager**
- 「数百台のサーバーにパッチを自動で適用」→ **Patch Manager**
- 「多数のインスタンスで一斉にスクリプトを実行」→ **Run Command**
- 「設定値を安全に保存（ローテーション不要）」→ **Parameter Store**

## よくあるひっかけ

- 「サーバーが Systems Manager に表示されない」→ エージェント・IAM ロール・通信経路のどれかが足りない
- パスワードの**自動ローテーション**が必要なら、Parameter Store ではなく [[secrets-manager]]
- EC2 のユーザーデータは起動時に 1 回だけ。起動後にコマンドを実行するなら Run Command
