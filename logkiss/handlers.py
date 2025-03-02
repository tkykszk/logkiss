"""
Handlers module for logkiss logging.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.

This module contains various handlers used in logkiss.
Main classes:
- BaseHandler: Base handler class for implementing custom handlers
- GCPCloudLoggingHandler: Handler for sending logs to Google Cloud Logging
- AWSCloudWatchHandler: Handler for sending logs to AWS CloudWatch Logs
"""

import json
import threading
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional, Union

try:
    from google.cloud import logging as google_logging
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False

try:
    import boto3
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False


class BaseHandler:
    """Base handler class for implementing custom handlers"""
    
    def __init__(self) -> None:
        pass
        
    def handle(self, log_entry: Dict[str, Any]) -> None:
        """
        Handle a log entry
        
        Args:
            log_entry: Log entry to be handled
        """
        raise NotImplementedError("handle method must be implemented")


class GCPCloudLoggingHandler(logging.Handler):
    """Handler for sending logs to Google Cloud Logging"""
    
    def __init__(
        self,
        project_id: Optional[str] = None,
        resource: Optional[Dict[str, str]] = None,
        labels: Optional[Dict[str, str]] = None,
        batch_size: int = 100,
        flush_interval: float = 5.0,
    ) -> None:
        """
        Args:
            project_id: Google Cloud project ID. If None, it will be automatically detected from environment variables
            resource: Google Cloud resource. If None, it will be automatically detected
            labels: Labels to add to all log entries
            batch_size: Batch size
            flush_interval: Flush interval in seconds
        """
        if not GOOGLE_CLOUD_AVAILABLE:
            raise ImportError(
                "google-cloud-logging package is required. "
                "Install it with: pip install 'logkiss[cloud]'"
            )
        
        super().__init__()
        self.client = google_logging.Client(project=project_id)
        self.project_id = project_id or self.client.project  # プロジェクトIDを設定
        self.logger = self.client.logger()
        self.resource = resource or {"type": "global"}
        self.labels = labels or {}
        
        self._batch = []
        self._batch_lock = threading.Lock()
        self._batch_size = batch_size
        self._flush_interval = flush_interval
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._running = True
        self._start_periodic_flush()
    
    def handle(self, log_entry: Dict[str, Any]) -> None:
        """
        Handle a log entry and send it to Google Cloud Logging
        
        Args:
            log_entry: Log entry to be handled
        """
        severity = self._convert_level_to_severity(log_entry.get("level", "INFO"))
        entry = {
            "severity": severity,
            "timestamp": log_entry.get("timestamp"),
            "message": log_entry.get("message", ""),
            "labels": {**self.labels, **log_entry.get("labels", {})},
        }
        
        with self._batch_lock:
            self._batch.append(entry)
            if len(self._batch) >= self._batch_size:
                self._flush()
    
    def _start_periodic_flush(self) -> None:
        """Start periodic flush"""
        def _periodic_flush():
            while self._running:
                time.sleep(self._flush_interval)
                self._flush()
        
        self._executor.submit(_periodic_flush)
    
    def _flush(self) -> None:
        """Flush batch"""
        with self._batch_lock:
            if not self._batch:
                return
            
            entries = self._batch
            self._batch = []
        
        try:
            # Google Cloud Logging APIに合わせてエントリを変換
            cloud_entries = []
            for entry in entries:
                cloud_entry = {
                    "severity": entry["severity"],
                    "text_payload": entry["message"],
                    "labels": entry.get("labels", {}),
                }
                if entry.get("timestamp"):
                    cloud_entry["timestamp"] = entry["timestamp"]
                cloud_entries.append(cloud_entry)
                
            # バッチでログを送信
            self.logger.log_entries(cloud_entries, resource=self.resource)
        except Exception as e:
            # Error log will be printed to standard error
            import sys
            print(f"Error writing to Cloud Logging: {e}", file=sys.stderr)
    
    def _convert_level_to_severity(self, level: str) -> str:
        """Convert log level to Cloud Logging severity"""
        mapping = {
            "DEBUG": "DEBUG",
            "INFO": "INFO",
            "WARNING": "WARNING",
            "ERROR": "ERROR",
            "CRITICAL": "CRITICAL",
        }
        return mapping.get(level.upper(), "DEFAULT")

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a record to Google Cloud Logging
        
        Args:
            record: Log record to be emitted
        """
        try:
            self.handle({
                "level": record.levelname,
                "timestamp": record.created,
                "message": record.getMessage(),
                "labels": {}
            })
        except Exception:
            self.handleError(record)

    def close(self) -> None:
        """Close the handler and clean up resources"""
        self._running = False
        with self._batch_lock:
            if self._batch:
                self._flush()
        
        if hasattr(self, '_executor'):
            self._executor.shutdown(wait=True)
        
        super().close()

    def __del__(self):
        """Cleanup when the handler is deleted"""
        self.close()


class AWSCloudWatchHandler(logging.Handler):
    """Handler for sending logs to AWS CloudWatch Logs"""
    
    def __init__(
        self,
        log_group_name: str,
        log_stream_name: Optional[str] = None,
        region_name: Optional[str] = None,
        batch_size: int = 100,
        flush_interval: float = 5.0,
    ) -> None:
        """
        Args:
            log_group_name: Log group name
            log_stream_name: Log stream name. If None, instance ID will be used
            region_name: Region name. If None, it will be automatically detected from environment variables
            batch_size: Batch size
            flush_interval: Flush interval in seconds
        """
        if not AWS_AVAILABLE:
            raise ImportError(
                "boto3 package is required. "
                "Install it with: pip install 'logkiss[cloud]'"
            )
        
        super().__init__()
        self.client = boto3.client("logs", region_name=region_name)
        self.log_group_name = log_group_name
        
        if log_stream_name is None:
            # Try to determine an appropriate log stream name
            # First check if we're running on EC2
            log_stream_name = self._get_instance_identifier()
        
        self.log_stream_name = log_stream_name
        self._ensure_log_group_and_stream()
        
        self._batch = []
        self._batch_lock = threading.Lock()
        self._batch_size = batch_size
        self._flush_interval = flush_interval
        self._sequence_token = None
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._running = True
        self._start_periodic_flush()
    
    def _get_instance_identifier(self) -> str:
        """
        Get a unique identifier for this instance.
        Tries different methods to get a unique identifier:
        1. Check AWS_INSTANCE_ID environment variable
        2. Use hostname
        3. Generate a random UUID as last resort
        
        Returns:
            A string identifier
        """
        import os
        import socket
        
        # Method 1: Try to get instance ID from environment variable
        instance_id = os.environ.get('AWS_INSTANCE_ID')
        if instance_id:
            return instance_id
            
        # Method 2: Use hostname
        try:
            hostname = socket.gethostname()
            if hostname and hostname != 'localhost':
                return hostname
        except Exception as e:
            print(f"Failed to get hostname: {str(e)}")
        
        # Method 3: Generate a random UUID as last resort
        import uuid
        random_id = str(uuid.uuid4())
        return random_id
    
    def _start_periodic_flush(self) -> None:
        """Start periodic flush"""
        def _periodic_flush():
            while self._running:
                time.sleep(self._flush_interval)
                self._flush()
        
        self._executor.submit(_periodic_flush)
    
    def handle(self, record: logging.LogRecord) -> None:
        """
        Handle a log record and send it to CloudWatch Logs
        
        Args:
            record: Log record to be handled
        """
        timestamp = int(record.created * 1000)
        message = json.dumps({
            "message": record.getMessage(),
            "level": record.levelname,
            "timestamp": record.created,
        })
        
        with self._batch_lock:
            self._batch.append({
                "timestamp": timestamp,
                "message": message
            })
            if len(self._batch) >= self._batch_size:
                self._flush()
    
    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a record to CloudWatch Logs
        
        Args:
            record: Log record to be emitted
        """
        try:
            self.handle(record)
        except Exception:
            self.handleError(record)
    
    def _ensure_log_group_and_stream(self) -> None:
        """Ensure log group and log stream exist, create if necessary"""
        try:
            self.client.create_log_group(logGroupName=self.log_group_name)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass
        
        try:
            self.client.create_log_stream(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name
            )
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass
    
    def _flush(self) -> None:
        """Flush batch"""
        with self._batch_lock:
            if not self._batch:
                return
            
            events = sorted(self._batch, key=lambda x: x["timestamp"])
            self._batch = []
        
        try:
            kwargs = {
                "logGroupName": self.log_group_name,
                "logStreamName": self.log_stream_name,
                "logEvents": events
            }
            if self._sequence_token:
                kwargs["sequenceToken"] = self._sequence_token
            
            response = self.client.put_log_events(**kwargs)
            self._sequence_token = response.get("nextSequenceToken")
        except Exception as e:
            # Error log will be printed to standard error
            import sys
            print(f"Error writing to CloudWatch Logs: {e}", file=sys.stderr)

    def close(self):
        """
        Close the handler and clean up resources
        """
        self._running = False
        self._flush()  # 最後に残っているログをフラッシュ
        
        if hasattr(self, '_executor'):
            self._executor.shutdown(wait=False)  # 非同期でシャットダウン
            
        super().close()
