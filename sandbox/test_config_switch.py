#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
設定ファイルを切り替えて出力するテスト

2つの異なる色設定ファイルを交互に切り替えて、合計4回の出力を行います。
"""

import logging
import os
import time
import logkiss
from logkiss import yaml_config


def print_all_log_levels(title):
    """すべてのログレベルでメッセージを出力する"""
    logger = logging.getLogger()
    
    print(f"\n--- {title} ---")
    logger.debug("これはDEBUGレベルのメッセージです")
    logger.info("これはINFOレベルのメッセージです")
    logger.warning("これはWARNINGレベルのメッセージです")
    logger.error("これはERRORレベルのメッセージです")
    logger.critical("これはCRITICALレベルのメッセージです")


def apply_config(config_path, title):
    """設定ファイルを適用して、すべてのログレベルでメッセージを出力する"""
    # ロガーの完全な初期化
    # ルートロガーのハンドラーをすべて削除
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]: 
        root_logger.removeHandler(handler)
    
    # ロギングモジュールをリロード
    import importlib
    importlib.reload(logging)
    
    # YAMLファイルから設定を読み込む
    import yaml
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 設定ファイルを適用
    yaml_config(config_path)
    
    # ColorManagerの設定を強制的に更新
    root_logger = logging.getLogger()
    if root_logger.handlers:
        formatter = root_logger.handlers[0].formatter
        if hasattr(formatter, 'color_manager'):
            # 色設定を完全に置き換え
            if 'formatters' in config:
                for _, formatter_config in config['formatters'].items():
                    if 'colors' in formatter_config:
                        # 色設定を完全に置き換え
                        formatter.color_manager.config = formatter_config['colors']
    
    # ログレベルをDEBUGに設定して、すべてのメッセージが表示されるようにする
    logging.getLogger().setLevel(logging.DEBUG)
    
    # すべてのログレベルでメッセージを出力
    print_all_log_levels(title)


def main():
    """メイン関数"""
    # 設定ファイルのパスを取得
    base_dir = os.path.dirname(__file__)
    config1_path = os.path.join(base_dir, "test.yaml")
    config2_path = os.path.join(base_dir, "alternative_config.yaml")
    
    # 設定1を適用して出力（1回目）
    apply_config(config1_path, "設定1（1回目）")
    
    # 少し待機して出力を見やすくする
    time.sleep(0.5)
    
    # 設定2を適用して出力（1回目）
    apply_config(config2_path, "設定2（1回目）")
    
    # 少し待機して出力を見やすくする
    time.sleep(0.5)
    
    # 設定1を適用して出力（2回目）
    apply_config(config1_path, "設定1（2回目）")
    
    # 少し待機して出力を見やすくする
    time.sleep(0.5)
    
    # 設定2を適用して出力（2回目）
    apply_config(config2_path, "設定2（2回目）")


if __name__ == "__main__":
    main()
