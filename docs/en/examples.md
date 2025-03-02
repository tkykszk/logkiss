# サンプル

## 基本的なロギング

基本的なロギングの例です。

```python
import logkiss as logging

# ロガーの取得
logger = logging.getLogger(__name__)

# ログの出力
logger.warning('これは警告メッセージです')
logger.info('これは情報メッセージです')
logger.error('これはエラーメッセージです')
```

## 既存のロガーの拡張

既存のロガーをlogkissで拡張する例です。

```python
import logging as standard_logging
import logkiss as logging

# 標準ロガーの設定
standard_logger = standard_logging.getLogger("standard")
standard_logger.setLevel(standard_logging.INFO)

# logkissのKissConsoleHandlerを追加
console_handler = logging.KissConsoleHandler()
standard_logger.addHandler(console_handler)

# ログの出力
standard_logger.info("標準ロガーからの情報メッセージ（色付き）")
standard_logger.warning("標準ロガーからの警告メッセージ（色付き）")
```

## 色の無効化

色を無効化する例です。

```python
import logkiss as logging

# ロガーの取得
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
logger.info("色なしの情報メッセージ")
logger.warning("色なしの警告メッセージ")
logger.error("色なしのエラーメッセージ")
```

## AWS CloudWatchの例

AWS CloudWatchにログを送信する例です。

```python
import os
import time
import hashlib
import logkiss as logging
from logkiss.handlers import AWSCloudWatchHandler

# 環境変数からAWS設定を取得
AWS_PROFILE = os.environ.get("AWS_PROFILE")
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

# クリーンアップフラグ（テスト後にリソースを削除するかどうか）
CLEAN_UP = True

# 一意のロググループ名を生成
timestamp = int(time.time())
unique_hash = hashlib.md5(f"{timestamp}".encode()).hexdigest()[:8]
log_group_name = f"logkiss-sample-{timestamp}-{unique_hash}"
log_stream_name = "sample-stream"

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# コンソールハンドラーを追加
console_handler = logging.KissConsoleHandler()
logger.addHandler(console_handler)

# AWS CloudWatchハンドラーを追加
aws_handler = AWSCloudWatchHandler(
    log_group_name=log_group_name,
    log_stream_name=log_stream_name,
    region_name=AWS_REGION,
    profile_name=AWS_PROFILE
)
logger.addHandler(aws_handler)

# ログの出力
logger.info(f"AWS CloudWatchにログを送信しています（グループ: {log_group_name}）")
logger.warning("これは警告メッセージです")
logger.error("これはエラーメッセージです")

# クリーンアップ
if CLEAN_UP:
    logger.info("リソースをクリーンアップしています...")
    aws_handler.cleanup()
    logger.info("クリーンアップ完了")
```

## Google Cloud Loggingの例

Google Cloud Loggingにログを送信する例です。

```python
import os
import time
import hashlib
import logkiss as logging
from logkiss.handlers import GCPCloudLoggingHandler

# 環境変数からGCP設定を取得
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

# クリーンアップフラグ（テスト後にリソースを削除するかどうか）
CLEAN_UP = True

# 一意のログ名を生成
timestamp = int(time.time())
unique_hash = hashlib.md5(f"{timestamp}".encode()).hexdigest()[:8]
log_name = f"logkiss-sample-{timestamp}-{unique_hash}"

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# コンソールハンドラーを追加
console_handler = logging.KissConsoleHandler()
logger.addHandler(console_handler)

# GCP Cloud Loggingハンドラーを追加
gcp_handler = GCPCloudLoggingHandler(
    project_id=GCP_PROJECT_ID,
    log_name=log_name
)
logger.addHandler(gcp_handler)

# ログの出力
logger.info(f"Google Cloud Loggingにログを送信しています（ログ名: {log_name}）")
logger.warning("これは警告メッセージです")
logger.error("これはエラーメッセージです")

# クリーンアップ
if CLEAN_UP:
    logger.info("リソースをクリーンアップしています...")
    gcp_handler.cleanup()
    logger.info("クリーンアップ完了")
```
