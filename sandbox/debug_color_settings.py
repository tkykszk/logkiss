#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
色設定のデバッグ用スクリプト

設定ファイルを切り替えた際に、ColorManagerの設定が正しく変更されているか確認します。
"""

import logging
import logging.config
import os
import yaml
from logkiss import yaml_config


def debug_color_settings(config_path, title):
    """設定ファイルを適用して、ColorManagerの設定をデバッグ出力する"""
    print("=== " + title + " ===")
    
    # 設定ファイルの内容を直接読み込んで表示
    with open(config_path, 'r', encoding='utf-8') as f:
        config_content = yaml.safe_load(f)
    
    print("設定ファイルの内容（" + os.path.basename(config_path) + "）:")
    if 'formatters' in config_content:
        for name, formatter_config in config_content['formatters'].items():
            if 'colors' in formatter_config:
                print(f"  - formatter: {name}")
                print("  - colors:")
                if 'levels' in formatter_config['colors']:
                    print("    - levels:")
                    for level_name, level_config in formatter_config['colors']['levels'].items():
                        print(f"      - {level_name}: {level_config}")
                if 'elements' in formatter_config['colors'] and 'message' in formatter_config['colors']['elements']:
                    print("    - elements.message:")
                    for level_name, msg_config in formatter_config['colors']['elements']['message'].items():
                        print(f"      - {level_name}: {msg_config}")
    
    # ロガーを完全にリセット
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        
    # 全てのロガーをリセット
    # loggingモジュールを再ロードする
    import importlib
    importlib.reload(logging)
    
    # 設定ファイルを適用
    yaml_config(config_path)
    
    # ColorManagerの設定を確認
    root_logger = logging.getLogger()
    if root_logger.handlers:
        formatter = root_logger.handlers[0].formatter
        if hasattr(formatter, 'color_manager'):
            print("\nColorManagerの設定:")
            print(f"  - 設定ファイル: {config_path}")
            
            # 色設定の内容を表示
            print("  - 色設定:")
            for level_name, level_config in formatter.color_manager.config.get("levels", {}).items():
                print(f"    - {level_name}: {level_config}")
            
            # メッセージの色設定を表示
            print("  - メッセージの色設定:")
            for level_name, msg_config in formatter.color_manager.config.get("elements", {}).get("message", {}).items():
                print(f"    - {level_name}: {msg_config}")
            
            # 実際の色付きメッセージを出力
            print("\n実際の出力:")
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            logger.debug("これはDEBUGレベルのメッセージです")
            logger.info("これはINFOレベルのメッセージです")
            logger.warning("これはWARNINGレベルのメッセージです")
            logger.error("これはERRORレベルのメッセージです")
            logger.critical("これはCRITICALレベルのメッセージです")
        else:
            print("ColorManagerが見つかりません")
    else:
        print("ロガーにハンドラーがありません")


def main():
    """メイン関数"""
    # 設定ファイルのパスを取得
    base_dir = os.path.dirname(__file__)
    config1 = os.path.join(base_dir, "test.yaml")
    config2 = os.path.join(base_dir, "alternative_config.yaml")
    
    # 両方の設定ファイルの内容を表示
    print("=== 設定ファイルの内容 ===")
    for config_path in [config1, config2]:
        print(f"\n{os.path.basename(config_path)}の内容:")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            if 'formatters' in config:
                for _, formatter_config in config['formatters'].items():
                    if "colors" in formatter_config:
                        print(f"\n{os.path.basename(config_path)}の内容:")
                        print(f"  - colors: {formatter_config['colors']}")
    
    # 設定を切り替えてデバッグ出力
    debug_color_settings(config1, "設定1")
    debug_color_settings(config2, "設定2")
    debug_color_settings(config1, "設定1（再適用）")


if __name__ == "__main__":
    main()
