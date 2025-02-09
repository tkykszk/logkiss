#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
import logkiss as logging

# ログファイルのパス
log_file = os.path.join(os.path.dirname(__file__), 'both.log')

# コンソールのみのロガーを作成
console_logger = logging.getLogger('console')
for handler in console_logger.handlers[:]:
    console_logger.removeHandler(handler)
console_logger.setLevel(logging.DEBUG)
console_handler = logging.KissConsoleHandler()
console_logger.addHandler(console_handler)
console_logger.propagate = False

# コンソールとファイルの両方に出力するロガーを作成
both_logger = logging.getLogger('both')
for handler in both_logger.handlers[:]:
    both_logger.removeHandler(handler)
both_logger.setLevel(logging.DEBUG)
both_logger.addHandler(logging.KissConsoleHandler())
both_logger.addHandler(logging.KissFileHandler(log_file))
both_logger.propagate = False

def main():
    """メイン関数"""
    print("\n1. コンソールのみのロガー:")
    console_logger.debug("デバッグメッセージ (コンソールのみ)")
    console_logger.info("情報メッセージ (コンソールのみ)")
    console_logger.warning("警告メッセージ (コンソールのみ)")
    console_logger.error("エラーメッセージ (コンソールのみ)")
    console_logger.critical("重大なエラーメッセージ (コンソールのみ)")
    
    print("\n2. コンソールとファイルの両方に出力するロガー:")
    both_logger.debug("デバッグメッセージ (両方)")
    both_logger.info("情報メッセージ (両方)")
    both_logger.warning("警告メッセージ (両方)")
    both_logger.error("エラーメッセージ (両方)")
    both_logger.critical("重大なエラーメッセージ (両方)")
    
    print(f"\nログファイルが作成されました: {log_file}")
    print("ファイルの内容:")
    print("-" * 80)
    with open(log_file, 'r') as f:
        print(f.read().rstrip())
    print("-" * 80)

if __name__ == '__main__':
    main()
