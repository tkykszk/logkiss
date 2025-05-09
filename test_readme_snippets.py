#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
READMEに記載されているコードスニペットのテスト
"""

import os
import sys
import logging
import logkiss

print("=== テスト1: 最小限の例（標準logging） ===")
logging.warning("Minimal example for beginners")

print("\n=== テスト2: 最小限の例（logkiss） ===")
import logkiss as logging_alias
logging_alias.warning("Minimal example for beginners")

print("\n=== テスト3: カラフルなコンソールログ ===")
logger = logkiss.getLogger("example1")
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical error message")

print("\n=== テスト4: loggingモジュール代替として使用 ===")
import logkiss as logging_replacement
logger2 = logging_replacement.getLogger("example2")
logger2.debug("Debug message")
logger2.info("Info message")
logger2.warning("Warning message")
logger2.error("Error message")
logger2.critical("Critical error message")

print("\n=== テスト5: カスタムハンドラー設定 ===")
logger3 = logging.getLogger("example3")
logger3.setLevel(logging.DEBUG)
logger3.debug("Debug message (標準logging)")
logger3.info("Info message (標準logging)")
logger3.warning("Warning message (標準logging)")
logger3.error("Error message (標準logging)")
logger3.critical("Critical error message (標準logging)")

# 既存のハンドラーをクリア
logger3.handlers.clear()

# logkissのカスタムハンドラーを追加
handler = logkiss.KissConsoleHandler()
handler.setFormatter(logkiss.ColoredFormatter(use_color=True))
logger3.addHandler(handler)

# カスタマイズされたハンドラーでログを出力
logger3.debug("Debug message (カスタムハンドラー)")
logger3.info("Info message (カスタムハンドラー)")
logger3.warning("Warning message (カスタムハンドラー)")
logger3.error("Customized colorful output")
logger3.critical("Critical message (カスタムハンドラー)")

print("\n=== テスト6: basicConfig関数の確認 ===")
# 既存のハンドラーをクリア
root = logging.getLogger()
for h in root.handlers[:]:
    root.removeHandler(h)

# logkiss.basicConfigを使用
logkiss.basicConfig(level=logkiss.DEBUG, format="%(levelname)s - %(message)s")
logger4 = logkiss.getLogger("example4")
logger4.debug("Debug with basicConfig")
logger4.info("Info with basicConfig")
logger4.warning("Warning with basicConfig")

print("\n=== テスト7: dictConfigの確認 ===")
# 既存のハンドラーをクリア
root = logging.getLogger()
for h in root.handlers[:]:
    root.removeHandler(h)

# logkiss.dictConfigを使用
os.environ["LOGKISS_LEVEL"] = "DEBUG"

# dictConfig用の設定辞書を作成
config = {
    "version": 1,
    "formatters": {
        "colored": {
            "class": "logkiss.ColoredFormatter",
            "format": "%(asctime)s [%(levelname)s] %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logkiss.KissConsoleHandler",
            "level": "DEBUG",
            "formatter": "colored"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG"
        }
    }
}

logkiss.dictConfig(config)
logger5 = logging.getLogger()
logger5.debug("Debug with dictConfig()")
logger5.info("Info with dictConfig()")
logger5.warning("Warning with dictConfig()")

print("\n=== テスト完了 ===")
