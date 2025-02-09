#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logkiss as logging

# basicConfigでDEBUGレベルを設定
logging.basicConfig(level=logging.DEBUG)

# ルートロガーを取得
logger = logging.getLogger()

# ログを出力
logger.debug("デバッグメッセージ")
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
logger.critical("重大なエラーメッセージ")
