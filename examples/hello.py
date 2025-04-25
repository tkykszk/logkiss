"""Hello world example for logkiss.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# logkissをインポートして  as logging として試用 デフォルトの動作の違いを確認できるようにします

import os
import sys
import logging

print("1. 標準のloggingモジュールの動作:")

logging.basicConfig()
# 標準のloggingの設定
default_logger = logging.getLogger()

# 標準のloggingでログ出力
print("\nログ出力テスト:")
default_logger.debug("デバッグメッセージ")
default_logger.info("情報メッセージ")
default_logger.warning("警告メッセージ")
default_logger.error("エラーメッセージ")
default_logger.critical("重大なエラーメッセージ")

print("\n2. logkissモジュールの動作:")
import logkiss as logging

# logkissロガーの取得（デフォルト設定を使用）
kiss_logger = logging.getLogger("logkiss")
kiss_logger.setLevel(logging.DEBUG)

# 標準のルートロガーへの伝播を無効化
kiss_logger.propagate = False

# ハンドラーの状態を確認
print("\nロガーの状態:")
print(f"ロガー名: {kiss_logger.name}")
print("ハンドラー一覧:")
for i, handler in enumerate(kiss_logger.handlers):
    print(f"  {i+1}. {type(handler).__name__}")

# logkissでログ出力
kiss_logger.debug("デバッグメッセージ")
kiss_logger.info("情報メッセージ")
kiss_logger.warning("警告メッセージ")
kiss_logger.error("エラーメッセージ")
kiss_logger.critical("重大なエラーメッセージ")

print("\n3. logkissの拡張機能:")


# ファイル名フィルターの使用
class FilenameFilter(logging.Filter):
    def __init__(self, filename):
        self.filename = filename

    def filter(self, record):
        record.filename = self.filename
        return True


# 異なるファイル名でログ出力
kiss_logger = logging.getLogger("logkiss")
kiss_logger.propagate = False
kiss_logger.addFilter(FilenameFilter("custom.py"))
kiss_logger.info("カスタムファイル名でのログ出力")

# ファイル名フィルターを削除
kiss_logger.removeFilter(kiss_logger.filters[0])

# 通常のConsoleHandlerを使用
print("\n4. 通常のConsoleHandlerを使用:")
logging.use_console_handler(kiss_logger)
kiss_logger.info("通常のConsoleHandlerでログ出力")
