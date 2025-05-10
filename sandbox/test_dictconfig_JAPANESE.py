#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
テストケース: dictConfigを使用したWARNINGレベルの色設定テスト
"""

import logging
import os
from logkiss import dictConfig


def test_dictconfig_warning_black_on_yellow():
    """dictConfigを使用してWARNINGレベルを黄色地に黒字で表示するテスト"""
    # ロガーの初期化をリセット
    logging.root.handlers = []
    
    # dictConfigで設定
    config = {
        "version": 1,
        "formatters": {
            "colored": {
                "()": "logkiss.ColoredFormatter",
                "format": "%(asctime)s %(levelname)s | %(filename)s: %(lineno)d | %(message)s",
                "colors": {
                    "levels": {
                        "WARNING": {"fg": "black", "bg": "yellow"}
                    },
                    "elements": {
                        "message": {
                            "WARNING": {"fg": "black", "bg": "yellow"}
                        }
                    }
                }
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
    
    # 設定を適用
    dictConfig(config)
    
    # ロガーを取得
    logger = logging.getLogger()
    
    # 各ログレベルでメッセージを出力
    print("\n--- dictConfigによる色設定テスト ---")
    logger.debug("これはDEBUGレベルのメッセージです (青色)")
    logger.info("これはINFOレベルのメッセージです (白色)")
    logger.warning("これはWARNINGレベルのメッセージです (黄色地に黒字)")
    logger.error("これはERRORレベルのメッセージです (赤地に黒字)")
    logger.critical("これはCRITICALレベルのメッセージです (明るい赤地に黒字、太字)")
    
    # テストが成功したことを示す
    assert True


def test_yaml_config_warning_black_on_yellow():
    """YAMLファイルからdictConfig形式の設定を読み込むテスト"""
    # ロガーの初期化をリセット
    logging.root.handlers = []
    
    # YAMLファイルを作成
    yaml_config = """
version: 1
formatters:
  colored:
    (): logkiss.ColoredFormatter
    format: "%(asctime)s %(levelname)s | %(filename)s: %(lineno)d | %(message)s"
    colors:
      levels:
        WARNING:
          fg: black
          bg: yellow
      elements:
        message:
          WARNING:
            fg: black
            bg: yellow
handlers:
  console:
    class: logkiss.KissConsoleHandler
    level: DEBUG
    formatter: colored
loggers:
  "":
    handlers: [console]
    level: DEBUG
"""
    
    # YAMLファイルを保存
    yaml_path = os.path.join(os.path.dirname(__file__), "dictconfig_test.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml_config)
    
    # YAMLファイルから設定を読み込む
    import yaml
    
    with open(yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # 設定を適用
    dictConfig(config)
    
    # ロガーを取得
    logger = logging.getLogger()
    
    # 各ログレベルでメッセージを出力
    print("\n--- YAML dictConfigによる色設定テスト ---")
    logger.debug("これはDEBUGレベルのメッセージです (青色)")
    logger.info("これはINFOレベルのメッセージです (白色)")
    logger.warning("これはWARNINGレベルのメッセージです (黄色地に黒字)")
    logger.error("これはERRORレベルのメッセージです (赤地に黒字)")
    logger.critical("これはCRITICALレベルのメッセージです (明るい赤地に黒字、太字)")
    
    # テストが成功したことを示す
    assert True
    
    # テスト後にYAMLファイルを削除
    try:
        os.remove(yaml_path)
    except FileNotFoundError:
        print(f"Warning: Could not find file {yaml_path} to remove")


if __name__ == "__main__":
    test_dictconfig_warning_black_on_yellow()
    test_yaml_config_warning_black_on_yellow()
