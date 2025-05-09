#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
設定ファイルを切り替えて出力するテスト

2つの異なる色設定ファイルを交互に切り替えて、合計4回の出力を行います。
シンプルな実装で、メイン側で数行で設定を切り替えられます。
"""

import os
import time
import logging
from logkiss.config import yaml_config


def switch_config(config_path, title):
    """設定ファイルを切り替えてログを出力するシンプルな関数"""
    # ロガーをリセット
    logging.root.handlers = []
    
    # 設定ファイルを適用
    # ライブラリ側で色設定が完全に置き換えられるように修正済み
    yaml_config(config_path)
    
    # DEBUGレベルに設定
    logging.getLogger().setLevel(logging.DEBUG)
    
    # ログ出力
    print(f"\n--- {title} ---")
    logger = logging.getLogger()
    logger.debug("これはDEBUGレベルのメッセージです")
    logger.info("これはINFOレベルのメッセージです")
    logger.warning("これはWARNINGレベルのメッセージです")
    logger.error("これはERRORレベルのメッセージです")
    logger.critical("これはCRITICALレベルのメッセージです")


def main():
    """メイン関数"""
    # 設定ファイルのパスを取得
    base_dir = os.path.dirname(__file__)
    config1 = os.path.join(base_dir, "test.yaml")
    config2 = os.path.join(base_dir, "alternative_config.yaml")
    
    # 4回の設定切り替えをシンプルに実行
    switch_config(config1, "設定1（1回目）")
    time.sleep(0.5)
    
    switch_config(config2, "設定2（1回目）")
    time.sleep(0.5)
    
    switch_config(config1, "設定1（2回目）")
    time.sleep(0.5)
    
    switch_config(config2, "設定2（2回目）")


if __name__ == "__main__":
    main()
