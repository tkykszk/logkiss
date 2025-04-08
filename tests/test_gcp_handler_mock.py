"""
Google Cloud Loggingハンドラーのモックテスト

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
"""

import pytest
import logging
import json
from unittest import mock
from datetime import datetime

from logkiss.handler_gcp import GCloudLoggingHandler


@pytest.fixture
def mock_gcp_client():
    """Create a mocked Google Cloud Logging client."""
    with mock.patch('google.cloud.logging.Client') as mock_client:
        # モック済みのロガーインスタンスを作成
        mock_logger = mock.MagicMock()
        
        # クライアントインスタンスがモックロガーを返すように設定
        mock_client_instance = mock.MagicMock()
        mock_client_instance.logger.return_value = mock_logger
        mock_client.return_value = mock_client_instance
        
        yield mock_logger


def test_gcp_logging_handler_init():
    """GCloudLoggingHandlerの初期化をテスト"""
    with mock.patch('google.cloud.logging.Client') as mock_client:
        # クライアントインスタンスのモックを設定
        mock_client_instance = mock.MagicMock()
        mock_client.return_value = mock_client_instance
        
        # ハンドラーを初期化
        handler = GCloudLoggingHandler(
            project_id="test-project",
            log_name="test-log"
        )
        
        # Google Cloud Logging Clientが正しいパラメータで呼び出されたか確認
        mock_client.assert_called_once_with(project="test-project")
        
        # ハンドラーの属性が正しく設定されていることを確認
        assert handler.log_name == "test-log"
        assert handler.resource is None  # デフォルト値
        
        # ロガーが取得されたか確認
        mock_client_instance.logger.assert_called_once_with("test-log")


def test_gcp_logging_handler_emit(mock_gcp_client):
    """GCloudLoggingHandlerのログ出力をテスト"""
    handler = GCloudLoggingHandler(
        project_id="test-project",
        log_name="test-log"
    )
    
    # テスト用のLogRecordを作成
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_gcp_handler_mock.py",
        lineno=123,
        msg="Test log message",
        args=(),
        exc_info=None
    )
    
    # extra情報を追加（json_fieldsを使用して構造化ログをテスト）
    record.__dict__['json_fields'] = {
        "test_id": 123,
        "timestamp": datetime.now().timestamp()
    }
    
    # ハンドラーにレコードを送信
    handler.emit(record)
    
    # メッセージが送信されたか確認
    mock_gcp_client.log_struct.assert_called_once()
    
    # 呼び出し引数を取得
    call_args = mock_gcp_client.log_struct.call_args[0][0]
    
    # 基本フィールドを確認
    assert call_args['message'] == 'Test log message'
    assert call_args['severity'] == 'INFO'
    assert call_args['logger'] == 'test_logger'
    
    # 追加フィールドを確認
    assert 'test_id' in call_args
    assert call_args['test_id'] == 123
    assert 'timestamp' in call_args


def test_gcp_logging_handler_with_resource():
    """リソース指定付きのGCloudLoggingHandlerをテスト"""
    with mock.patch('google.cloud.logging.Client') as mock_client:
        # クライアントインスタンスのモックを設定
        mock_client_instance = mock.MagicMock()
        mock_client.return_value = mock_client_instance
        
        # カスタムリソースを設定
        resource = {"type": "global"}
        
        # ハンドラーを初期化（リソース指定付き）
        handler = GCloudLoggingHandler(
            project_id="test-project",
            log_name="test-log",
            resource=resource
        )
        
        # リソースが正しく設定されていることを確認
        assert handler.resource == resource
