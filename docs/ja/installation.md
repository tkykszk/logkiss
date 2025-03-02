# インストール

## 必要条件

- Python 3.8以上

## pipを使ったインストール

最も簡単なインストール方法は、pipを使用することです：

```bash
pip install logkiss
```

クラウドロギング機能（AWS CloudWatchとGoogle Cloud Logging）を使用する場合は、以下のようにインストールします：

```bash
pip install "logkiss[cloud]"
```

## PDMを使ったインストール

PDMを使用している場合は、以下のコマンドでインストールできます：

```bash
pdm add logkiss
```

クラウドロギング機能を使用する場合：

```bash
pdm add "logkiss[cloud]"
```

## Poetryを使ったインストール

Poetryを使用している場合は、以下のコマンドでインストールできます：

```bash
poetry add logkiss
```

クラウドロギング機能を使用する場合：

```bash
poetry add "logkiss[cloud]"
```

## ソースからのインストール

最新の開発バージョンを使用したい場合は、GitHubリポジトリからクローンして直接インストールすることもできます：

```bash
git clone https://github.com/yourusername/logkiss.git
cd logkiss
pip install -e .
```

## 依存関係

- **必須**: PyYAML
- **オプション**: 
  - AWS CloudWatchを使用する場合: boto3
  - Google Cloud Loggingを使用する場合: google-cloud-logging
