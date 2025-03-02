#!/usr/bin/env python
"""
Google Cloud Logging サンプル

このサンプルでは、logkiss を使用して Google Cloud Logging にログを送信する方法を示します。

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
"""

import os
import time
import logging
import hashlib
import uuid
from datetime import datetime

# 環境変数から GCP の設定を取得
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

# logkiss をインポート
import logkiss
from logkiss.handlers import GCPCloudLoggingHandler

# ユニークなログ名を生成（テスト用）
def generate_test_log_name():
    """テスト用の一意のログ名を生成（短いハッシュ値を使用）"""
    timestamp = datetime.now().strftime("%Y%m%d")
    unique_id = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:12]
    return f"logkiss_test_{timestamp}_{unique_id}"

# クリーンアップフラグ（テスト後にリソースを削除するかどうか）
CLEAN_UP = True

def main():
    # ログ名を設定
    log_name = generate_test_log_name()
    print(f"ログ名: {log_name}")
    
    # ロガーを設定
    logger = logging.getLogger("gcp_sample")
    logger.setLevel(logging.DEBUG)
    
    # 既存のハンドラーをクリア（重複出力を避けるため）
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # コンソールハンドラーを追加
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # GCPCloudLoggingHandler を追加
    try:
        gcp_handler = GCPCloudLoggingHandler(
            project_id=GCP_PROJECT_ID,
            batch_size=10,  # 小さいバッチサイズを設定（サンプル用）
            flush_interval=2.0  # 短いフラッシュ間隔を設定（サンプル用）
        )
        logger.addHandler(gcp_handler)
        print("Google Cloud Logging ハンドラーを追加しました")
    except ImportError as e:
        print(f"エラー: {e}")
        print("google-cloud-logging パッケージをインストールしてください: pip install 'logkiss[cloud]'")
        return
    
    # ログを出力
    print("\n=== ログ出力を開始します ===")
    logger.info("Google Cloud Logging サンプルを開始します")
    logger.debug("これはデバッグメッセージです")
    
    # 構造化ログを出力
    logger.warning("ユーザーがログインに失敗しました", extra={
        "user_id": 12345,
        "ip_address": "192.168.1.100",
        "attempts": 3,
        "timestamp": time.time()
    })
    
    # エラーログを出力
    try:
        result = 10 / 0
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}", extra={
            "error_type": type(e).__name__,
            "timestamp": time.time()
        })
    
    # バッチがフラッシュされるのを待つ
    print("ログをGoogle Cloud Loggingに送信中...")
    time.sleep(3)
    
    # ハンドラーを明示的にクローズ
    print("ハンドラーをクローズしています...")
    gcp_handler.close()
    
    # ログの確認方法を表示
    print("\n=== ログの確認方法 ===")
    print(f"1. Google Cloud Console を開く: https://console.cloud.google.com/logs/")
    print(f"2. 以下のクエリでログを検索:")
    print(f"   resource.type=\"global\" AND logName=\"projects/{GCP_PROJECT_ID or '<your-project-id>'}/logs/{log_name}\"")
    print("\nまたは、以下の gcloud コマンドを実行:")
    print(f"gcloud logging read 'resource.type=\"global\" AND logName=\"projects/{GCP_PROJECT_ID or '<your-project-id>'}/logs/{log_name}\"'")
    
    # クリーンアップ（テスト用リソースの削除）
    if CLEAN_UP:
        print("\n=== クリーンアップ ===")
        print(f"ログ「{log_name}」を削除します...")
        try:
            from google.cloud import logging as google_logging
            client = google_logging.Client(project=GCP_PROJECT_ID)
            
            # ログエントリを削除するためのフィルタを作成
            filter_str = f'logName="projects/{client.project}/logs/{log_name}"'
            print(f"削除フィルタ: {filter_str}")
            
            # ログエントリを削除
            client.delete_entries(filter_=filter_str)
            print("ログエントリを削除しました")
        except Exception as e:
            print(f"ログエントリの削除中にエラーが発生しました: {e}")
    else:
        print("\n=== クリーンアップはスキップされました ===")
        print("CLEAN_UP = False に設定されているため、リソースは削除されません")

if __name__ == "__main__":
    main()
