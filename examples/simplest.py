#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logkiss as logging
#import logging

# 無設定の場合は、logging.level は logging.WARNINGが採用されるようにしてください


print("3行でたら正解")
# ログを出力
logging.debug("デバッグメッセージ")  ##表示されないのが正解
logging.info("情報メッセージ")    ## 表示されないのが正解
logging.warning("警告メッセージ") ## 表示されるのが正解
logging.error("エラーメッセージ")
logging.critical("重大なエラーメッセージ")
