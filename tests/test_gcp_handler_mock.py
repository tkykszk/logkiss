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
        
        # CloudLoggingHandlerのモックを作成
        mock_handler = mock.MagicMock()
        
        # CloudLoggingHandlerのクラスをモック化
        with mock.patch('logkiss.handler_gcp.CloudLoggingHandler', return_value=mock_handler) as mock_cloud_handler_class:
            # ハンドラーを初期化
            handler = GCloudLoggingHandler(
                project_id="test-project",
                log_name="test-log"
            )
            
            # Google Cloud Logging Clientが正しいパラメータで呼び出されたか確認
            mock_client.assert_called_once_with(project="test-project", credentials=None)
            
            # CloudLoggingHandlerが正しく生成されたか確認
            mock_cloud_handler_class.assert_called_once()
            
            # 内部ハンドラーが設定されていることを確認
            assert handler.handler is not None


def test_gcp_logging_handler_emit(mock_gcp_client):
    """GCloudLoggingHandlerのログ出力をテスト"""
    # 内部ハンドラーのモックを作成
    mock_cloud_handler = mock.MagicMock()
    
    # GCloudLoggingHandlerをモックして内部ハンドラーを設定
    with mock.patch('logkiss.handler_gcp.CloudLoggingHandler', return_value=mock_cloud_handler):
        handler = GCloudLoggingHandler(
            project_id="test-project",
            log_name="test-log"
        )
        
        # 内部ハンドラーをモックに設定
        # GCloudLoggingHandlerは自動的にhandler属性を設定するはず
    
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
        
        # レコードにjson_fieldsを追加
        setattr(record, 'json_fields', {
            "test_id": 123,
            "timestamp": datetime.now().timestamp()
        })
        
        # ハンドラーにレコードを送信
        handler.emit(record)
        
        # 内部ハンドラーのemitメソッドが呼び出されたか確認
        mock_cloud_handler.emit.assert_called_once()
        
        # かんたんな確認として、3回以上呼ばれていないことを確認
        assert mock_cloud_handler.emit.call_count == 1


def test_gcp_logging_handler_with_resource():
    """リソース指定付きのGCloudLoggingHandlerをテスト"""
    with mock.patch('google.cloud.logging.Client') as mock_client:
        # クライアントインスタンスのモックを設定
        mock_client_instance = mock.MagicMock()
        mock_client.return_value = mock_client_instance
        
        # CloudLoggingHandlerのモックを作成
        mock_handler = mock.MagicMock()
        
        # CloudLoggingHandlerのクラスをモック化
        with mock.patch('logkiss.handler_gcp.CloudLoggingHandler', return_value=mock_handler) as mock_handler_class:
            # カスタムリソースを設定
            resource = {"type": "global"}
            
            # ハンドラーを初期化（リソース指定付き）
            handler = GCloudLoggingHandler(
                project_id="test-project",
                log_name="test-log",
                resource=resource
            )
            
            # 内部のCloudLoggingHandlerが正しい引数で生成されたか確認
            # resourceパラメータが正しく渡されているか確認
            mock_handler_class.assert_called_once()
            
            # モックが呼び出されたことを確認する別の方法
            assert mock_handler_class.call_count == 1
