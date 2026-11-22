## しくみ

オンプレミスや他のクラウドのサーバーを、**作り直さずにそのまま** [[ec2]] へ移す（**リホスト／リフト＆シフト**）ためのサービスです。

1. 移行元のサーバーに**レプリケーションエージェント**を入れる
2. ディスクの内容が、ブロック単位で AWS へ**継続的に複製**される
3. AWS 上でテスト用のインスタンスを起動して、動作を確認する
4. 切り替え（カットオーバー）のときだけ短時間止めて、EC2 に移る

- 物理サーバー、VMware、Hyper-V、他のクラウドの仮想マシンに対応
- 旧 CloudEndure Migration、Server Migration Service（SMS）の後継

## 試験でのポイント

- 「多数のサーバーを、アプリを変更せずに AWS へ移行」「リフト＆シフト」「停止時間を最小に」→ Application Migration Service
- 移行の計画には、オンプレミスのサーバーの情報を集める Application Discovery Service や Migration Hub も使う

## よくあるひっかけ

- データベースだけを移すなら [[dms]]、ファイルだけを移すなら [[datasync]]
- 災害対策として、オンプレミスのサーバーを AWS に複製しておくなら AWS Elastic Disaster Recovery（同じ仕組みの別サービス）
