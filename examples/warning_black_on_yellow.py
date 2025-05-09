#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WARNINGレベルを黄色地に黒字で表示するサンプルコード
"""

import logging
import os
from logkiss.logkiss import setup

def main():
    """WARNINGレベルを黄色地に黒字で表示するデモ"""
    # ロガーの初期化をリセット
    logging.root.handlers = []
    
    # 設定ファイルを指定してlogkissをセットアップ
    config_path = os.path.join(os.path.dirname(__file__), "custom_color_config.yaml")
    logger = setup(config_path)
    
    # すべてのログレベルを表示するために、DEBUGレベルに設定
    logger.setLevel(logging.DEBUG)
    
    # 各ログレベルでメッセージを出力
    logger.debug("これはDEBUGレベルのメッセージです (青色)")
    logger.info("これはINFOレベルのメッセージです (白色)")
    logger.warning("これはWARNINGレベルのメッセージです (黄色地に黒字)")
    logger.error("これはERRORレベルのメッセージです (赤地に黒字)")
    logger.critical("これはCRITICALレベルのメッセージです (明るい赤地に黒字、太字)")

if __name__ == "__main__":
    main()
