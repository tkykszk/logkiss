#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
logkissの各ログレベルの色を表示するデモスクリプト
スクリーンショット撮影用
"""

import logging
import logkiss
import os

def main():
    """各ログレベルの色を表示するメイン関数"""
    # ロガーの初期化をリセット
    logging.root.handlers = []
    
    # logkissのセットアップ
    # dictConfig用の設定辞書を作成
    config = {
        "version": 1,
        "formatters": {
            "colored": {
                "class": "logkiss.ColoredFormatter",
                "format": "%(asctime)s [%(levelname)s] %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logkiss.KissConsoleHandler",
                "level": "DEBUG",
                "formatter": "colored"
            }
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "DEBUG"
            }
        }
    }
    
    logkiss.dictConfig(config)
    logger = logging.getLogger()
    
    # すべてのログレベルを表示するために、DEBUGレベルに設定
    logger.setLevel(logging.DEBUG)
    
    # 各ログレベルでメッセージを出力
    logger.debug("これはDEBUGレベルのメッセージです (青色)")
    logger.info("これはINFOレベルのメッセージです (白色)")
    logger.warning("これはWARNINGレベルのメッセージです (黄色)")
    logger.error("これはERRORレベルのメッセージです (黒字に赤背景)")
    logger.critical("これはCRITICALレベルのメッセージです (黒字に明るい赤背景、太字)")
    
    # 区切り線
    print("\n" + "-" * 80 + "\n")
    
    # 環境変数NO_COLORを設定して色を無効化するデモ
    print("NO_COLOR環境変数を設定して色を無効化するデモ:")
    os.environ["NO_COLOR"] = "1"
    
    # ロガーの初期化をリセット
    logging.root.handlers = []
    
    # 新しいロガーを作成（NO_COLOR環境変数が反映される）
    # dictConfig用の設定辞書を作成
    config = {
        "version": 1,
        "formatters": {
            "colored": {
                "class": "logkiss.ColoredFormatter",
                "format": "%(asctime)s [%(levelname)s] %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logkiss.KissConsoleHandler",
                "level": "DEBUG",
                "formatter": "colored"
            }
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "DEBUG"
            }
        }
    }
    
    logkiss.dictConfig(config)
    no_color_logger = logging.getLogger()
    no_color_logger.setLevel(logging.DEBUG)
    
    # 各ログレベルでメッセージを出力（色なし）
    no_color_logger.debug("これはDEBUGレベルのメッセージです (色なし)")
    no_color_logger.info("これはINFOレベルのメッセージです (色なし)")
    no_color_logger.warning("これはWARNINGレベルのメッセージです (色なし)")
    no_color_logger.error("これはERRORレベルのメッセージです (色なし)")
    no_color_logger.critical("これはCRITICALレベルのメッセージです (色なし)")

if __name__ == "__main__":
    main()
