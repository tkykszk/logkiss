#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logkiss as logging

# ロガーを取得
logger = logging.getLogger()  # ルートロガーを使う

# ログを出力
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
logger.critical("重大なエラーメッセージ")
