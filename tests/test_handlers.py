"""Test cases for logkiss.handlers module.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.

This module provides test cases for logkiss.handlers.
The following handlers are tested:
- BaseHandler: Base handler class
- GCPCloudLoggingHandler: Google Cloud Logging handler
- AWSCloudWatchHandler: AWS CloudWatch handler
"""

import json
import time
from unittest.mock import MagicMock, patch

import pytest

from logkiss.handlers import (
    AWSCloudWatchHandler,
    BaseHandler,
    GCPCloudLoggingHandler,
)


def test_base_handler():
    """BaseHandlerのテスト"""
    handler = BaseHandler()
    with pytest.raises(NotImplementedError):
        handler.handle({"message": "test"})


@pytest.fixture
def mock_google_client():
    """Google Cloud Loggingのモックを作成"""
    with patch("logkiss.handlers.google_logging") as mock_logging:
        mock_client = MagicMock()
        mock_logger = MagicMock()
        mock_client.logger.return_value = mock_logger
        mock_logging.Client.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_boto3_client():
    """AWS CloudWatch Logsのモックを作成"""
    with patch("logkiss.handlers.boto3") as mock_boto3:
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        yield mock_client


class TestGCPCloudLoggingHandler:
    """GCPCloudLoggingHandlerのテストケース"""

    def test_init(self, mock_google_client):
        """外部のgcloud環境から初期化するテスト"""
        success_logged = False
        error_logged = False
        
        try:
            # モックのプロジェクト情報を設定
            mock_project = "gcloud-project"
            mock_google_client.project = mock_project

            print("DEBUG: Setting up mock project:", mock_project)
            print("DEBUG: Mock client:", mock_google_client)
            print("DEBUG: Mock client project:", getattr(mock_google_client, 'project', None))

            # 引数なしで初期化（gcloud環境から情報を取得）
            print("DEBUG: Creating handler without args")
            handler = GCPCloudLoggingHandler()
            print("DEBUG: Handler created successfully")
            success_logged = True

            print("DEBUG: Handler project_id:", getattr(handler, 'project_id', None))
            print("DEBUG: Handler client:", handler.client)
            print("DEBUG: Handler client project:", getattr(handler.client, 'project', None))

            print("DEBUG: Running first assertions")
            assert mock_project == getattr(handler.client, 'project', None), "Client project mismatch"
            assert handler.project_id == mock_project, "Project ID mismatch"
            assert handler.resource == {"type": "global"}, "Resource mismatch"
            assert handler._batch_size == 100, "Batch size mismatch"
            assert handler._flush_interval == 5.0, "Flush interval mismatch"
            print("DEBUG: First assertions passed")

            # 引数で上書き
            print("DEBUG: Creating handler with args")
            handler = GCPCloudLoggingHandler(
                project_id="test-project",
                log_name="test-log",
                labels={"env": "test"}
            )
            print("DEBUG: Handler created with args successfully")
            success_logged = True

            print("DEBUG: Handler project_id:", getattr(handler, 'project_id', None))
            print("DEBUG: Running second assertions")
            assert handler.project_id == "test-project", "Project ID override failed"
            assert handler.labels == {"env": "test"}, "Labels override failed"
            print("DEBUG: Second assertions passed")

        except Exception as e:
            print("ERROR: Test failed with exception:", str(e))
            error_logged = True
            import traceback
            print("ERROR: Traceback:", traceback.format_exc())
            raise
        finally:
            # 明示的にスレッドを停止
            if 'handler' in locals():
                print("DEBUG: Shutting down thread")
                handler._running = False
                if hasattr(handler, '_flush_thread') and handler._flush_thread is not None:
                    if handler._flush_thread.is_alive():
                        handler._flush_thread.join(timeout=1.0)
                print("DEBUG: Thread shutdown completed")

            # ログに基づいて判定
            if not success_logged and not error_logged:
                raise TimeoutError("テストが応答を返しませんでした")
            elif error_logged:
                raise AssertionError("テストがエラーで失敗しました")

    def test_convert_level_to_severity(self, mock_google_client):
        """ログレベル変換のテスト"""
        handler = GCPCloudLoggingHandler()
        assert handler._convert_level_to_severity("DEBUG") == "DEBUG"
        assert handler._convert_level_to_severity("INFO") == "INFO"
        assert handler._convert_level_to_severity("WARNING") == "WARNING"
        assert handler._convert_level_to_severity("ERROR") == "ERROR"
        assert handler._convert_level_to_severity("CRITICAL") == "CRITICAL"
        assert handler._convert_level_to_severity("UNKNOWN") == "DEFAULT"


