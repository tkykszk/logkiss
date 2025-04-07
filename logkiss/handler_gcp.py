#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Google Cloud Logging Handler for logkiss.

This module provides a handler for sending logs to Google Cloud Logging.
It uses the official Google Cloud Logging client library.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
"""

import logging
import os
from typing import Dict, Any, Optional, Union

# Flag to track if Google Cloud Logging is available
HAS_GOOGLE_CLOUD_LOGGING = False

# Try to import Google Cloud Logging modules
try:
    from google.cloud import logging as google_logging
    from google.cloud.logging_v2.handlers import CloudLoggingHandler
    # EXCLUDED_LOGGER_DEFAULTS is imported but not used currently
    HAS_GOOGLE_CLOUD_LOGGING = True
except ImportError:
    # Define placeholder for when the module is not available
    class CloudLoggingHandler:
        """Placeholder for CloudLoggingHandler when Google Cloud Logging is not available."""
        def __init__(self, *args, **kwargs):
            """Placeholder constructor"""
            # No implementation needed


class GCloudLoggingHandler(logging.Handler):
    """Google Cloud Logging handler for logkiss.
    
    This handler uses the official Google Cloud Logging client library to send logs
    to Google Cloud Logging. It provides a simple interface for configuring and using
    the handler.
    
    Args:
        project_id (str, optional): Google Cloud Project ID. If not provided, it will be
            determined from the environment.
        credentials (google.auth.credentials.Credentials, optional): Google Cloud credentials.
            If not provided, default credentials will be used.
        labels (Dict[str, str], optional): Labels to add to all log entries.
        log_name (str, optional): Name of the log to write to. Defaults to 'python'.
        resource (google.cloud.logging_v2.resource.Resource, optional): Monitored resource
            to use for logging. If not provided, it will be determined from the environment.
        excluded_loggers (list, optional): List of logger names to exclude from logging.
    """
    
    def __init__(
        self,
        project_id: Optional[str] = None,
        credentials: Any = None,
        log_name: str = "python",
        labels: Optional[Dict[str, str]] = None,
        resource: Any = None,
        excluded_loggers: Optional[list] = None,
    ) -> None:
        """Initialize the handler.
        
        Args:
            project_id: Google Cloud project ID. If None, it will be automatically detected.
            credentials: Google Cloud credentials. If None, default credentials will be used.
            log_name: Name of the log to write to.
            labels: Labels to add to all log entries.
            resource: Monitored resource to use for logging.
            excluded_loggers: List of logger names to exclude from logging.
            
        Raises:
            ImportError: If Google Cloud Logging is not available.
        """
        if not HAS_GOOGLE_CLOUD_LOGGING:
            raise ImportError(
                "Google Cloud Logging is not available. "
                "Please install the required dependencies using: "
                "pip install google-cloud-logging"
            )
            
        super().__init__()
        
        # Initialize Google Cloud Logging client
        client = google_logging.Client(project=project_id, credentials=credentials)
        
        # Create the handler with the specified configuration
        self.handler = CloudLoggingHandler(
            client,
            name=log_name,
            labels=labels,
            resource=resource,
        )
        
        # Store excluded loggers
        self.excluded_loggers = excluded_loggers or []
        
        # Formatter for the handler
        formatter = logging.Formatter('%(message)s')
        self.setFormatter(formatter)
    
    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record.
        
        Args:
            record (logging.LogRecord): The log record to emit.
        """
        # Skip excluded loggers
        if record.name in self.excluded_loggers:
            return
        
        # Ensure extra is a dict if it exists
        if hasattr(record, "extra") and not isinstance(record.extra, dict):
            record.extra = {"extra": str(record.extra)}
        
        # Google Cloud Loggingのハンドラーが期待する属性を追加
        if not hasattr(record, "_resource"):
            record._resource = None
            
        # _labels属性を追加
        if not hasattr(record, "_labels"):
            record._labels = {}
            
        # extraの内容を処理
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            # 特別なキー "json_fields" を使用して構造化ログを設定
            # CloudLoggingHandlerは内部でjson_fieldsをjsonPayloadとして扱う
            record.json_fields = {}
            for key, value in record.extra.items():
                # 値を文字列に変換（必要な場合）
                if not isinstance(value, (str, int, float, bool, dict, list, type(None))):
                    value = str(value)
                record.json_fields[key] = value
                
            # labelsにも追加（文字列に変換）
            for key, value in record.extra.items():
                record._labels[key] = str(value) if not isinstance(value, (str, bytes)) else value
        
        # その他の必要な属性を追加
        for attr in ["_trace", "_span_id", "_trace_sampled", "_http_request", "_source_location"]:
            if not hasattr(record, attr):
                setattr(record, attr, None)
        
        # Forward to Google Cloud Logging handler
        self.handler.emit(record)
    
    def close(self) -> None:
        """Close the handler."""
        self.handler.close()
        super().close()


def setup_gcp_logging(
    project_id: Optional[str] = None,
    log_name: str = "python",
    labels: Optional[Dict[str, str]] = None,
    level: Union[int, str] = logging.INFO,
    excluded_loggers: Optional[list] = None,
) -> GCloudLoggingHandler:
    """Google Cloud Loggingの設定を行います。

    Args:
        project_id: Google CloudプロジェクトのプロジェクトID。Noneの場合は環境変数から自動検出します。
        log_name: ログ名
        labels: すべてのログエントリに追加するラベル
        level: ログレベル
        excluded_loggers: 除外するロガー名のリスト

    Returns:
        GCloudLoggingHandler: 設定されたハンドラー
    """
    # ルートロガーを取得
    root_logger = logging.getLogger()
    
    # GCloudLoggingHandlerを作成
    handler = GCloudLoggingHandler(
        project_id=project_id,
        log_name=log_name,
        labels=labels,
        excluded_loggers=excluded_loggers,
    )
    
    # ログレベルを設定
    handler.setLevel(level)
    
    # ルートロガーにハンドラーを追加
    root_logger.addHandler(handler)
    
    return handler


# Simple usage example
def create_handler(
    project_id: Optional[str] = None,
    log_name: str = "python",
    labels: Optional[Dict[str, str]] = None,
) -> GCloudLoggingHandler:
    """Create a GCloudLoggingHandler with minimal configuration.
    
    Args:
        project_id (str, optional): Google Cloud Project ID. If not provided, it will be
            determined from the environment.
        log_name (str, optional): Name of the log to write to. Defaults to 'python'.
        labels (Dict[str, str], optional): Labels to add to all log entries.
    
    Returns:
        GCloudLoggingHandler: The created handler.
    """
    # Use environment variable if project_id is not provided
    if project_id is None:
        project_id = os.environ.get("GCP_PROJECT_ID")
    
    # Create the handler
    return GCloudLoggingHandler(
        project_id=project_id,
        log_name=log_name,
        labels=labels,
    )
