#!/usr/bin/env python
"""
AWS CloudWatch Logs サンプル

このサンプルでは、logkiss を使用して AWS CloudWatch Logs にログを送信する方法を示します。

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
"""

import os
import time
import logging
import hashlib
import uuid
from datetime import datetime

# 環境変数から AWS の設定を取得
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

# logkiss をインポート
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
    # ロググループとストリームの名前を設定
    log_group_name = generate_test_log_group_name()
    log_stream_name = f"sample-{datetime.now().strftime('%H%M%S')}"
    
    print(f"ロググループ名: {log_group_name}")
    print(f"ログストリーム名: {log_stream_name}")
    
    # ロガーを設定
    logger = logging.getLogger("aws_sample")
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
    
    # AWSCloudWatchHandler を追加
    try:
        aws_handler = AWSCloudWatchHandler(
            log_group_name=log_group_name,
            log_stream_name=log_stream_name,
            region_name=AWS_REGION,
            batch_size=10,  # 小さいバッチサイズを設定（サンプル用）
            flush_interval=2.0  # 短いフラッシュ間隔を設定（サンプル用）
        )
        logger.addHandler(aws_handler)
        print("AWS CloudWatch Logs ハンドラーを追加しました")
    except ImportError as e:
        print(f"エラー: {e}")
        print("boto3 パッケージをインストールしてください: pip install 'logkiss[cloud]'")
        return
    
    # ログを出力
    print("\n=== ログ出力を開始します ===")
    logger.info("AWS CloudWatch Logs サンプルを開始します")
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
    print("ログをCloudWatch Logsに送信中...")
    time.sleep(3)
    
    # ハンドラーを明示的にクローズ
    print("ハンドラーをクローズしています...")
    aws_handler.close()
    
    # ログの確認方法を表示
    print("\n=== ログの確認方法 ===")
    print(f"1. AWS マネジメントコンソールを開く: https://console.aws.amazon.com/cloudwatch/")
    print(f"2. 左側のメニューから「ロググループ」を選択")
    print(f"3. ロググループ「{log_group_name}」を検索")
    print(f"4. ログストリーム「{log_stream_name}」をクリック")
    print("\nまたは、以下の AWS CLI コマンドを実行:")
    print(f"aws logs get-log-events --log-group-name {log_group_name} "
          f"--log-stream-name {log_stream_name} --region {AWS_REGION}")
    
    # クリーンアップ（テスト用リソースの削除）
    if CLEAN_UP:
        print("\n=== クリーンアップ ===")
        print(f"ロググループ「{log_group_name}」を削除します...")
        try:
            import boto3
            logs_client = boto3.client('logs', region_name=AWS_REGION)
            logs_client.delete_log_group(logGroupName=log_group_name)
            print("ロググループを削除しました")
        except Exception as e:
            print(f"ロググループの削除中にエラーが発生しました: {e}")
    else:
        print("\n=== クリーンアップはスキップされました ===")
        print("CLEAN_UP = False に設定されているため、リソースは削除されません")

if __name__ == "__main__":
    main()
