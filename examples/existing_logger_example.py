#!/usr/bin/env python
"""
既存のロギング設定に logkiss を追加するサンプル

このサンプルでは、既に設定されている標準の logging モジュールに
logkiss の KissConsoleHandler を追加する方法を示します。

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
"""

import logging
import sys

# メイン処理
def main():
    # デフォルトのロガー設定を使用
    # 基本的な設定だけ行う（ロガーレベルの設定のみ）
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("my_app")
    logger.setLevel(logging.DEBUG)
    
    print("=== デフォルトのロガー設定 ===")
    logging.info("これはルートロガーからの情報メッセージです")
    logger.debug("これはアプリケーションロガーからのデバッグメッセージです")
    logger.info("これはアプリケーションロガーからの情報メッセージです")
    
    # 既存のロガーのハンドラーを一時的に保存
    root_handlers = logging.getLogger().handlers[:]
    app_handlers = logger.handlers[:]
    
    # 既存のロガーからハンドラーを削除
    for handler in logging.getLogger().handlers[:]:
        logging.getLogger().removeHandler(handler)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    print("\n=== logkiss の KissConsoleHandler を使用 ===")
    # ここで logkiss をインポート
    import logkiss
    from logkiss.logkiss import KissConsoleHandler
    
    # KissConsoleHandler を追加
    kiss_handler = KissConsoleHandler()
    logger.addHandler(kiss_handler)
    
    # ログを出力
    logger.debug("これはKissConsoleHandlerを使ったデバッグメッセージです")
    logger.info("これはKissConsoleHandlerを使った情報メッセージです")
    
    # 構造化ログを出力
    logger.warning("構造化ログの例", extra={
        "user_id": 12345,
        "action": "login",
        "status": "failure",
        "attempts": 3
    })
    
    print("\n=== ルートロガーにも logkiss の KissConsoleHandler を追加 ===")
    # ルートロガーに KissConsoleHandler を追加
    root_kiss_handler = KissConsoleHandler()
    logging.getLogger().addHandler(root_kiss_handler)
    
    # ログを出力
    logging.info("これはKissConsoleHandlerを使ったルートロガーからの情報メッセージです")
    logger.debug("これはKissConsoleHandlerを使ったデバッグメッセージです")
    logger.info("これはKissConsoleHandlerを使った情報メッセージです")
    
    # 元のハンドラーを復元
    print("\n=== 元のロガー設定に戻す ===")
    # 現在のハンドラーを削除
    for handler in logging.getLogger().handlers[:]:
        logging.getLogger().removeHandler(handler)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 元のハンドラーを復元
    for handler in root_handlers:
        logging.getLogger().addHandler(handler)
    for handler in app_handlers:
        logger.addHandler(handler)
    
    # 元のロガー設定でログを出力
    logging.info("元の設定に戻したルートロガーからの情報メッセージです")
    logger.debug("元の設定に戻したアプリケーションロガーからのデバッグメッセージです")
    logger.info("元の設定に戻したアプリケーションロガーからの情報メッセージです")

    # README.md に説明を追加
    print("\n=== 説明 ===")
    print("このサンプルでは、既存のロギング設定に logkiss の KissConsoleHandler を追加する方法を示しています。")
    print("1. デフォルトのロガー設定を使用してログを出力（basicConfigでレベルのみ設定）")
    print("2. 既存のハンドラーを一時的に保存して削除")
    print("3. logkiss の KissConsoleHandler を追加してログを出力（formatterを変更せずに使用可能）")
    print("4. 元のハンドラーを復元して元の設定に戻す")
    print("\nこの方法を使えば、既存のコードを大幅に変更することなく、")
    print("必要なときだけ logkiss の色付きログ出力を利用できます。")

if __name__ == "__main__":
    main()
