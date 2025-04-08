"""
AWS CloudWatch Logsハンドラーのモックテスト

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
"""

import pytest
import logging
import json
from unittest import mock
from datetime import datetime

from logkiss.handlers import AWSCloudWatchHandler


@pytest.fixture
def mock_boto3_client():
    """Create a mocked boto3 client."""
    with mock.patch('boto3.client') as mock_client:
        # モック済みのクライアントインスタンスを作成
        mock_logs = mock.MagicMock()
        
        # クライアントファクトリがモックロガーを返すように設定
        mock_client.return_value = mock_logs
        
        yield mock_logs


def test_aws_cloudwatch_logs_handler_init():
    """AWSCloudWatchHandlerの初期化をテスト"""
    with mock.patch('boto3.client') as mock_client:
        # ハンドラーを初期化
        handler = AWSCloudWatchHandler(
            log_group_name="test-group",
            log_stream_name="test-stream",
            aws_access_key_id="test-key",
            aws_secret_access_key="test-secret",
            region_name="us-west-2"
        )
        
        # boto3.clientが正しいパラメータで呼び出されたか確認
        mock_client.assert_called_once_with(
            'logs',
            aws_access_key_id="test-key",
            aws_secret_access_key="test-secret",
            region_name="us-west-2"
        )
        
        # ハンドラーの属性が正しく設定されていることを確認
        assert handler.log_group_name == "test-group"
        assert handler.log_stream_name == "test-stream"
        assert handler.batch_size == 100  # デフォルト値
        assert handler.flush_interval == 5.0  # デフォルト値


def test_aws_cloudwatch_logs_handler_emit(mock_boto3_client):
    """AWSCloudWatchHandlerのログ出力をテスト"""
    handler = AWSCloudWatchHandler(
        log_group_name="test-group",
        log_stream_name="test-stream"
    )
    
    # テスト用のLogRecordを作成
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_aws_handler_mock.py",
        lineno=123,
        msg="Test log message",
        args=(),
        exc_info=None
    )
    
    # ハンドラーにレコードを送信
    handler.emit(record)
    
    # バッファにメッセージが追加されたか確認
    assert len(handler.buffer) == 1
    log_event = handler.buffer[0]
    assert 'timestamp' in log_event
    assert 'message' in log_event
    
    # メッセージの内容を確認
    message_json = json.loads(log_event['message'])
    assert message_json['level'] == 'INFO'
    assert message_json['message'] == 'Test log message'
    assert message_json['logger'] == 'test_logger'


def test_aws_cloudwatch_logs_handler_flush(mock_boto3_client):
    """AWSCloudWatchHandlerのバッファフラッシュをテスト"""
    handler = AWSCloudWatchHandler(
        log_group_name="test-group",
        log_stream_name="test-stream",
        batch_size=2  # テスト用に小さい値に設定
    )
    
    # テスト用にログイベントをバッファに追加
    handler.buffer = [
        {'timestamp': int(datetime.now().timestamp() * 1000), 'message': '{"msg":"テストメッセージ1"}'},
        {'timestamp': int(datetime.now().timestamp() * 1000), 'message': '{"msg":"テストメッセージ2"}'}
    ]
    
    # フラッシュを実行
    handler.flush()
    
    # CloudWatchにログが送信されたか確認
    mock_boto3_client.put_log_events.assert_called_once()
    
    # バッファがクリアされたか確認
    assert len(handler.buffer) == 0
