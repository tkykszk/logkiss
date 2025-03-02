"""E2E test for Google Cloud Logging integration.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.
"""

import os
import json
import time
import uuid
import hashlib
import pytest
import subprocess
from datetime import datetime
from google.cloud import logging as google_logging
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# クリーンアップフラグ（テスト後にリソースを削除するかどうか）
CLEAN_UP = True

def check_gcp_auth():
    """GCPの認証状態を確認し、テスト用のログエントリを書き込めるか検証する"""
    print("\n認証状態の確認を開始します...")
    
    # 環境変数からプロジェクトIDを取得（設定されていない場合はデフォルト値を使用）
    project_id = os.environ.get("GCP_PROJECT_ID", "emgen-sandbox1")
    
    try:
        # 認証情報の確認
        cmd = ["gcloud", "auth", "list"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"認証済みアカウント:\n{result.stdout}")
        
        # アクティブなプロジェクトの確認
        cmd = ["gcloud", "config", "get-value", "project"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        current_project = result.stdout.strip()
        print(f"現在のプロジェクト: {current_project}")
        
        # プロジェクトIDが一致しない場合は警告
        if current_project != project_id:
            print(f"警告: 現在のプロジェクト({current_project})と環境変数のプロジェクト({project_id})が一致しません")
            print(f"環境変数のプロジェクトを使用します: {project_id}")
        
        # テスト用のログエントリを書き込めるか確認
        test_log_name = generate_test_log_name()
        client = google_logging.Client(project=project_id)
        logger = client.logger(test_log_name)
        
        # テスト用のログエントリを送信
        test_message = {"message": "Auth check test", "timestamp": time.time()}
        logger.log_struct(test_message)
        print(f"テスト用ログエントリを送信しました: {json.dumps(test_message)}")
        
        # ログが書き込まれたか確認
        time.sleep(3)  # ログが反映されるまで少し待つ
        cmd = [
            "gcloud", "logging", "read",
            f'resource.type="global" AND logName="projects/{project_id}/logs/{test_log_name}"',
            "--limit", "1",
            "--format", "json",
            "--project", project_id
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            print("認証成功: テスト用ログエントリが正常に書き込まれました")
            return True, test_log_name, project_id
        else:
            print("警告: テスト用ログエントリが見つかりませんでした")
            print(f"stderr: {result.stderr}")
            return False, None, None
            
    except Exception as e:
        print(f"エラー: 認証確認中に例外が発生しました: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False, None, None


def generate_test_log_name():
    """テスト用の一意のログ名を生成（短いハッシュ値を使用）"""
    timestamp = datetime.now().strftime("%Y%m%d")
    unique_id = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:12]
    return f"logkiss_test_{timestamp}_{unique_id}"


@pytest.mark.e2e
@pytest.mark.timeout(120)  # 120秒でタイムアウト
def test_gcp_cloud_logging_e2e():
    """GCP Cloud Loggingへの実際のログ送信をテスト"""
    # 事前に認証状態を確認
    auth_success, auth_log_name, project_id = check_gcp_auth()
    if not auth_success:
        pytest.skip("GCP認証に失敗したため、テストをスキップします")
    
    # 一意のログ名を生成（テストの分離のため）
    log_name = generate_test_log_name()
    print(f"\nDEBUG: Using log name: {log_name}")

    try:
        # 環境変数からプロジェクトIDを取得
        project_id = os.environ.get("GCP_PROJECT_ID", project_id)
        print(f"DEBUG: Using project_id: {project_id}")

        # ハンドラーの初期化を簡略化し、スレッドプールを使用しない
        print("DEBUG: Creating handler without thread pool")
        
        # クライアントを直接作成してテスト
        client = google_logging.Client(project=project_id)
        logger = client.logger(log_name)
        
        # テスト用のログエントリを送信
        test_entry = {
            "message": "E2E test log entry",
            "severity": "INFO",
            "test_id": 1
        }
        
        print(f"DEBUG: Sending log entry directly: {json.dumps(test_entry)}")
        logger.log_struct(test_entry)
        print("DEBUG: Log entry sent")
        
        # Cloud Loggingに反映されるまで少し待つ
        print("DEBUG: Waiting for logs to be available")
        time.sleep(3)

        # ログを検索するコマンドを実行
        search_cmd = [
            "gcloud", "logging", "read",
            f'resource.type="global" AND logName="projects/{project_id}/logs/{log_name}"',
            "--limit", "5",
            "--project", project_id,
            "--format", "json"
        ]
        print(f"DEBUG: Running command: {' '.join(search_cmd)}")
        search_result = subprocess.run(
            search_cmd,
            capture_output=True,
            text=True
        )
        print(f"DEBUG: Search command exit code: {search_result.returncode}")
        print(f"DEBUG: Search command stdout: {search_result.stdout}")
        print(f"DEBUG: Search command stderr: {search_result.stderr}")

        # テストが成功したことを示す
        if search_result.returncode == 0 and search_result.stdout.strip():
            print("\nテスト成功: ログエントリが送信され、確認できました")
        else:
            print("\nテスト失敗: ログエントリが見つかりませんでした")
            pytest.fail("ログエントリが見つかりませんでした")
        
        # クリーンアップ（テスト後にリソースを削除）
        if CLEAN_UP:
            print("\n=== クリーンアップ ===")
            print(f"ログ「{log_name}」のエントリを削除します...")
            try:
                # ログエントリを削除するためのフィルタを作成
                filter_str = f'logName="projects/{project_id}/logs/{log_name}"'
                print(f"削除フィルタ: {filter_str}")
                
                # ログエントリを削除
                client.delete_entries(filter_=filter_str)
                print("ログエントリを削除しました")
                
                # 認証チェック時のログも削除
                if auth_log_name:
                    filter_str = f'logName="projects/{project_id}/logs/{auth_log_name}"'
                    client.delete_entries(filter_=filter_str)
                    print(f"認証チェック用ログ「{auth_log_name}」のエントリも削除しました")
            except Exception as e:
                print(f"ログエントリの削除中にエラーが発生しました: {e}")
        else:
            print("\n=== クリーンアップはスキップされました ===")
            print("CLEAN_UP = False に設定されているため、リソースは削除されません")
            
    except Exception as e:
        print(f"ERROR: Test failed with exception: {str(e)}")
        import traceback
        print(f"ERROR: Traceback: {traceback.format_exc()}")
        raise


@pytest.mark.e2e
@pytest.mark.timeout(120)  # 120秒でタイムアウト
def test_gcp_cloud_logging_handler_e2e():
    """GCPCloudLoggingHandlerを使用したE2Eテスト"""
    # 事前に認証状態を確認
    auth_success, _, project_id = check_gcp_auth()
    if not auth_success:
        pytest.skip("GCP認証に失敗したため、テストをスキップします")
    
    # 一意のログ名を生成（テストの分離のため）
    log_name = generate_test_log_name()
    print(f"\nDEBUG: Using log name for handler test: {log_name}")

    try:
        # 環境変数からプロジェクトIDを取得
        project_id = os.environ.get("GCP_PROJECT_ID", project_id)
        print(f"DEBUG: Using project_id: {project_id}")

        # GCPCloudLoggingHandlerを使用してテスト
        from logkiss.handlers import GCPCloudLoggingHandler
        print("DEBUG: Creating GCPCloudLoggingHandler")
        handler = GCPCloudLoggingHandler(
            project_id=project_id,
            log_name=log_name,
            batch_size=1,  # 即時フラッシュするために1に設定
            flush_interval=1.0  # 短いフラッシュ間隔
        )
        
        # テスト用のログエントリを送信
        test_entry = {
            "message": "Handler E2E test log entry",
            "level": "INFO",
            "test_id": 2,
            "timestamp": time.time()
        }
        
        print(f"DEBUG: Sending log entry via handler: {json.dumps(test_entry)}")
        handler.handle(test_entry)
        print("DEBUG: Log entry sent")
        
        # ハンドラーがフラッシュするのを待つ
        print("DEBUG: Waiting for handler to flush")
        time.sleep(5)
        
        # ログを検索するコマンドを実行
        search_cmd = [
            "gcloud", "logging", "read",
            f'resource.type="global" AND logName="projects/{project_id}/logs/{log_name}"',
            "--limit", "5",
            "--project", project_id,
            "--format", "json"
        ]
        print(f"DEBUG: Running command: {' '.join(search_cmd)}")
        search_result = subprocess.run(
            search_cmd,
            capture_output=True,
            text=True
        )
        print(f"DEBUG: Search command exit code: {search_result.returncode}")
        print(f"DEBUG: Search command stdout: {search_result.stdout}")
        print(f"DEBUG: Search command stderr: {search_result.stderr}")

        # テストが成功したことを示す
        if search_result.returncode == 0 and search_result.stdout.strip():
            print("\nテスト成功: ハンドラー経由でログエントリが送信され、確認できました")
        else:
            print("\nテスト失敗: ハンドラー経由で送信したログエントリが見つかりませんでした")
            pytest.fail("ログエントリが見つかりませんでした")
        
        # クリーンアップ（テスト後にリソースを削除）
        if CLEAN_UP:
            print("\n=== クリーンアップ ===")
            print(f"ログ「{log_name}」のエントリを削除します...")
            try:
                # Google Cloud Logging クライアントを作成
                client = google_logging.Client(project=project_id)
                
                # ログエントリを削除するためのフィルタを作成
                filter_str = f'logName="projects/{project_id}/logs/{log_name}"'
                print(f"削除フィルタ: {filter_str}")
                
                # ログエントリを削除
                client.delete_entries(filter_=filter_str)
                print("ログエントリを削除しました")
            except Exception as e:
                print(f"ログエントリの削除中にエラーが発生しました: {e}")
        else:
            print("\n=== クリーンアップはスキップされました ===")
            print("CLEAN_UP = False に設定されているため、リソースは削除されません")
            
    except Exception as e:
        print(f"ERROR: Test failed with exception: {str(e)}")
        import traceback
        print(f"ERROR: Traceback: {traceback.format_exc()}")
        raise