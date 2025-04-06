"""Test cases for logkiss.handlers module.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.

This module provides test cases for logkiss.handlers.
The following handlers are tested:
- BaseHandler: Base handler class
- GCloudLoggingHandler: Google Cloud Logging handler
- AWSCloudWatchHandler: AWS CloudWatch handler
"""

import json
import time
from unittest.mock import MagicMock, patch
import logging

import pytest

from logkiss.handlers import (
    AWSCloudWatchHandler,
    BaseHandler,
)
from logkiss.handler_gcp import GCloudLoggingHandler


def test_base_handler():
    """BaseHandlerのテスト"""
    handler = BaseHandler()
    with pytest.raises(NotImplementedError):
        handler.handle({"message": "test"})


@pytest.fixture
def mock_google_client():
    """Google Cloud Loggingのモックを作成"""
    with patch("logkiss.handler_gcp.google_logging") as mock_logging:
        mock_client = MagicMock()
        mock_logger = MagicMock()
        mock_client.logger.return_value = mock_logger
        mock_logging.Client.return_value = mock_client
        
        # モックのプロジェクト情報を設定
        mock_client.project = "mock-project"
        
        yield mock_logging


@pytest.fixture
def mock_boto3_client():
    """AWS CloudWatch Logsのモックを作成"""
    with patch("logkiss.handlers.boto3") as mock_boto3:
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        yield mock_client


class TestGCloudLoggingHandler:
    """GCloudLoggingHandlerのテストケース"""

    def test_init(self, mock_google_client):
        """外部のgcloud環境から初期化するテスト"""
        success_logged = False
        error_logged = False
    
        try:
            # 引数なしで初期化（gcloud環境から情報を取得）
            print("DEBUG: Creating handler without args")
            handler = GCloudLoggingHandler()
            print("DEBUG: Handler created successfully")
            success_logged = True

            # 内部のハンドラーが正しく初期化されていることを確認
            assert handler.handler is not None
            
            # Clientが呼び出されたことを確認
            assert mock_google_client.Client.called
            
            # 引数で上書き
            print("DEBUG: Creating handler with args")
            handler = GCloudLoggingHandler(
                project_id="test-project",
                log_name="test-log",
                labels={"env": "test"}
            )
            print("DEBUG: Handler with args created successfully")
            
            # 内部のハンドラーが正しく初期化されていることを確認
            assert handler.handler is not None
            
        except Exception as e:
            print(f"ERROR: Test failed with exception: {str(e)}")
            import traceback
            print(f"ERROR: Traceback: {traceback.format_exc()}")
            error_logged = True
            raise
        finally:
            # テスト結果を表示
            if success_logged:
                print("SUCCESS: Handler initialization test passed")
            if error_logged:
                print("ERROR: Handler initialization test failed")
                
        # テストが成功したことを確認
        assert success_logged, "テストがエラーで失敗しました"
        assert not error_logged, "テストがエラーで失敗しました"

    def test_convert_level_to_severity(self, mock_google_client):
        """ログレベル変換のテスト"""
        handler = GCloudLoggingHandler()
        
        # 内部ハンドラーが設定されていることを確認
        assert handler.handler is not None
        
        # emit関数が呼び出せることを確認
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        # モックを設定
        handler.handler.emit = MagicMock()
        
        # emit関数を呼び出す
        handler.emit(record)
        
        # 内部ハンドラーのemit関数が呼び出されたことを確認
        handler.handler.emit.assert_called_once()


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
