"""
AWS CloudWatch Logs E2E テスト

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
"""

import os
import json
import time
import uuid
import hashlib
import pytest
import subprocess
from datetime import datetime
import boto3
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

from logkiss.handlers import AWSCloudWatchHandler

# クリーンアップフラグ（テスト後にリソースを削除するかどうか）
CLEAN_UP = True


def generate_test_log_group_name():
    """テスト用の一意のロググループ名を生成（短いハッシュ値を使用）"""
    timestamp = datetime.now().strftime("%Y%m%d")
    unique_id = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:12]
    return f"logkiss-test-{timestamp}-{unique_id}"


def check_aws_auth():
    """AWSの認証状態を確認し、テスト用のログエントリを書き込めるか検証する"""
    print("\n認証状態の確認を開始します...")

    # 環境変数からAWS設定を取得
    aws_profile = os.environ.get("AWS_PROFILE")
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

    # 認証情報が設定されていない場合はスキップ
    if not aws_profile and not os.environ.get("AWS_ACCESS_KEY_ID"):
        print("警告: AWS認証情報が設定されていません。テストをスキップします。")
        return False, None

    try:
        # 認証情報の確認
        cmd = ["aws", "sts", "get-caller-identity", "--profile", aws_profile]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            identity = json.loads(result.stdout)
            print(f"認証済みアカウント: {identity.get('Arn')}")
            print(f"アカウントID: {identity.get('Account')}")
        else:
            print(f"認証エラー: {result.stderr}")
            return False

        # テスト用のロググループとストリームを作成
        test_log_group = generate_test_log_group_name()
        test_log_stream = f"auth-check-{datetime.now().strftime('%H%M%S')}"

        # boto3クライアントを作成
        logs_client = boto3.client("logs", region_name=aws_region)

        # ロググループとストリームを作成
        try:
            logs_client.create_log_group(logGroupName=test_log_group)
            print(f"ロググループを作成しました: {test_log_group}")
        except logs_client.exceptions.ResourceAlreadyExistsException:
            print(f"ロググループは既に存在します: {test_log_group}")

        try:
            logs_client.create_log_stream(logGroupName=test_log_group, logStreamName=test_log_stream)
            print(f"ログストリームを作成しました: {test_log_stream}")
        except logs_client.exceptions.ResourceAlreadyExistsException:
            print(f"ログストリームは既に存在します: {test_log_stream}")

        # テスト用のログエントリを送信
        test_message = {"message": "Auth check test", "timestamp": time.time()}
        logs_client.put_log_events(
            logGroupName=test_log_group,
            logStreamName=test_log_stream,
            logEvents=[{"timestamp": int(time.time() * 1000), "message": json.dumps(test_message)}],
        )
        print(f"テスト用ログエントリを送信しました: {json.dumps(test_message)}")

        # ログが書き込まれたか確認
        time.sleep(3)  # ログが反映されるまで少し待つ
        cmd = [
            "aws",
            "logs",
            "get-log-events",
            "--log-group-name",
            test_log_group,
            "--log-stream-name",
            test_log_stream,
            "--limit",
            "5",
            "--profile",
            aws_profile,
            "--region",
            aws_region,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0 and "events" in result.stdout:
            print("認証成功: テスト用ログエントリが正常に書き込まれました")
            return True, test_log_group
        else:
            print("警告: テスト用ログエントリが見つかりませんでした")
            print(f"stderr: {result.stderr}")
            return False, None

    except Exception as e:
        print(f"エラー: 認証確認中に例外が発生しました: {str(e)}")
        import traceback

        print(traceback.format_exc())
        return False, None


def generate_unique_log_name():
    """一意のログ名を生成"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"logkiss-test-{timestamp}-{unique_id}"


@pytest.mark.e2e
@pytest.mark.aws
@pytest.mark.timeout(120)  # 120秒でタイムアウト
def test_aws_cloudwatch_logs_e2e():
    """AWS CloudWatch Logsへの実際のログ送信をテスト"""
    # 事前に認証状態を確認
    auth_success, test_log_group = check_aws_auth()
    if not auth_success:
        pytest.skip("AWS認証に失敗したため、テストをスキップします")

    # 環境変数からAWS設定を取得
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

    # テスト用のログストリーム名を生成
    log_stream_name = f"e2e-test-{datetime.now().strftime('%H%M%S')}-{str(uuid.uuid4())[:8]}"
    print(f"\nDEBUG: Using log stream: {log_stream_name}")

    try:
        # boto3クライアントを直接使用してテスト
        print("DEBUG: Creating logs client")
        logs_client = boto3.client("logs", region_name=aws_region)

        # ログストリームを作成
        try:
            logs_client.create_log_stream(logGroupName=test_log_group, logStreamName=log_stream_name)
            print(f"DEBUG: Created log stream: {log_stream_name}")
        except logs_client.exceptions.ResourceAlreadyExistsException:
            print(f"DEBUG: Log stream already exists: {log_stream_name}")

        # テスト用のログエントリを送信
        test_entry = {"message": "E2E test log entry", "level": "INFO", "test_id": 1, "timestamp": time.time()}

        print(f"DEBUG: Sending log entry directly: {json.dumps(test_entry)}")
        logs_client.put_log_events(
            logGroupName=test_log_group,
            logStreamName=log_stream_name,
            logEvents=[{"timestamp": int(test_entry["timestamp"] * 1000), "message": json.dumps(test_entry)}],
        )
        print("DEBUG: Log entry sent")

        # CloudWatch Logsに反映されるまで少し待つ
        print("DEBUG: Waiting for logs to be available")
        time.sleep(3)

        # ログを検索するコマンドを実行
        search_cmd = [
            "aws",
            "logs",
            "get-log-events",
            "--log-group-name",
            test_log_group,
            "--log-stream-name",
            log_stream_name,
            "--limit",
            "5",
            "--region",
            aws_region,
        ]
        print(f"DEBUG: Running command: {' '.join(search_cmd)}")
        search_result = subprocess.run(search_cmd, capture_output=True, text=True)
        print(f"DEBUG: Search command exit code: {search_result.returncode}")
        print(f"DEBUG: Search command stdout: {search_result.stdout}")
        print(f"DEBUG: Search command stderr: {search_result.stderr}")

        # テストが成功したことを示す
        if search_result.returncode == 0 and "events" in search_result.stdout:
            print("\nテスト成功: ログエントリが送信され、確認できました")

            # 結果をJSONとしてパース
            result_json = json.loads(search_result.stdout)
            events = result_json.get("events", [])

            if events:
                print("\n取得したログエントリ:")
                for event in events:
                    print(f"タイムスタンプ: {datetime.fromtimestamp(event['timestamp']/1000).isoformat()}")
                    print(f"メッセージ: {event['message']}")
                    print("---")
        else:
            print("\nテスト失敗: ログエントリが見つかりませんでした")
            pytest.fail("ログエントリが見つかりませんでした")

        # クリーンアップ（テスト後にリソースを削除）
        if CLEAN_UP:
            print("\n=== クリーンアップ ===")
            print(f"ロググループ「{test_log_group}」を削除します...")
            try:
                logs_client.delete_log_group(logGroupName=test_log_group)
                print("ロググループを削除しました")
            except Exception as e:
                print(f"ロググループの削除中にエラーが発生しました: {e}")
        else:
            print("\n=== クリーンアップはスキップされました ===")
            print("CLEAN_UP = False に設定されているため、リソースは削除されません")

    except Exception as e:
        print(f"ERROR: Test failed with exception: {str(e)}")
        import traceback

        print(f"ERROR: Traceback: {traceback.format_exc()}")
        raise


@pytest.mark.e2e
@pytest.mark.aws
@pytest.mark.timeout(120)  # 120秒でタイムアウト
def test_aws_cloudwatch_logs_handler_e2e():
    """AWSCloudWatchHandlerを使用したE2Eテスト"""
    # 事前に認証状態を確認
    auth_success, _ = check_aws_auth()
    if not auth_success:
        pytest.skip("AWS認証に失敗したため、テストをスキップします")

    # 環境変数からAWS設定を取得
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

    # テスト用のロググループとストリーム名を生成
    log_group_name = generate_test_log_group_name()
    log_stream_name = f"handler-test-{datetime.now().strftime('%H%M%S')}"
    print(f"\nDEBUG: Using log group: {log_group_name}")
    print(f"DEBUG: Using log stream: {log_stream_name}")

    try:
        # AWSCloudWatchHandlerを使用してテスト
        print("DEBUG: Creating AWSCloudWatchHandler")
        handler = AWSCloudWatchHandler(
            log_group_name=log_group_name,
            log_stream_name=log_stream_name,
            region_name=aws_region,
            batch_size=1,  # 即時フラッシュするために1に設定
            flush_interval=1.0,  # 短いフラッシュ間隔
        )

        # テスト用のログエントリを送信
        test_entry = {"message": "Handler E2E test log entry", "level": "INFO", "test_id": 2, "timestamp": time.time()}

        print(f"DEBUG: Sending log entry via handler: {json.dumps(test_entry)}")
        handler.handle(test_entry)
        print("DEBUG: Log entry sent")

        # ハンドラーがフラッシュするのを待つ
        print("DEBUG: Waiting for handler to flush")
        time.sleep(5)

        # ログを検索するコマンドを実行
        search_cmd = [
            "aws",
            "logs",
            "get-log-events",
            "--log-group-name",
            log_group_name,
            "--log-stream-name",
            log_stream_name,
            "--limit",
            "5",
            "--region",
            aws_region,
        ]
        print(f"DEBUG: Running command: {' '.join(search_cmd)}")
        search_result = subprocess.run(search_cmd, capture_output=True, text=True)
        print(f"DEBUG: Search command exit code: {search_result.returncode}")
        print(f"DEBUG: Search command stdout: {search_result.stdout}")
        print(f"DEBUG: Search command stderr: {search_result.stderr}")

        # テストが成功したことを示す
        if search_result.returncode == 0 and "events" in search_result.stdout:
            print("\nテスト成功: ハンドラー経由でログエントリが送信され、確認できました")

            # 結果をJSONとしてパース
            result_json = json.loads(search_result.stdout)
            events = result_json.get("events", [])

            if events:
                print("\n取得したログエントリ:")
                for event in events:
                    print(f"タイムスタンプ: {datetime.fromtimestamp(event['timestamp']/1000).isoformat()}")
                    print(f"メッセージ: {event['message']}")
                    print("---")
        else:
            print("\nテスト失敗: ハンドラー経由で送信したログエントリが見つかりませんでした")
            pytest.fail("ログエントリが見つかりませんでした")

        # クリーンアップ（テスト後にリソースを削除）
        if CLEAN_UP:
            print("\n=== クリーンアップ ===")
            print(f"ロググループ「{log_group_name}」を削除します...")
            try:
                logs_client = boto3.client("logs", region_name=aws_region)
                logs_client.delete_log_group(logGroupName=log_group_name)
                print("ロググループを削除しました")
            except Exception as e:
                print(f"ロググループの削除中にエラーが発生しました: {e}")
        else:
            print("\n=== クリーンアップはスキップされました ===")
            print("CLEAN_UP = False に設定されているため、リソースは削除されません")

    except Exception as e:
        print(f"ERROR: Test failed with exception: {str(e)}")
        import traceback

        print(f"ERROR: Traceback: {traceback.format_exc()}")
        raise
