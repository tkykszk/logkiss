# logkiss サンプル集

このディレクトリには、様々なロギングシナリオで `logkiss` ライブラリを使用する方法の例が含まれています。

## 基本的なサンプル

- **simple_example.py**: `KissConsoleHandler` を使った `logkiss` の基本的な使い方を示します。
- **existing_logger_example.py**: 既存のロガーに `logkiss` を統合する方法を示します。
- **structured_logging_example.py**: `logkiss` を使った構造化ロギングを示します。

## クラウドロギングのサンプル

- **sample_aws.py**: `logkiss` を使って AWS CloudWatch Logs にログを送信する方法を示します。
- **sample_gcp.py**: `logkiss` を使って Google Cloud Logging にログを送信する方法を示します。

## サンプルの実行方法

サンプルを実行するには、適切なエクストラで `logkiss` をインストールしていることを確認してください：

```bash
# 基本的なサンプル用
pip install logkiss

# クラウドロギングのサンプル用
pip install 'logkiss[cloud]'
```

その後、サンプルを実行できます：

```bash
python simple_example.py
python existing_logger_example.py
python structured_logging_example.py
```

## クラウドロギングのセットアップ

### AWS CloudWatch Logs

AWS CloudWatch Logs のサンプルを実行するには：

1. AWS 認証情報を設定します（AWS CLI または環境変数を使用）
2. 以下の環境変数を設定します：
   - `AWS_PROFILE`: AWS プロファイル名（オプション）
   - `AWS_DEFAULT_REGION`: AWS リージョン（デフォルト: ap-northeast-1）

その後、実行します：

```bash
python sample_aws.py
```

### Google Cloud Logging

Google Cloud Logging のサンプルを実行するには：

1. GCP 認証情報を設定します（`gcloud auth application-default login` を使用）
2. 以下の環境変数を設定します：
   - `GCP_PROJECT_ID`: Google Cloud プロジェクト ID

その後、実行します：

```bash
python sample_gcp.py
```

## クリーンアップ

両方のクラウドロギングサンプルには、`CLEAN_UP` グローバル変数で制御されるクリーンアップ機能が含まれています。`True`（デフォルト）に設定すると、サンプルは実行後にテストリソース（ロググループ、ストリーム、エントリ）を削除します。検査のためにログを保持したい場合は、`False` に設定してください。

## 示されている機能

- `KissConsoleHandler` による色分けされたログ出力
- 追加フィールドを持つ構造化ロギング
- 既存のロガーとの統合
- AWS CloudWatch Logs へのログ送信
- Google Cloud Logging へのログ送信
- テストリソースのクリーンアップ

## 注意点

- クラウドロギングのサンプルは、衝突を避けるためにタイムスタンプとハッシュを使用して一意のログ名を生成します。
- クリーンアップ機能は、サンプルによって作成されたテストリソースのみを削除するように設計されており、既存のログは削除しません。
