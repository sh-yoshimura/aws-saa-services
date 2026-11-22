# AWS サービス図鑑（SAA-C03 対策）

AWS 主要サービスのアイコン・正式名称・基本機能・試験キーワードの一覧。
カテゴリごとに、サービスの比較表と使い分けのポイントも載せている。

- 公開サイト（スマホ可）: https://sh-yoshimura.github.io/aws-saa-services/
- Claude の公開ページ: https://claude.ai/artifact/243uLzu97V23xpX6JZjDqP （自分だけが見られる設定）
- ローカル: `index.html` をブラウザで開く

## ファイル

| ファイル | 役割 |
|---|---|
| `services.yaml` | **データ本体。追加・修正はここだけ** |
| `template.html` | 見た目（CSS・検索などの動き） |
| `build.py` | YAML とテンプレートから `index.html` を作る |
| `icons/` | アイコン（初回の生成時に diagrams ライブラリから自動でコピーされる） |
| `index.html` | 生成物。直接編集しない（git には入れない） |
| `.github/workflows/pages.yml` | main に push すると、ページを作り直して GitHub Pages に公開する |

## サービスを追加する

1. `services.yaml` の `services:` に追記する

   ```yaml
   - id: appsync
     name: AWS AppSync
     category: integration
     icon: integration/appsync
     summary: GraphQL API をマネージドで作成・公開する。
     use_when: 複数のデータソースをまとめた GraphQL API を作りたいとき
     attrs: {"配信のしかた": "GraphQL（購読でリアルタイム配信）", "特徴": "複数のデータソースを 1 つの API に"}
     keywords: [GraphQL, リアルタイム更新]
     compare: REST API なら API Gateway。
     tags: [要復習]
   ```

2. 作り直す

   ```bash
   uv run --with pyyaml --with diagrams python build.py
   ```

- 使えるアイコン名の一覧: `uv run --with pyyaml --with diagrams python build.py --list-icons`
- 自前のアイコンを使うなら `icons/<分類>/<名前>.png` に置き、`icon: <分類>/<名前>` と書く
- `use_when`（どういうときに使うか）と `attrs`（比較表の列の値）を書くと、そのカテゴリの比較表に自動で行が増える。
  `attrs` の列名は、そのカテゴリの `columns` と同じにする（違うと build.py がエラーで教えてくれる）
- カテゴリを増やすなら `categories:` に `label`・`columns`・`points` を足す
- 比較表の列を増やすなら、カテゴリの `columns` に列名を足し、各サービスの `attrs` に値を書く（未記入は「—」になる）
- 使い分けのポイントは、カテゴリの `points` に 1 行ずつ足す
- `tags` は自由に付けられ、検索の対象になる（`要復習` で絞り込むなど）

## 公開サイトへの反映

`main` ブランチに push すると、GitHub Actions が `build.py` を実行して GitHub Pages に公開する（1〜2 分）。
スマホからは、GitHub 上で `services.yaml` を直接編集してコミットするだけで反映される。
新しいアイコンを使うときは、手元で一度 build.py を実行して `icons/` に追加されたファイルもコミットする
（Actions では diagrams ライブラリを入れていないため）。
