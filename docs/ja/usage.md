# 使い方

## 基本的な使い方

logkissは標準のPythonロギングモジュールと互換性があり、同様の方法で使用できます。

```python
import logkiss as logging

# ロガーの取得
logger = logging.getLogger(__name__)

# ログレベルの設定
logger.setLevel(logging.DEBUG)

# ログの出力
logger.debug("デバッグメッセージ")
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
logger.critical("致命的エラーメッセージ")
```

## KissConsoleHandlerの使用

logkissの主な特徴は、カラフルなコンソール出力を提供する`KissConsoleHandler`です。

```python
import logkiss as logging

# ロガーの取得
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 既存のハンドラーをクリア
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# KissConsoleHandlerを追加
console_handler = logging.KissConsoleHandler()
logger.addHandler(console_handler)

# ログの出力
logger.debug("デバッグメッセージ")
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
logger.critical("致命的エラーメッセージ")
```

## 色の無効化

特定の環境では、色付きの出力が不要な場合があります。その場合は、以下のようにして色を無効化できます：

```python
import logkiss as logging

# ロガーの取得
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 既存のハンドラーをクリア
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# 色を無効化したフォーマッターを作成
formatter = logging.ColoredFormatter(use_color=False)

# KissConsoleHandlerを追加し、フォーマッターを設定
console_handler = logging.KissConsoleHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# ログの出力
logger.debug("色なしのデバッグメッセージ")
logger.info("色なしの情報メッセージ")
logger.warning("色なしの警告メッセージ")
logger.error("色なしのエラーメッセージ")
```

## ファイルへのログ出力

ファイルにログを出力する場合は、標準の`FileHandler`と`ColoredFormatter`を使用します：

```python
import logging
from logkiss import ColoredFormatter

# ロガーを作成
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

# FileHandlerとColoredFormatterを追加
file_handler = logging.FileHandler("app.log")
formatter = ColoredFormatter(use_color=False)  # ファイル出力用に色を無効化
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ログメッセージを出力
logger.debug("デバッグメッセージ")
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
logger.critical("重大メッセージ")
```

## AWS CloudWatchへのログ出力

AWS CloudWatchにログを送信する場合は、`AWSCloudWatchHandler`を使用します：

```python
import logkiss as logging
from logkiss.handlers import AWSCloudWatchHandler

# ロガーの取得
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# AWSCloudWatchHandlerを追加
aws_handler = AWSCloudWatchHandler(
    log_group_name="my-log-group",
    log_stream_name="my-log-stream",
    region_name="ap-northeast-1"
)
logger.addHandler(aws_handler)

# ログの出力
logger.info("AWS CloudWatchに送信される情報メッセージ")
```

## Google Cloud Loggingへのログ出力

Google Cloud Loggingにログを送信する場合は、`GCPCloudLoggingHandler`を使用します：

```python
import logkiss as logging
from logkiss.handlers import GCPCloudLoggingHandler

# ロガーの取得
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# GCPCloudLoggingHandlerを追加
gcp_handler = GCPCloudLoggingHandler(
    project_id="my-gcp-project",
    log_name="my-log"
)
logger.addHandler(gcp_handler)

# ログの出力
logger.info("Google Cloud Loggingに送信される情報メッセージ")
```