class TestAWSCloudWatchHandler:
    """AWSCloudWatchHandlerのテストケース"""

    def test_init(self, mock_boto3_client):
        """初期化のテスト"""
        handler = AWSCloudWatchHandler(
            log_group_name="test-group",
            log_stream_name="test-stream",
            region_name="us-west-2"
        )
        assert handler.log_group_name == "test-group"
        assert handler.log_stream_name == "test-stream"
        mock_boto3_client.create_log_group.assert_called_once_with(
            logGroupName="test-group"
        )
        mock_boto3_client.create_log_stream.assert_called_once_with(
            logGroupName="test-group",
            logStreamName="test-stream"
        )

    def test_auto_log_stream_name(self, mock_boto3_client):
        """ログストリーム名の自動生成テスト"""
        with patch("socket.gethostname", return_value="test-host"):
            handler = AWSCloudWatchHandler(log_group_name="test-group")
            assert handler.log_stream_name == "test-host"

    # def test_handle_and_flush(self, mock_boto3_client):
    #     """ハンドルとフラッシュのテスト"""
    #     # 定期的なフラッシュを無効化
    #     with patch.object(AWSCloudWatchHandler, '_start_periodic_flush'):
    #         handler = AWSCloudWatchHandler(
    #             log_group_name="test-group",
    #             log_stream_name="test-stream",
    #             batch_size=2
    #         )
            
    #         # シーケンストークンをセットアップ
    #         mock_boto3_client.put_log_events.return_value = {
    #             "nextSequenceToken": "token123"
    #         }
            
    #         # 1つ目のログ - バッチに追加されるだけ
    #         timestamp1 = int(time.time() * 1000)
    #         log_entry1 = {
    #             "level": "INFO",
    #             "message": "test1",
    #             "timestamp": timestamp1 / 1000,
    #             "extra": {"tag": "test"}
    #         }
    #         handler.handle(log_entry1)
    #         assert len(handler._batch) == 1
    #         mock_boto3_client.put_log_events.assert_not_called()
            
    #         # 2つ目のログ - バッチサイズに達したのでフラッシュされる
    #         timestamp2 = int(time.time() * 1000)
    #         log_entry2 = {
    #             "level": "ERROR",
    #             "message": "test2",
    #             "timestamp": timestamp2 / 1000
    #         }
    #         handler.handle(log_entry2)
    #         assert len(handler._batch) == 0
            
    #         # フラッシュされたイベントを確認
    #         mock_boto3_client.put_log_events.assert_called_once()
    #         call_args = mock_boto3_client.put_log_events.call_args[1]
    #         assert call_args["logGroupName"] == "test-group"
    #         assert call_args["logStreamName"] == "test-stream"
    #         assert len(call_args["logEvents"]) == 2
            
    #         events = sorted(call_args["logEvents"], key=lambda x: x["timestamp"])
    #         assert events[0]["timestamp"] == timestamp1
    #         assert events[0]["message"] == json.dumps(log_entry1)
    #         assert events[1]["timestamp"] == timestamp2
    #         assert events[1]["message"] == json.dumps(log_entry2)
            
    #         # 次のフラッシュではシーケンストークンが使用される
    #         handler.handle(log_entry1)
    #         handler.handle(log_entry2)
    #         call_args = mock_boto3_client.put_log_events.call_args[1]
    #         assert call_args["sequenceToken"] == "token123"

    #         # 明示的にExecutorをシャットダウン
    #         handler._executor.shutdown(wait=True)
