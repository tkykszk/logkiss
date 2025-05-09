#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
色設定の適用プロセスをデバッグするためのスクリプト

このスクリプトは、alternative_config.yamlの色設定が反映されない原因を調査します。
"""

import logging
import os
import yaml
import sys
import pprint
import copy
import logkiss
from logkiss import yaml_config
from logkiss.logkiss import ColoredFormatter


def print_color_manager_config(title, logger=None):
    """ColorManagerの設定を表示する"""
    if logger is None:
        logger = logging.getLogger()
    
    print(f"\n=== {title} ===")
    
    if not logger.handlers:
        print("ロガーにハンドラーがありません")
        return
    
    formatter = logger.handlers[0].formatter
    if not isinstance(formatter, ColoredFormatter):
        print(f"フォーマッターがColoredFormatterではありません: {type(formatter)}")
        return
    
    print(f"フォーマット文字列: {formatter._fmt}")
    print(f"use_color: {formatter.use_color}")
    print("ColorManager設定:")
    pprint.pprint(formatter.color_manager.config)


def load_yaml_file(file_path):
    """YAMLファイルを読み込む"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def debug_config_application(config_path):
    """設定ファイルの適用プロセスをデバッグする"""
    # 設定ファイルの内容を表示
    print(f"\n=== 設定ファイル: {config_path} ===")
    config = load_yaml_file(config_path)
    print("設定内容:")
    pprint.pprint(config)
    
    # ロガーの初期状態を表示
    print_color_manager_config("適用前のロガー状態")
    
    # ロガーの初期化
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]: 
        root_logger.removeHandler(handler)
    
    # 設定ファイルを適用
    print("\n=== yaml_config関数を呼び出し ===")
    yaml_config(config_path)
    
    # 適用後のロガー状態を表示
    print_color_manager_config("適用後のロガー状態")
    
    # 色設定を直接適用してみる
    print("\n=== 色設定を直接適用 ===")
    root_logger = logging.getLogger()
    if root_logger.handlers:
        formatter = root_logger.handlers[0].formatter
        if isinstance(formatter, ColoredFormatter):
            # 設定ファイルから色設定を取得
            colors_config = None
            for _, formatter_config in config['formatters'].items():
                if 'colors' in formatter_config:
                    colors_config = formatter_config['colors']
                    break
            
            if colors_config:
                print("適用する色設定:")
                pprint.pprint(colors_config)
                
                # 色設定を完全に置き換え
                old_config = copy.deepcopy(formatter.color_manager.config)
                formatter.color_manager.config = colors_config
                
                print("置き換え後の色設定:")
                pprint.pprint(formatter.color_manager.config)
                
                # 元の設定と比較
                print("\n=== 設定の比較 ===")
                print("変更前:")
                pprint.pprint(old_config)
                print("変更後:")
                pprint.pprint(formatter.color_manager.config)
    
    # テストメッセージを出力
    print("\n=== テストメッセージ ===")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.debug("これはDEBUGレベルのメッセージです")
    logger.info("これはINFOレベルのメッセージです")
    logger.warning("これはWARNINGレベルのメッセージです")
    logger.error("これはERRORレベルのメッセージです")
    logger.critical("これはCRITICALレベルのメッセージです")


def main():
    """メイン関数"""
    # 設定ファイルのパスを取得
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, "alternative_config.yaml")
    
    # 設定ファイルの適用プロセスをデバッグ
    debug_config_application(config_path)


if __name__ == "__main__":
    main()
