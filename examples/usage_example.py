#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logkiss as logging

# ロガーの設定
logger = logging.getLogger(__name__)

print("1. デフォルトでKissConsoleHandlerを使用:")
logger1 = logging.getLogger("example1")
logger1.info("カラフルな出力")

print("\n2. loggingモジュールの代替として使用:")
logger2 = logging.getLogger("example2")
logger2.warning("これもカラフルな出力")

print("\n3. 通常のConsoleHandlerに切り替え:")
import logging

logger3 = logging.getLogger("example3")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    fmt='%(asctime)s,%(msecs)03d %(levelname)-5s | %(filename)s:%(lineno)3d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
logger3.addHandler(handler)
logger3.error("通常の白黒出力")
