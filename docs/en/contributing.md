# 貢献ガイド

logkissプロジェクトへの貢献に興味をお持ちいただき、ありがとうございます！このガイドでは、プロジェクトに貢献するための方法を説明します。

## 開発環境のセットアップ

1. リポジトリをクローンします：

```bash
git clone https://github.com/yourusername/logkiss.git
cd logkiss
```

2. 開発環境をセットアップします：

```bash
# PDMを使用する場合
pdm install -d

# Poetryを使用する場合
poetry install
```

## テストの実行

変更を加える前に、既存のテストが通ることを確認してください：

```bash
# PDMを使用する場合
pdm run pytest

# Poetryを使用する場合
poetry run pytest
```

## コーディング規約

このプロジェクトでは、以下のツールを使用してコードの品質を維持しています：

- **Black**: コードフォーマッター
- **isort**: インポート文の整理
- **mypy**: 型チェック
- **flake8**: コードリンター

変更を提出する前に、これらのツールを実行してください：

```bash
# PDMを使用する場合
pdm run black .
pdm run isort .
pdm run mypy logkiss
pdm run flake8 logkiss

# Poetryを使用する場合
poetry run black .
poetry run isort .
poetry run mypy logkiss
poetry run flake8 logkiss
```

## プルリクエストの提出

1. 新しいブランチを作成します：

```bash
git checkout -b feature/your-feature-name
```

2. 変更を加え、コミットします：

**Note: Commit messages must be written in English.**

```bash
git add .
git commit -m "Add your feature description"
```

3. GitHubにプッシュします：

```bash
git push origin feature/your-feature-name
```

4. GitHubでプルリクエストを作成します。

## ドキュメントの更新

機能を追加または変更した場合は、対応するドキュメントも更新してください：

```bash
# ドキュメントをローカルでプレビュー
pdm run docs-serve

# ドキュメントをビルド
pdm run docs-build
```

## リリースプロセス

リリースプロセスは以下の通りです：

1. バージョン番号を更新します（`pyproject.toml`）
2. CHANGELOGを更新します
3. タグを作成してプッシュします：

```bash
git tag v1.0.0
git push origin v1.0.0
```

4. GitHubのリリースページで新しいリリースを作成します。

## 質問やサポート

質問やサポートが必要な場合は、GitHubのIssueを作成してください。
