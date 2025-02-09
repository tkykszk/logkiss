#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logkiss as logging

# ロガーを取得
logger = logging.getLogger()  # ルートロガーを使う

print("3行でたら正解")
# ログを出力
logger.debug("デバッグメッセージ")
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
logger.critical("重大なエラーメッセージ")
