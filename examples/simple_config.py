#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logkiss as logging

# ルートロガーを取得
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  

print("5行でたら正解")
# ログを出力
logger.debug("デバッグメッセージ")
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
logger.critical("重大なエラーメッセージ")
