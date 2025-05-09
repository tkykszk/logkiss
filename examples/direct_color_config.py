#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WARNINGレベルを黄色地に黒字で表示するサンプルコード（直接設定版）
"""

import logging
import logkiss
from logkiss.logkiss import ColorManager, ColoredFormatter, KissConsoleHandler

def main():
    """WARNINGレベルを黄色地に黒字で表示するデモ（直接設定）"""
    # ロガーの初期化をリセット
    logging.root.handlers = []
    
    # カスタムカラーマネージャーを作成
    color_manager = ColorManager()
    
    # WARNINGレベルの色を明示的に上書き
    color_manager.config["levels"]["WARNING"] = {"fg": "black", "bg": "yellow"}
    color_manager.config["elements"]["message"]["WARNING"] = {"fg": "black", "bg": "yellow"}
    
    # カスタムフォーマッターを作成
    formatter = ColoredFormatter(use_color=True)
    formatter.color_manager = color_manager
    
    # ハンドラーを作成して設定
    handler = KissConsoleHandler()
    handler.setFormatter(formatter)
    
    # ロガーを設定
    logger = logging.getLogger()
    logger.handlers = []  # 既存のハンドラーをクリア
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    # 各ログレベルでメッセージを出力
    logger.debug("これはDEBUGレベルのメッセージです (青色)")
    logger.info("これはINFOレベルのメッセージです (白色)")
    logger.warning("これはWARNINGレベルのメッセージです (黄色地に黒字)")
    logger.error("これはERRORレベルのメッセージです (赤地に黒字)")
    logger.critical("これはCRITICALレベルのメッセージです (明るい赤地に黒字、太字)")

if __name__ == "__main__":
    main()
