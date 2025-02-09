#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
import logkiss as logging

# ロガーの設定
console_logger = logging.getLogger('console_only')
both_logger = logging.getLogger('both')

# ファイルハンドラを作成
log_file = Path('both.log')
file_handler = logging.FileHandler(str(log_file))
file_handler.setFormatter(logging.Formatter(
    fmt='%(asctime)s,%(msecs)03d %(levelname)-5s | %(name)s | %(filename)s:%(lineno)3d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
both_logger.addHandler(file_handler)

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
    
    print(f"\nログファイルが作成されました: {log_file.absolute()}")
    print("ファイルの内容:")
    print("-" * 80)
    with open(log_file) as f:
        print(f.read().rstrip())
    print("-" * 80)

if __name__ == '__main__':
    main()
