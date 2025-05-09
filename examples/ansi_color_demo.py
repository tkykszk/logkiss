#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ANSIエスケープシーケンスを直接使用して、WARNINGレベルを黄色地に黒字で表示するサンプル
"""

import logging
import os
import sys

# ANSIエスケープシーケンスの定義
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # 前景色（文字色）
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # 背景色
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # 明るい色（前景色）
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # 明るい色（背景色）
    BG_BRIGHT_BLACK = "\033[100m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"
    BG_BRIGHT_BLUE = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN = "\033[106m"
    BG_BRIGHT_WHITE = "\033[107m"

# カスタムフォーマッター
class CustomColorFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.formats = {
            logging.DEBUG: Colors.BLUE + "%(asctime)s DEBUG | %(filename)s: %(lineno)d | %(message)s" + Colors.RESET,
            logging.INFO: Colors.WHITE + "%(asctime)s INFO  | %(filename)s: %(lineno)d | %(message)s" + Colors.RESET,
            logging.WARNING: Colors.BLACK + Colors.BG_YELLOW + "%(asctime)s WARN  | %(filename)s: %(lineno)d | %(message)s" + Colors.RESET,
            logging.ERROR: Colors.BLACK + Colors.BG_RED + "%(asctime)s ERROR | %(filename)s: %(lineno)d | %(message)s" + Colors.RESET,
            logging.CRITICAL: Colors.BLACK + Colors.BG_BRIGHT_RED + Colors.BOLD + "%(asctime)s CRITI | %(filename)s: %(lineno)d | %(message)s" + Colors.RESET,
        }
    
    def format(self, record):
        log_format = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S,%f"[:-3])
        return formatter.format(record)

def main():
    """各ログレベルの色を表示するメイン関数"""
    # ロガーの初期化
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # 既存のハンドラーをクリア
    logger.handlers = []
    
    # カスタムフォーマッターを使用したハンドラーを追加
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(CustomColorFormatter())
    logger.addHandler(handler)
    
    # 各ログレベルでメッセージを出力
    logger.debug("これはDEBUGレベルのメッセージです (青色)")
    logger.info("これはINFOレベルのメッセージです (白色)")
    logger.warning("これはWARNINGレベルのメッセージです (黄色地に黒字)")
    logger.error("これはERRORレベルのメッセージです (赤地に黒字)")
    logger.critical("これはCRITICALレベルのメッセージです (明るい赤地に黒字、太字)")

if __name__ == "__main__":
    main()
