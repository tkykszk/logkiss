#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Google Cloud Logging Handler サンプル

このサンプルでは、GCloudLoggingHandlerを使用してGoogle Cloud Loggingにログを送信する方法を示します。
このハンドラーは、Google Cloud Loggingの公式クライアントライブラリを使用しています。

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
"""

import os
import sys
import time
import logging
import traceback
from datetime import datetime

# logkissモジュールをインポート
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logkiss
from logkiss.handler_gcp import GCloudLoggingHandler, setup_gcp_logging


def simple_example():
    """シンプルな使用例"""
    # 環境変数からGCPプロジェクトIDを取得
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        print("環境変数 GCP_PROJECT_ID が設定されていません。")
        print("例: export GCP_PROJECT_ID=your-project-id")
        sys.exit(1)
    
    # ログ名を設定（一意の名前を使用）
    log_name = f"logkiss_test_{datetime.now().strftime('%Y%m%d')}_{os.urandom(4).hex()}"
    
    print(f"Google Cloud Loggingにログを送信します (プロジェクトID: {project_id}, ログ名: {log_name})")
    
    # Google Cloud Loggingの設定
    handler = GCloudLoggingHandler(
        project_id=project_id,
        log_name=log_name,
        labels={
            "application": "logkiss_sample",
            "environment": "development"
        }
    )
    
    # ハンドラーをルートロガーに追加
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.DEBUG)
    
    # 各レベルのログを出力
    logging.debug("これはDEBUGレベルのログです")
    logging.info("これはINFOレベルのログです")
    logging.warning("これはWARNINGレベルのログです")
    logging.error("これはERRORレベルのログです")
    
    # 構造化ログの出力
    logging.info("構造化ログの例", extra={
        "user_id": "12345",
        "action": "login",
        "timestamp": time.time()
    })
    
    # 例外ログの出力
    try:
        result = 10 / 0
    except Exception as e:
        logging.error(f"エラーが発生しました: {str(e)}", extra={
            "error_type": type(e).__name__,
            "error_message": str(e),
            "stack_trace": traceback.format_exc()
        })
    
    print("ログをGoogle Cloud Loggingに送信しました")
    print(f"Google Cloud Loggingコンソールで確認できます: https://console.cloud.google.com/logs/query?project={project_id}")


def setup_logging_example():
    """setup_logging関数を使用した例"""
    # 環境変数からGCPプロジェクトIDを取得
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        print("環境変数 GCP_PROJECT_ID が設定されていません。")
        print("例: export GCP_PROJECT_ID=your-project-id")
        sys.exit(1)
    
    # ログ名を設定（一意の名前を使用）
    log_name = f"logkiss_setup_{datetime.now().strftime('%Y%m%d')}_{os.urandom(4).hex()}"
    
    print(f"Google Cloud Loggingにログを送信します (プロジェクトID: {project_id}, ログ名: {log_name})")
    
    # setup_logging関数を使用してロギングを設定
    setup_gcp_logging(
        project_id=project_id,
        log_name=log_name,
        labels={
            "application": "logkiss_setup_sample",
            "environment": "development"
        },
        level=logging.DEBUG,
        root_level=logging.DEBUG
    )
    
    # 各レベルのログを出力
    logging.debug("これはDEBUGレベルのログです (setup_logging)")
    logging.info("これはINFOレベルのログです (setup_logging)")
    logging.warning("これはWARNINGレベルのログです (setup_logging)")
    logging.error("これはERRORレベルのログです (setup_logging)")
    
    # 構造化ログの出力
    logging.info("構造化ログの例 (setup_logging)", extra={
        "user_id": "67890",
        "action": "logout",
        "timestamp": time.time()
    })
    
    print("ログをGoogle Cloud Loggingに送信しました")
    print(f"Google Cloud Loggingコンソールで確認できます: https://console.cloud.google.com/logs/query?project={project_id}")


if __name__ == "__main__":
    # シンプルな使用例
    simple_example()
    
    print("\n" + "-" * 50 + "\n")
    
    # setup_logging関数を使用した例
    setup_logging_example()
