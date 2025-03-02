# logkiss サンプルコード集

このディレクトリには、Python logging モジュールと logkiss を組み合わせて使用する方法を示すサンプルコードが含まれています。

## サンプル一覧

### console_handler_example.py

標準の Python logging モジュールと logkiss を組み合わせて、コンソールにログを出力する方法を示すサンプルです。

**主な機能**:
- `logkiss.logkiss.KissConsoleHandler` を使用して、色付きコンソールハンドラーを設定
- 通常のログメッセージの出力
- 構造化ログの出力
- ネストされた構造化ログの出力
- ルートロガーの使用例

**実行方法**:
```bash
python examples/console_handler_example.py
```

### existing_logger_example.py

既存のロギング設定に logkiss を追加する方法を示すサンプルです。

**主な機能**:
- デフォルトのロガー設定（basicConfig）を使用
- 既存のロガーに logkiss の KissConsoleHandler を追加
- ルートロガーと個別のロガーの両方での使用例
- 構造化ログの出力
- 元のロガー設定に戻す方法

**実行方法**:
```bash
python examples/existing_logger_example.py
```

### sample_aws.py

AWS CloudWatch Logs にログを送信する方法を示すサンプルです。

**主な機能**:
- AWS CloudWatch Logs へのログ送信
- ロググループ、ストリーム、エントリの作成
- ログの送信と表示

**実行方法**:
```bash
python examples/sample_aws.py
```

### sample_gcp.py

Google Cloud Logging にログを送信する方法を示すサンプルです。

**主な機能**:
- Google Cloud Logging へのログ送信
- ログの作成と表示

**実行方法**:
```bash
python examples/sample_gcp.py
```

## 使用例

### 基本的な使用方法

```python
import logging
from logkiss.logkiss import KissConsoleHandler

# ロガーを取得
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

# KissConsoleHandler を追加
handler = KissConsoleHandler()
logger.addHandler(handler)

# ログを出力
logger.debug("デバッグメッセージ")
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
logger.critical("重大なエラーメッセージ")
```

### 既存のロガーに追加する方法

```python
import logging
from logkiss.logkiss import KissConsoleHandler

# 既存のロガーのハンドラーを一時的に保存
logger = logging.getLogger("my_app")
existing_handlers = logger.handlers[:]

# 既存のハンドラーを削除（重複出力を避けるため）
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# KissConsoleHandler を追加
kiss_handler = KissConsoleHandler()
logger.addHandler(kiss_handler)

# ログを出力
logger.info("色付きログメッセージ")

# 元のハンドラーを復元
for handler in logger.handlers[:]:
    logger.removeHandler(handler)
for handler in existing_handlers:
    logger.addHandler(handler)
```

## クリーンアップ機能

AWS CloudWatch Logs と Google Cloud Logging のサンプルには、クリーンアップ機能が含まれています。この機能は、テストリソース（ロググループ、ストリーム、エントリ）を削除するために使用されます。クリーンアップ機能は、デフォルトで有効になっています。クリーンアップ機能を無効にするには、`CLEAN_UP` グローバル変数を `False` に設定してください。

## 注意点

- `KissConsoleHandler` は、ログレベルに応じて自動的に色付けされます
- フォーマットは自動的に `%(asctime)s,%(msecs)03d %(levelname)-5s | %(filename)s:%(lineno)3d | %(message)s` に設定されます
- 日付フォーマットは自動的に `%Y-%m-%d %H:%M:%S` に設定されます
- **色付きログ出力**: logkiss の KissConsoleHandler は、ログレベルに応じて自動的に色付けされます

詳細な使用方法については、[logkiss のドキュメント](../README.md) を参照してください。
