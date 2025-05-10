#!/usr/bin/env python
"""
Google Cloud Logging Sample

This sample demonstrates how to send logs to Google Cloud Logging using logkiss.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
"""

import os
import uuid
from datetime import datetime
import logging
import hashlib
from google.cloud import logging as google_logging

# Get GCP settings from environment variables
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

# Import logkiss
import logkiss
from logkiss.handler_gcp import GCloudLoggingHandler


# Generate unique log name (for testing)
def generate_test_log_name():
    """Generate a unique log name for testing (using short hash value)"""
    timestamp = datetime.now().strftime("%Y%m%d")
    unique_id = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:12]
    return f"logkiss_test_{timestamp}_{unique_id}"


# Cleanup flag (whether to delete resources after testing)
CLEAN_UP = False  # True


def main():
    """Main function"""
    # Import necessary modules
    import time
    import logging
    from logkiss import getLogger

    # Set log name
    log_name = generate_test_log_name()
    print(f"Log name: {log_name}")

    # Configure logger
    logger = getLogger("gcp_sample")
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers (to avoid duplicate output)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add GCloudLoggingHandler
    try:
        gcp_handler = GCloudLoggingHandler(
            project_id=GCP_PROJECT_ID,
            log_name=log_name,
        )
        logger.addHandler(gcp_handler)
        print("Added Google Cloud Logging handler")
    except ImportError as e:
        print(f"Error: {e}")
        print("Please install the google-cloud-logging package: pip install 'logkiss[cloud]'")
        return

    # Output logs
    print("\n=== Starting log output ===")
    logger.info("Starting Google Cloud Logging sample")
    logger.debug("This is a debug message")

    # Output structured log
    logger.warning(
        "User failed to login", extra={"user_id": 12345, "ip_address": "192.168.1.100", "attempts": 3, "timestamp": time.time()}
    )

    # Output error log
    try:
        result = 10 / 0
    except Exception as e:
        logger.error(
            f"An error occurred: {str(e)}",
            extra={
                "error_type": type(e).__name__,
                "error_message": str(e),
                "timestamp": time.time(),
                "test_field": "This is a test field",
                "numeric_value": 42,
            },
        )

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
            client = google_logging.Client(project=GCP_PROJECT_ID)

            # ログエントリを削除するためのフィルタを作成
            filter_str = f'logName="projects/{client.project}/logs/{log_name}"'
            print(f"削除フィルタ: {filter_str}")

            # web consoleを開く
            import webbrowser

            console_url = f"https://console.cloud.google.com/logs/query;query=resource.type%3D%22global%22%20AND%20logName%3D%22projects%2F{client.project}%2Flogs%2F{log_name}%22?project={client.project}"
            print(f"ログコンソールを開きます: {console_url}")
            webbrowser.open(console_url)

            # 少し待ってからログを削除（ブラウザが開くのを待つ）
            import time

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
