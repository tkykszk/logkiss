#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logkiss as logging

# ロガーの設定
logger = logging.getLogger(__name__)
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

print("1. デフォルトでKissConsoleHandlerを使用:")
logger1 = logging.getLogger("example1")
for handler in logger1.handlers[:]:
    logger1.removeHandler(handler)
logger1.addHandler(logging.KissConsoleHandler())
logger1.propagate = False
logger1.info("カラフルな出力")

print("\n2. loggingモジュールの代替として使用:")
logger2 = logging.getLogger("example2")
for handler in logger2.handlers[:]:
    logger2.removeHandler(handler)
logger2.addHandler(logging.KissConsoleHandler())
logger2.propagate = False
logger2.warning("これもカラフルな出力")

print("\n3. 通常のConsoleHandlerに切り替え:")
import logging as std_logging

logger3 = std_logging.getLogger("example3")
for handler in logger3.handlers[:]:
    logger3.removeHandler(handler)
handler = std_logging.StreamHandler()
handler.setFormatter(std_logging.Formatter(
    fmt='%(asctime)s,%(msecs)03d %(levelname)-5s | %(filename)s:%(lineno)3d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
logger3.addHandler(handler)
logger3.propagate = False
logger3.error("通常の白黒出力")
