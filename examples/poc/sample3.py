#!/usr/bin/env python3
# シンプルなloggingモジュールとlogkissハンドラーの組み合わせ例
# 標準のloggingモジュールのロガーにlogkissのカラフルなハンドラーを設定するサンプル

import logging
import sys

# 1. 標準loggingモジュールからロガーを取得
logger_default = logging.getLogger("log_default")


# 2. ロガーのレベルを設定（すべてのメッセージを表示するためDEBUGに）
logger_default.setLevel(logging.DEBUG)
print("\ndefault logger 各ログレベルの出力例：")
logger_default.debug("DEBUGレベルのメッセージ")
logger_default.info("INFOレベルのメッセージ")
logger_default.warning("WARNINGレベルのメッセージ")
logger_default.error("ERRORレベルのメッセージ")

import logkiss


# 3. 既存のハンドラーをクリア（既に設定されている場合に備えて）
logger_color = logkiss.getLogger("log_color")

logger_color.handlers.clear()

# 4. logkissのカラフルなハンドラーを作成
handler = logkiss.KissConsoleHandler()

# 5. ハンドラーにカラーフォーマッターを設定
handler.setFormatter(logkiss.ColoredFormatter())

# 6. ロガーにhandlerを追加
logger_color.addHandler(handler)

# 7. 各レベルのログを出力
print("\ncolored 各ログレベルの出力例：")
logger_color.debug("DEBUGレベルのメッセージ")
logger_color.info("INFOレベルのメッセージ")
logger_color.warning("WARNINGレベルのメッセージ")
logger_color.error("ERRORレベルのメッセージ")
