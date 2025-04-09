#!/usr/bin/env python
"""
Google Cloud Logging サンプル

このサンプルでは、logkiss を使用して Google Cloud Logging にログを送信する方法を示します。

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
"""

import os
import uuid
import time
import hashlib
from datetime import datetime

# 環境変数から GCP の設定を取得
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", None)  # デフォルト値をNoneに設定

# logkiss をインポート - シンプルに一度だけインポート
import logkiss
# GCPハンドラーは従来の方法でインポート
from logkiss.handler_gcp import GCloudLoggingHandler

# ユニークなログ名を生成（テスト用）
def generate_test_log_name():
    """テスト用の一意のログ名を生成（短いハッシュ値を使用）"""
    timestamp = datetime.now().strftime("%Y%m%d")
    unique_id = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:12]
    return f"logkiss_test_{timestamp}_{unique_id}"

# クリーンアップフラグ（テスト後にリソースを削除するかどうか）
CLEAN_UP = False  # True

def main():
    """メイン関数"""
    # ログ名を設定
    log_name = generate_test_log_name()
    print(f"ログ名: {log_name}")
    
    # ロガーの設定 - シンプルにgetLoggerを使用
    logger = logkiss.getLogger("gcp_sample")
    logger.setLevel(logkiss.logging.DEBUG)
    
    # 既存のハンドラーをクリア（重複出力を避けるため）
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # コンソールハンドラーを追加
    console_handler = logkiss.logging.StreamHandler()
    console_handler.setLevel(logkiss.logging.INFO)
    formatter = logkiss.logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # クラウドハンドラーを追加 - 遅延インポートにより必要になるまでSDKはロードされない
    try:
        gcp_handler = GCloudLoggingHandler(
            project_id=GCP_PROJECT_ID,
            log_name=log_name
        )
        logger.addHandler(gcp_handler)
        print("Cloud Loggingハンドラーを追加しました")
    except ImportError as e:
        print(f"エラー: {e}")
        print("必要な依存関係が見つかりません。以下のコマンドでインストールしてください:")
        print("    pip install 'logkiss[cloud]'")
        return
    
    # 基本的なログ出力テスト
    print("\n=== ログ出力テスト開始 ===")
    logger.info("Cloud Loggingサンプルを開始します")
    logger.debug("これはデバッグメッセージです")
    
    # 構造化ログ出力テスト
    logger.warning("ユーザー認証エラー", extra={
        "user_id": 12345,
        "ip_address": "192.168.1.100",
        "attempts": 3,
        "timestamp": time.time()
    })
    
    # エラーログ出力テスト
    try:
        calculation = 10 / 0  # わざと例外を発生させる
    except Exception as e:
        logger.error("計算エラーが発生しました: %s", str(e), extra={
            "error_type": type(e).__name__,
            "error_message": str(e),
            "timestamp": time.time(),
            "test_field": "これはテストフィールドです",
            "numeric_value": 42
        })
    
    # バッチがフラッシュされるのを待つ
    print("ログをCloud Loggingに送信中...")
    time.sleep(3)
    
    # ハンドラーを明示的にクローズ
    print("ハンドラーをクローズします...")
    gcp_handler.close()
    
    # ログの確認方法を表示
    print("\n=== ログの確認方法 ===")
    print("1. Google Cloud Console を開く: https://console.cloud.google.com/logs/")
    print("2. 以下のクエリでログを検索:")
    print(f"   resource.type=\"global\" AND logName=\"projects/{GCP_PROJECT_ID or '<your-project-id>'}/logs/{log_name}\"")
    print("\nまたは、以下のgcloudコマンドを実行:")
    print(f"gcloud logging read 'resource.type=\"global\" AND logName=\"projects/{GCP_PROJECT_ID or '<your-project-id>'}/logs/{log_name}\"'")
    
    # クリーンアップ（テスト用リソースの削除）
    if CLEAN_UP:
        print("\n=== クリーンアップ ===")
        print(f"ログ「{log_name}」を削除します...")
        try:
            # Google Cloud SDKにアクセスするのはここでだけ
            from google.cloud import logging as google_logging
            client = google_logging.Client(project=GCP_PROJECT_ID)
            
            # ログエントリを削除するためのフィルタを作成
            filter_str = f'logName="projects/{client.project}/logs/{log_name}"'
            print(f"削除フィルタ: {filter_str}")

            # web consoleを開く
            import webbrowser
            console_url = f"https://console.cloud.google.com/logs/query;query=resource.type%3D%22global%22%20AND%20logName%3D%22projects%2F{client.project}%2Flogs%2F{log_name}%22?project={client.project}"
            print(f"ログコンソールを開きます: {console_url}")
            webbrowser.open(console_url)
            
            # ブラウザが開くのを待つ
            time.sleep(2)
            
            # 注意: Google Cloud Loggingには直接ログを削除するAPIがないため、
            # 実際のクリーンアップはGCPコンソールまたはgcloudコマンドで行う必要があります
            print("注意: Google Cloud Loggingには直接ログを削除するAPIがありません。")
            print("GCPコンソールまたはgcloudコマンドを使用して手動でログを削除してください。")
            print("例: gcloud logging logs delete " + log_name)
        except Exception as e:
            print(f"クリーンアップ中にエラーが発生しました: {e}")
    else:
        print("\n=== クリーンアップはスキップされました ===")
        print("CLEAN_UP = False に設定されているため、リソースは削除されません")

if __name__ == "__main__":
    main()
