## しくみ

ソースコードの変更から、ビルド・テスト・デプロイまでを自動でつなぐ **CI/CD のパイプライン**を作るサービスです。

- **ステージ**（Source → Build → Test → Deploy など）と、その中の**アクション**で構成する
- Source：GitHub、Bitbucket、[[s3]]、[[ecr]] など
- Build / Test：[[codebuild]]、Jenkins など
- Deploy：[[codedeploy]]、[[ecs]]、[[elastic-beanstalk]]、[[cloudformation]]、S3 など
- **手動承認**のアクションを挟んで、本番へのデプロイ前に人が確認できる

## 試験でのポイント

- 「コードの変更をきっかけに、ビルドからデプロイまでを自動化」「リリースの流れを管理」→ CodePipeline
- 「本番に出す前に承認を入れたい」→ 手動承認アクション

## よくあるひっかけ

- CodePipeline は流れをつなぐだけで、ビルド自体は CodeBuild、デプロイ自体は CodeDeploy などが行う
