"""
Handlers module for logkiss logging.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.

This module contains various handlers used in logkiss.
Main classes:
- BaseHandler: Base handler class for implementing custom handlers
- KissGCPCloudLoggingHandler: Handler for sending logs to Google Cloud Logging
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


class KissGCPCloudLoggingHandler(logging.Handler):
    """Handler for sending logs to Google Cloud Logging"""
    
    def __init__(
        self,
        project_id: Optional[str] = None,
        resource: Optional[Dict[str, str]] = None,
        labels: Optional[Dict[str, str]] = None,
        batch_size: int = 100,
        flush_interval: float = 2.0,
        log_name: str = "python",
    ) -> None:
        """
        Args:
            project_id: Google Cloud project ID. If None, it will be automatically detected from environment variables
            resource: Google Cloud resource. If None, it will be automatically detected
            labels: Labels to add to all log entries
            batch_size: Batch size
            flush_interval: Flush interval in seconds
            log_name: Name of the log
        """
        if not GOOGLE_CLOUD_AVAILABLE:
            raise ImportError(
                "google-cloud-logging package is required. "
                "Install it with: pip install 'logkiss[cloud]'"
            )
        
        # 先に基底クラスの初期化
        super().__init__()
        
        # 属性を初期化して、初期化失敗時のエラーを防ぐ
        self._batch = []
        self._batch_lock = threading.Lock()
        self._batch_size = batch_size
        self._flush_interval = flush_interval
        self._executor = None
        self._running = False
        self._flush_thread = None
        
        try:
            # Google Cloud Loggingクライアントを初期化
            self.client = google_logging.Client(project=project_id)
            self.project_id = project_id or self.client.project  # プロジェクトIDを設定
            self.logger = self.client.logger(log_name)
            self.resource = resource or {"type": "global"}
            self.labels = labels or {}
            
            # 定期的なフラッシュを開始
            self._start_periodic_flush()
        except Exception as e:
            import sys
            print(f"Error initializing KissGCPCloudLoggingHandler: {e}", file=sys.stderr)
            # 初期化に失敗した場合は、runningフラグをFalseにして、スレッドが開始されないようにする
            self._running = False
            raise

    def _start_periodic_flush(self):
        """Start a background thread to periodically flush the batch."""
        if self._flush_thread is not None and self._flush_thread.is_alive():
            return  # すでに実行中のスレッドがある場合は何もしない

        self._running = True
        self._flush_thread = threading.Thread(
            target=self._periodic_flush_worker,
            daemon=True,  # デーモンスレッドとして実行（プログラム終了時に自動終了）
        )
        self._flush_thread.start()

    def _periodic_flush_worker(self):
        """Worker function for the periodic flush thread."""
        while self._running:
            try:
                # ここでの二重チェックは重要
                if not self._running:
                    break
                self._flush()
            except Exception as e:
                import sys
                print(f"Error in periodic flush: {e}", file=sys.stderr)
                # エラーが発生しても継続する
            
            # スリープ前に終了フラグを確認
            if not self._running:
                break
                
            # 次の実行までスリープ
            time.sleep(self._flush_interval)

    def emit(self, record: logging.LogRecord) -> None:
        """Process log record"""
        if not self._running:
            return
            
        try:
            # ログレコードからメッセージを取得
            message = self.format(record)
            
            # ログレベルをGoogle Cloud Loggingのseverityに変換
            severity = self._convert_level_to_severity(record.levelname)
            
            # エラーログまたは例外情報がある場合は常にERRORレベルに設定
            if record.levelno >= logging.ERROR or record.exc_info:
                severity = "ERROR"
            
            # エントリを作成
            entry = {
                "message": message,
                "severity": severity,
                "labels": self.labels.copy(),
                "json_payload": {},  # extraの内容をjson_payloadとして送信するための辞書
            }
            
            # 追加情報がある場合は追加
            if hasattr(record, "extra") and isinstance(record.extra, dict):
                # extraの内容をjson_payloadにコピー
                entry["json_payload"] = record.extra.copy()
                
                # labelsにも追加（文字列に変換）
                for key, value in record.extra.items():
                    if not isinstance(value, (str, bytes)):
                        entry["labels"][key] = str(value)
                    else:
                        entry["labels"][key] = value
            
            # exc_info=Trueが指定された場合のスタックトレース情報を追加
            if record.exc_info:
                import traceback
                stack_trace_list = traceback.format_exception(*record.exc_info)
                entry["labels"]["stack_trace"] = ''.join(stack_trace_list)
            
            # バッチに追加
            with self._batch_lock:
                self._batch.append(entry)
                
                # バッチサイズに達したらフラッシュ
                if len(self._batch) >= self._batch_size:
                    self._flush()
        except Exception as e:
            import sys
            print(f"Error in KissGCPCloudLoggingHandler.emit: {e}", file=sys.stderr)

    def _convert_level_to_severity(self, level: str) -> str:
        """Convert log level to Google Cloud Logging severity"""
        severity_map = {
            "DEBUG": "DEBUG",
            "INFO": "INFO",
            "WARNING": "WARNING",
            "ERROR": "ERROR",
            "CRITICAL": "CRITICAL",
        }
        return severity_map.get(level, "DEFAULT")

    def _flush(self) -> None:
        """Flush batch"""
        if not self._running:
            return
            
        entries = []
        with self._batch_lock:
            if not self._batch:
                return
            
            entries = self._batch
            self._batch = []
        
        if not entries:
            return
            
        try:
            # Google Cloud Logging APIを使用してログを送信
            for entry in entries:
                # 構造化ログを作成
                struct_data = {
                    "message": entry["message"]
                }
                
                # json_payloadがある場合は構造化ログに追加
                if entry.get("json_payload"):
                    struct_data.update(entry["json_payload"])
                
                # log_structメソッドを使用して構造化ログを送信
                self.logger.log_struct(
                    info=struct_data,
                    severity=entry["severity"],
                    labels=entry.get("labels", {})
                )
        except Exception as e:
            # Error log will be printed to standard error
            import sys
            print(f"Error writing to Cloud Logging: {e}", file=sys.stderr)

    def close(self):
        """
        Close the handler and release all resources.
        """
        if not hasattr(self, '_running'):
            # 初期化が完了していない場合は何もしない
            super().close()
            return
            
        try:
            # スレッドを停止
            self._running = False
            
            # 最後の一回フラッシュを試みる
            try:
                self._flush()
            except Exception as e:
                import sys
                print(f"Error in final flush: {e}", file=sys.stderr)
                
            # スレッドが存在し、実行中であれば、終了を待つ（最大1秒）
            if hasattr(self, '_flush_thread') and self._flush_thread is not None:
                if self._flush_thread.is_alive():
                    self._flush_thread.join(timeout=1.0)
        except Exception as e:
            import sys
            print(f"Error closing handler: {e}", file=sys.stderr)
        finally:
            # 親クラスのcloseメソッドを呼び出す
            super().close()

    def __del__(self):
        """Cleanup when the handler is deleted"""
        try:
            if hasattr(self, '_running') and self._running:
                self.close()
        except Exception:
            # __del__内では例外を無視
            pass


class AWSCloudWatchHandler(logging.Handler):
    """
    AWS CloudWatch Logs handler
    """

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
        
        # 先に基底クラスの初期化
        super().__init__()
        
        # 属性を初期化して、初期化失敗時のエラーを防ぐ
        self._batch = []
        self._batch_lock = threading.Lock()
        self._batch_size = batch_size
        self._flush_interval = flush_interval
        self._sequence_token = None
        self._executor = None
        self._running = False
        self._flush_thread = None
        
        try:
            # AWS CloudWatch Logsクライアントを初期化
            self.client = boto3.client("logs", region_name=region_name)
            self.log_group_name = log_group_name
            
            if log_stream_name is None:
                # Try to determine an appropriate log stream name
                # First check if we're running on EC2
                log_stream_name = self._get_instance_identifier()
            
            self.log_stream_name = log_stream_name
            self._ensure_log_group_and_stream()
            
            # 定期的なフラッシュを開始
            self._start_periodic_flush()
        except Exception as e:
            import sys
            print(f"Error initializing AWSCloudWatchHandler: {e}", file=sys.stderr)
            # 初期化に失敗した場合は、runningフラグをFalseにして、スレッドが開始されないようにする
            self._running = False
            raise

    def _get_instance_identifier(self) -> str:
        """
        Get instance identifier for log stream name
        """
        try:
            # Try to get EC2 instance ID
            import requests
            response = requests.get(
                "http://169.254.169.254/latest/meta-data/instance-id",
                timeout=0.1
            )
            if response.status_code == 200:
                return response.text
        except Exception:
            pass
        
        # Fallback to hostname
        import socket
        return socket.gethostname()

    def _ensure_log_group_and_stream(self) -> None:
        """
        Ensure log group and stream exist
        """
        # Create log group if it doesn't exist
        try:
            self.client.create_log_group(logGroupName=self.log_group_name)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass
        
        # Create log stream if it doesn't exist
        try:
            self.client.create_log_stream(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name
            )
        except self.client.exceptions.ResourceAlreadyExistsException:
            # Get sequence token
            response = self.client.describe_log_streams(
                logGroupName=self.log_group_name,
                logStreamNamePrefix=self.log_stream_name,
                limit=1
            )
            
            for stream in response.get("logStreams", []):
                if stream.get("logStreamName") == self.log_stream_name:
                    self._sequence_token = stream.get("uploadSequenceToken")
                    break

    def _start_periodic_flush(self):
        """Start a background thread to periodically flush the batch."""
        if self._flush_thread is not None and self._flush_thread.is_alive():
            return  # すでに実行中のスレッドがある場合は何もしない

        self._running = True
        self._flush_thread = threading.Thread(
            target=self._periodic_flush_worker,
            daemon=True,  # デーモンスレッドとして実行（プログラム終了時に自動終了）
        )
        self._flush_thread.start()

    def _periodic_flush_worker(self):
        """Worker function for the periodic flush thread."""
        while self._running:
            try:
                # ここでの二重チェックは重要
                if not self._running:
                    break
                self._flush()
            except Exception as e:
                import sys
                print(f"Error in periodic flush: {e}", file=sys.stderr)
                # エラーが発生しても継続する
            
            # スリープ前に終了フラグを確認
            if not self._running:
                break
                
            # 次の実行までスリープ
            time.sleep(self._flush_interval)

    def emit(self, record: logging.LogRecord) -> None:
        """Process log record"""
        if not self._running:
            return
            
        try:
            # ログレコードからメッセージを取得
            message = self.format(record)
            
            # タイムスタンプを取得（ミリ秒単位）
            timestamp = int(record.created * 1000)
            
            # エントリを作成
            entry = {
                "timestamp": timestamp,
                "message": message,
            }
            
            # exc_info=Trueが指定された場合のスタックトレース情報を追加
            if record.exc_info:
                import traceback
                import json
                # JSONとして追加情報を埋め込む
                entry["message"] += "\nStack Trace: " + json.dumps({
                    "stack_trace": traceback.format_exception(*record.exc_info)
                })
            
            # バッチに追加
            with self._batch_lock:
                self._batch.append(entry)
                
                # バッチサイズに達したらフラッシュ
                if len(self._batch) >= self._batch_size:
                    self._flush()
        except Exception as e:
            import sys
            print(f"Error in AWSCloudWatchHandler.emit: {e}", file=sys.stderr)

    def _flush(self) -> None:
        """Flush batch"""
        if not self._running:
            return
            
        entries = []
        with self._batch_lock:
            if not self._batch:
                return
            
            entries = self._batch
            self._batch = []
        
        if not entries:
            return
            
        # Sort entries by timestamp
        entries.sort(key=lambda x: x["timestamp"])
        
        # Convert to CloudWatch Logs format
        log_events = [
            {
                "timestamp": entry["timestamp"],
                "message": entry["message"]
            }
            for entry in entries
        ]
        
        # Send to CloudWatch Logs
        try:
            kwargs = {
                "logGroupName": self.log_group_name,
                "logStreamName": self.log_stream_name,
                "logEvents": log_events
            }
            
            if self._sequence_token:
                kwargs["sequenceToken"] = self._sequence_token
            
            response = self.client.put_log_events(**kwargs)
            self._sequence_token = response.get("nextSequenceToken")
        except self.client.exceptions.InvalidSequenceTokenException as e:
            # Get the correct sequence token from the error message
            import re
            match = re.search(r"sequenceToken is: (\S+)", str(e))
            if match:
                self._sequence_token = match.group(1)
                # Retry with the correct sequence token
                self._flush()
        except Exception as e:
            import sys
            print(f"Error writing to CloudWatch Logs: {e}", file=sys.stderr)
            # Put the entries back in the batch
            with self._batch_lock:
                self._batch = entries + self._batch

    def close(self):
        """
        Close the handler and release all resources.
        """
        if not hasattr(self, '_running'):
            # 初期化が完了していない場合は何もしない
            super().close()
            return
            
        try:
            # スレッドを停止
            self._running = False
            
            # 最後の一回フラッシュを試みる
            try:
                self._flush()
            except Exception as e:
                import sys
                print(f"Error in final flush: {e}", file=sys.stderr)
                
            # スレッドが存在し、実行中であれば、終了を待つ（最大1秒）
            if hasattr(self, '_flush_thread') and self._flush_thread is not None:
                if self._flush_thread.is_alive():
                    self._flush_thread.join(timeout=1.0)
        except Exception as e:
            import sys
            print(f"Error closing handler: {e}", file=sys.stderr)
        finally:
            # 親クラスのcloseメソッドを呼び出す
            super().close()

    def __del__(self):
        """Cleanup when the handler is deleted"""
        try:
            if hasattr(self, '_running') and self._running:
                self.close()
        except Exception:
            # __del__内では例外を無視
            pass
