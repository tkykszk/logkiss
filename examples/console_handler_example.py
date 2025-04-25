#!/usr/bin/env python
"""
既存の logging を利用している状況で、追加的に logkiss の KissConsoleHandler を使用するサンプル

このサンプルでは、標準の logging モジュールと logkiss を組み合わせて
コンソールにログを出力する方法を示します。

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
"""

import logging
import logkiss
from logkiss.logkiss import KissConsoleHandler

# ロガーを取得
logger = logging.getLogger("console_example")
logger.setLevel(logging.DEBUG)

# 既存のハンドラーをクリア（重複出力を避けるため）
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# logkiss の KissConsoleHandler を使用
kiss_handler = KissConsoleHandler()
logger.addHandler(kiss_handler)

# ログ出力
logger.debug("これはデバッグメッセージです")
logger.info("これは情報メッセージです")
logger.warning("これは警告メッセージです")
logger.error("これはエラーメッセージです")
logger.critical("これは重大なエラーメッセージです")

# 構造化ログの出力
logger.info("構造化ログの例", extra={"user_id": 12345, "action": "login", "status": "success", "ip_address": "192.168.1.1"})

# ネストされた構造化ログの出力
logger.warning(
    "複雑な構造化ログの例",
    extra={
        "request": {"method": "POST", "path": "/api/users", "headers": {"content-type": "application/json", "user-agent": "Mozilla/5.0"}},
        "response": {"status_code": 400, "body": {"error": "Invalid input", "details": ["Username is required", "Email is invalid"]}},
    },
)

print("\n--- ルートロガーを使用する例 ---")

# ルートロガーを取得して設定
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# すべてのハンドラーをクリア
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# すべてのハンドラーをクリア（重複出力を避けるため）
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# logkiss の KissConsoleHandler を使用
root_kiss_handler = KissConsoleHandler()
root_logger.addHandler(root_kiss_handler)

# ログ出力
logging.info("ルートロガーからの情報メッセージ")
logging.warning("ルートロガーからの警告メッセージ")
logging.error("ルートロガーからのエラーメッセージ")
