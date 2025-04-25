#!/usr/bin/env python
"""
AWS CloudWatch Logs サンプル

このサンプルでは、logkiss を使用して AWS CloudWatch Logs にログを送信する方法を示します。

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
"""

import json
import os
import socket
import uuid
import hashlib
import time
from datetime import datetime

# 環境変数から AWS の設定を取得
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

# logkiss をインポート - シンプルに一度だけインポート
import logkiss
from logkiss.handlers import AWSCloudWatchHandler


# ユニークなロググループ名を生成（テスト用）
def generate_test_log_group_name():
    """テスト用の一意のロググループ名を生成（短いハッシュ値を使用）"""
    timestamp = datetime.now().strftime("%Y%m%d")
    unique_id = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:12]
    return f"logkiss-test-{timestamp}-{unique_id}"


# クリーンアップフラグ（テスト後にリソースを削除するかどうか）
CLEAN_UP = True


def main():
    """メイン関数"""
    # ロググループとストリームの名前を設定
    log_group_name = generate_test_log_group_name()
    log_stream_name = f"sample-{datetime.now().strftime('%H%M%S')}"
    print(f"ロググループ名: {log_group_name}")
    print(f"ログストリーム名: {log_stream_name}")

    # ロガーの設定 - シンプルにgetLoggerを使用
    logger = logkiss.getLogger("aws_sample")
    logger.setLevel(logkiss.logging.DEBUG)

    # 既存のハンドラーをクリア（重複出力を避けるため）
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # コンソールハンドラーを追加
    console_handler = logkiss.logging.StreamHandler()
    console_handler.setLevel(logkiss.logging.INFO)
    formatter = logkiss.logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # クラウドハンドラーを追加 - 遅延インポートにより必要になるまでSDKはロードされない
    try:
        aws_handler = AWSCloudWatchHandler(
            log_group_name=log_group_name,
            log_stream_name=log_stream_name,
            region_name=AWS_REGION,
            batch_size=10,  # サンプル用に小さいバッチサイズ
            flush_interval=2.0,  # サンプル用に短いフラッシュ間隔
        )
        logger.addHandler(aws_handler)
        print("CloudWatchLogsハンドラーを追加しました")
    except ImportError as e:
        print(f"エラー: {e}")
        print("必要な依存関係が見つかりません。以下のコマンドでインストールしてください:")
        print("    pip install 'logkiss[cloud]'")
        return

    # 基本的なログ出力テスト
    print("\n=== ログ出力テスト開始 ===")
    logger.info("CloudWatchLogsサンプルを開始します")
    logger.debug("これはデバッグメッセージです")

    # 構造化ログ出力テスト
    logger.warning("ユーザー認証エラー", extra={"user_id": 12345, "ip_address": "192.168.1.100", "attempts": 3, "timestamp": time.time()})

    # エラーログ出力テスト
    try:
        result = 10 / 0  # わざと例外を発生させる
    except Exception as e:
        logger.error("計算エラーが発生しました: %s", str(e), extra={"error_type": type(e).__name__, "timestamp": time.time()})

    # バッチがフラッシュされるのを待つ
    print("ログをCloudWatchLogsに送信中...")
    time.sleep(3)

    # ハンドラーを明示的にクローズ
    print("ハンドラーをクローズします...")
    aws_handler.close()

    # ログの確認方法を表示
    print("\n=== ログの確認方法 ===")
    print("1. AWS マネジメントコンソールを開く: https://console.aws.amazon.com/cloudwatch/")
    print("2. 左側のメニューから「ロググループ」を選択")
    print(f"3. ロググループ「{log_group_name}」を検索")
    print(f"4. ログストリーム「{log_stream_name}」をクリック")
    print("\nまたは、以下のAWS CLIコマンドを実行:")
    print(f"aws logs get-log-events --log-group-name {log_group_name} " f"--log-stream-name {log_stream_name} --region {AWS_REGION}")

    # クリーンアップ（テスト用リソースの削除）
    if CLEAN_UP:
        print("\n=== クリーンアップ ===")
        print(f"ロググループ「{log_group_name}」を削除します...")
        try:
            import boto3

            logs_client = boto3.client("logs", region_name=AWS_REGION)

            # CloudWatch Logsコンソールを開く
            import webbrowser

            region = logs_client.meta.region_name
            console_url = f"https://{region}.console.aws.amazon.com/cloudwatch/home?region={region}#logsV2:log-groups/log-group/{log_group_name}"
            print(f"CloudWatch Logsコンソールを開きます: {console_url}")
            webbrowser.open(console_url)

            # ブラウザが開くのを待ってからリソースを削除
            time.sleep(2)

            # ロググループを削除
            logs_client.delete_log_group(logGroupName=log_group_name)
            print("ロググループを削除しました")
        except Exception as e:
            print(f"クリーンアップ中にエラーが発生しました: {e}")
    else:
        print("\n=== クリーンアップはスキップされました ===")
        print("CLEAN_UP = False に設定されているため、リソースは削除されません")


if __name__ == "__main__":
    main()
