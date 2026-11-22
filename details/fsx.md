## しくみ

よく使われる 4 種類のファイルシステムを、フルマネージドで提供するサービス群です。

| 種類 | 特徴 | 試験でこう出たら |
|---|---|---|
| FSx for Windows File Server | **SMB**、Windows の **Active Directory** と連携、DFS | 「Windows のファイル共有」「AD のユーザーでアクセス制御」 |
| FSx for Lustre | 高速な並列ファイルシステム。[[s3]] と連携できる | 「HPC」「機械学習の学習データ」「ミリ秒以下のレイテンシー」 |
| FSx for NetApp ONTAP | NFS・SMB・iSCSI に対応。スナップショットや重複排除 | 「オンプレミスの NetApp を移行」「複数のプロトコル」 |
| FSx for OpenZFS | ZFS 互換。NFS | 「オンプレミスの ZFS を移行」 |

- Windows File Server と ONTAP には**マルチ AZ**構成がある

## 試験でのポイント

- Windows ＋共有ファイル → **FSx for Windows File Server**（[[efs]] は Linux 向け）
- HPC・大規模な並列処理で、S3 のデータを高速に処理 → **FSx for Lustre**

## よくあるひっかけ

- Lustre の「スクラッチ」タイプは一時的な処理用で、データは複製されない。長期保存なら「永続」タイプ
- オンプレミスの Windows ファイルサーバーから AWS のストレージを使い続けたいだけなら、[[storage-gateway]]（FSx File Gateway）も候補
