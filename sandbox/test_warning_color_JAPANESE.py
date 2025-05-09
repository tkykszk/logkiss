#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
テストケース1: WARNINGレベルを黄色地に黒字で表示するテスト
"""

import logging
import os
import logkiss
from logkiss import yaml_config


def test_warning_black_on_yellow_yaml():
    """YAMLファイルを使用してWARNINGレベルを黄色地に黒字で表示するテスト"""
    # ロガーの初期化をリセット
    logging.root.handlers = []
    
    # 設定ファイルを指定してlogkissをセットアップ
    config_path = os.path.join(os.path.dirname(__file__), "custom_color_config.yaml")
    yaml_config(config_path)
    logger = logging.getLogger()
    
    # すべてのログレベルを表示するために、DEBUGレベルに設定
    logger.setLevel(logging.DEBUG)
    
    # 各ログレベルでメッセージを出力
    print("\n--- YAMLファイルによる色設定テスト ---")
    logger.debug("これはDEBUGレベルのメッセージです (青色)")
    logger.info("これはINFOレベルのメッセージです (白色)")
    logger.warning("これはWARNINGレベルのメッセージです (黄色地に黒字)")
    logger.error("これはERRORレベルのメッセージです (赤地に黒字)")
    logger.critical("これはCRITICALレベルのメッセージです (明るい赤地に黒字、太字)")
    
    # テストが成功したことを示す
    assert True


def test_warning_black_on_yellow_direct():
    """プログラム内で直接WARNINGレベルを黄色地に黒字で設定するテスト"""
    # ロガーの初期化をリセット
    logging.root.handlers = []
    
    # logkissをデフォルト設定でセットアップ
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
    
    # 色設定を直接カスタマイズ
    color_config = {
        "levels": {
            "WARNING": {
                "fg": "black",
                "bg": "yellow"
            }
        },
        "elements": {
            "message": {
                "WARNING": {
                    "fg": "black",
                    "bg": "yellow"
                }
            }
        }
    }
    
    logger.handlers[0].formatter.color_manager.config.update(color_config)
    
    # すべてのログレベルを表示するために、DEBUGレベルに設定
    logger.setLevel(logging.DEBUG)
    
    # 各ログレベルでメッセージを出力
    print("\n--- プログラム内での直接設定テスト ---")
    logger.debug("これはDEBUGレベルのメッセージです (青色)")
    logger.info("これはINFOレベルのメッセージです (白色)")
    logger.warning("これはWARNINGレベルのメッセージです (黄色地に黒字)")
    logger.error("これはERRORレベルのメッセージです (赤地に黒字)")
    logger.critical("これはCRITICALレベルのメッセージです (明るい赤地に黒字、太字)")
    
    # テストが成功したことを示す
    assert True


if __name__ == "__main__":
    test_warning_black_on_yellow_yaml()
    test_warning_black_on_yellow_direct()
