## しくみ

**全文検索**や**ログ分析**のための OpenSearch（Elasticsearch から派生したオープンソース）を、マネージドで提供します。可視化ツールの **OpenSearch Dashboards** も使えます。

- **ドメイン**（クラスター）を作って使う。マルチ AZ 構成で高可用性にできる
- **OpenSearch Serverless**：容量の管理が不要
- データの取り込み：[[data-firehose]]、[[cloudwatch]] Logs、OpenSearch Ingestion など
- ベクトル検索にも対応（生成 AI の検索拡張に使われる）

## 試験でのポイント

- 「全文検索」「サイト内検索」「ログをほぼリアルタイムに検索・可視化」→ OpenSearch Service
- 「DynamoDB のデータを全文検索したい」→ DynamoDB と OpenSearch を連携する

## よくあるひっかけ

- 決まった集計・分析なら [[redshift]] や [[athena]]。OpenSearch は「検索」が得意
