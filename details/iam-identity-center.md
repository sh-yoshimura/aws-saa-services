## しくみ

複数の AWS アカウントや業務アプリへの**シングルサインオン（SSO）**を、1 か所で管理します（旧 AWS Single Sign-On）。社員は 1 つの ID でポータルにログインし、許可されたアカウントとロールを選んで使います。

- **ID ソース**：Identity Center 自体のディレクトリ、Active Directory（AWS Directory Service など）、外部の ID プロバイダー（Microsoft Entra ID、Okta など）
- **アクセス許可セット**：「このグループは、このアカウントで、この権限」を決める。各アカウントに IAM ロールが自動で作られる
- [[organizations]] と連携して、組織内のアカウントをまとめて扱う

## 試験でのポイント

- 「複数のアカウントへのアクセスを一元管理」「社員が 1 つの ID でログイン」「既存の社内 ID（AD・Entra ID）を使いたい」→ IAM Identity Center
- アカウントごとに IAM ユーザーを作る選択肢は、運用負荷が高く誤りになりやすい

## よくあるひっかけ

- Web・モバイルアプリの**利用者**のログインは [[cognito]]。Identity Center は**社員（AWS を使う人）**向け
