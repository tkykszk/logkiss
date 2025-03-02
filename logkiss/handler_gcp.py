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

from google.cloud import logging as google_logging
from google.cloud.logging_v2.handlers import CloudLoggingHandler as GoogleCloudLoggingHandler
from google.cloud.logging_v2.handlers.handlers import EXCLUDED_LOGGER_DEFAULTS


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
        labels: Optional[Dict[str, str]] = None,
        log_name: str = "python",
        resource: Any = None,
        excluded_loggers: Optional[list] = None,
    ):
        """Initialize the handler."""
        super().__init__()
        
        # Initialize Google Cloud Logging client
        self.project_id = project_id
        self.client = google_logging.Client(
            project=project_id,
            credentials=credentials,
        )
        
        # Create the handler
        self.handler = GoogleCloudLoggingHandler(
            client=self.client,
            name=log_name,
            labels=labels,
            resource=resource,
        )
        
        # Set up excluded loggers
        self.excluded_loggers = excluded_loggers or EXCLUDED_LOGGER_DEFAULTS
    
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
            
        # extraの内容を_labelsに追加
        if hasattr(record, "extra") and isinstance(record.extra, dict):
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


def setup_logging(
    project_id: Optional[str] = None,
    credentials: Any = None,
    labels: Optional[Dict[str, str]] = None,
    log_name: str = "python",
    resource: Any = None,
    excluded_loggers: Optional[list] = None,
    level: int = logging.INFO,
    root_level: int = logging.WARNING,
) -> GCloudLoggingHandler:
    """Set up logging to Google Cloud Logging.
    
    This function creates a GCloudLoggingHandler and adds it to the root logger.
    
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
        level (int, optional): Logging level for the handler. Defaults to INFO.
        root_level (int, optional): Logging level for the root logger. Defaults to WARNING.
    
    Returns:
        GCloudLoggingHandler: The created handler.
    """
    # Create the handler
    handler = GCloudLoggingHandler(
        project_id=project_id,
        credentials=credentials,
        labels=labels,
        log_name=log_name,
        resource=resource,
        excluded_loggers=excluded_loggers,
    )
    
    # Set the handler level
    handler.setLevel(level)
    
    # Add the handler to the root logger
    logging.getLogger().addHandler(handler)
    
    # Set the root logger level
    logging.getLogger().setLevel(root_level)
    
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
