"""logkiss - Keep It Simple and Stupid Logger.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.

A simple and colorful Python logging library.
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import logging.handlers
from pathlib import Path
from typing import Optional, Union, Dict, Any

# Set debug mode
DEBUG_MODE = os.environ.get('LOGKISS_DEBUG', '0').lower() in ('1', 'true', 'yes')

# Import logkiss module classes
from .logkiss import (
    KissLogger, KissConsoleHandler, ColoredFormatter,
    setup_from_yaml, setup_from_env,
)

# Import base handler only
from .handlers import BaseHandler

# プロキシクラスと遅延インポート機能
# クラウドサービス依存関係を実際に使用するまで読み込まない

# AWS CloudWatchハンドラー用プロキシクラス
class AWSCloudWatchHandler:
    """AWS CloudWatch Logs対応のロギングハンドラー
    
    実際のAWS SDK (boto3)の読み込みは初めて使用されるときまで遅延されます。
    """
    def __new__(cls, *args, **kwargs):
        # 遅延インポート
        try:
            from .handlers import AWSCloudWatchHandler as RealHandler
            # 実際のクラスのインスタンスを返す
            return RealHandler(*args, **kwargs)
        except ImportError as exc:
            raise ImportError(
                "AWSCloudWatchHandler requires boto3 package. "
                "Install it with: pip install 'logkiss[aws]' or pip install boto3"
            ) from exc

# GCP Cloud Loggingハンドラー用プロキシクラス
class GCloudLoggingHandler:
    """Google Cloud Logging対応のロギングハンドラー
    
    実際のGoogle Cloud SDK (google-cloud-logging)の読み込みは初めて使用されるときまで遅延されます。
    """
    def __new__(cls, *args, **kwargs):
        # 遅延インポート
        try:
            from .handler_gcp import GCloudLoggingHandler as RealHandler
            # 実際のクラスのインスタンスを返す
            return RealHandler(*args, **kwargs)
        except ImportError as exc:
            raise ImportError(
                "GCloudLoggingHandler requires google-cloud-logging package. "
                "Install it with: pip install 'logkiss[gcp]' or pip install google-cloud-logging"
            ) from exc

# GCPロギング設定関数の遅延インポート版
def setup_gcp_logging(*args, **kwargs):
    """Google Cloud Loggingの設定を行う（遅延ロード）
    
    実際のGoogle Cloud SDK (google-cloud-logging)の読み込みは初めて使用されるときまで遅延されます。
    """
    try:
        from .handler_gcp import setup_gcp_logging as real_setup
        return real_setup(*args, **kwargs)
    except ImportError as exc:
        raise ImportError(
            "setup_gcp_logging requires google-cloud-logging package. "
            "Install it with: pip install 'logkiss[gcp]' or pip install google-cloud-logging"
        ) from exc

# Try to import Qt handler if available
try:
    from .handler_qt import QtTextEditHandler, QT_AVAILABLE
except ImportError:
    QT_AVAILABLE = False

# Import standard logging module functions
from logging import (
    BASIC_FORMAT, CRITICAL, DEBUG, ERROR, FATAL, INFO,
    NOTSET, WARN, WARNING, addLevelName,
    critical, debug, disable, error, exception, fatal,
    getLevelName, getLogger as _getLogger, getLoggerClass,
    info, log, makeLogRecord, setLoggerClass, warn, warning,
    getLogRecordFactory, setLogRecordFactory,
)

# Define __all__
__all__ = [
    'BASIC_FORMAT', 'BufferingFormatter', 'CRITICAL', 'DEBUG', 'ERROR',
    'FATAL', 'FileHandler', 'Filter', 'Formatter', 'Handler', 'INFO',
    'LogRecord', 'Logger', 'LoggerAdapter', 'NOTSET', 'NullHandler',
    'StreamHandler', 'WARN', 'WARNING', 'addLevelName', 'basicConfig',
    'critical', 'debug', 'disable', 'error',
    'exception', 'fatal', 'getLevelName', 'getLogger', 'getLoggerClass',
    'info', 'log', 'makeLogRecord', 'setLoggerClass', 'warn', 'warning',
    # ハンドラー
    'BaseHandler',
    'AWSCloudWatchHandler',
    'GCloudLoggingHandler',
    'setup_gcp_logging',
    # Qt handler
    'QtTextEditHandler',
    'QT_AVAILABLE',
    # 設定
    'setup_from_yaml',
    'setup_from_env',
]

# グローバル設定
_replace_root_logger = False  # デフォルトでは置き換えない
_root_logger_configured = False
_original_root_state = None  # 元のルートロガーの状態を保存

# Register custom logger class
logging.setLoggerClass(KissLogger)

# 元のルートロガーを保存
_original_root_logger = logging.root

# KissLoggerベースのルートロガーを作成
_kiss_root_logger = KissLogger('root')
for handler in _kiss_root_logger.handlers[:]:
    _kiss_root_logger.removeHandler(handler)
handler = KissConsoleHandler()
_kiss_root_logger.addHandler(handler)
_kiss_root_logger.setLevel(WARNING)  # Default to WARNING level

# KissLoggerルート使用時のみルートロガーを置き換える
if _replace_root_logger:
    logging.root = _kiss_root_logger
    root_logger = _kiss_root_logger
else:
    # 標準のルートロガーを使う（デフォルト）
    root_logger = _original_root_logger

# Set lastResort handler to KissConsoleHandler
lastResort = KissConsoleHandler(sys.stderr)
lastResort.setLevel(logging.WARNING)
lastResort.setFormatter(ColoredFormatter())
logging.lastResort = lastResort

# Save getLogger function
_getLogger = logging.getLogger

def getLogger(name: str = None) -> logging.Logger:
    """Get a logger with the specified name.

    Args:
        name: The name of the logger. If not specified, return the root logger.

    Returns:
        A logger with the specified name.
    """
    logger = _getLogger(name)
    if name is None:
        # ルートロガーの場合はグローバル変数のルートロガーを返す
        return root_logger
        
    # 非ルートロガーの場合、ハンドラーがなければ追加
    if not logger.handlers:
        # 親にハンドラーがある場合は伝播されるので追加不要
        parent_has_handlers = any(h for h in [logger.parent] if h.handlers)
        if not parent_has_handlers:
            kiss_handler = KissConsoleHandler()
            kiss_handler.setLevel(INFO)  # ハンドラーレベルをINFOに設定
            logger.addHandler(kiss_handler)
    
    return logger

# ロガーの初期化関数
def init_logging(replace_root=False, restore_original=False):
    """ロガーシステムを初期化します
    
    Args:
        replace_root: Trueの場合、ルートロガーをKissLoggerで置き換えます（階層は自動的に保持）
        restore_original: Trueの場合、変更前の状態に戻します
    
    Returns:
        ルートロガー
    """
    global _replace_root_logger, _root_logger_configured, root_logger, _original_root_state  # pylint: disable=global-statement
    
    # 最初の呼び出し時にオリジナルの状態を保存
    if _original_root_state is None:
        # オリジナルの状態を辞書として保存
        _original_root_state = {
            'level': logging.root.level,
            'handlers': logging.root.handlers[:],
            'disabled': logging.root.disabled,
            'propagate': logging.root.propagate,
            'filters': logging.root.filters[:],
            'class': logging.root.__class__
        }
    
    if restore_original:
        # オリジナルの状態に戻す
        old_root = logging.root
        
        # ハンドラをクリア
        for handler in old_root.handlers[:]:
            old_root.removeHandler(handler)
            
        # 保存したハンドラーを復元
        for handler in _original_root_state['handlers']:
            old_root.addHandler(handler)
            
        # 基本属性を復元
        old_root.level = _original_root_state['level']
        old_root.disabled = _original_root_state['disabled']
        old_root.propagate = _original_root_state['propagate']
        
        # ロガークラスを復元
        logging.setLoggerClass(_original_root_state['class'])
        
        _replace_root_logger = False
        root_logger = old_root
        _root_logger_configured = False
        
        return root_logger
    
    _replace_root_logger = replace_root
    
    if replace_root:
        # インプレース更新方式（broken parent問題を解消）
        old_root = logging.root
        
        # ハンドラーを更新
        for handler in old_root.handlers[:]:
            old_root.removeHandler(handler)
            
        # KissConsoleHandlerを追加
        kiss_handler = KissConsoleHandler()  # pylint: disable=redefined-outer-name
        old_root.addHandler(kiss_handler)
        old_root.setLevel(WARNING)
        
        # KissLoggerの属性をルートロガーにコピーする
        attrs_to_copy = ['findCaller', 'handle', 'makeRecord']
        for attr in attrs_to_copy:
            if hasattr(_kiss_root_logger, attr):
                try:
                    setattr(old_root, attr, getattr(_kiss_root_logger, attr))
                except (AttributeError, TypeError):
                    pass
        
        # 既存のロガー階層は自動的に保持される（インプレース更新のため）
        root_logger = old_root
    else:
        # 標準のルートロガーを使用
        root_logger = _original_root_logger
        
        # 標準ルートロガーにKissConsoleHandlerを追加するか判断
        if not _root_logger_configured:
            has_console_handler = any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers)
            if not has_console_handler:
                kiss_handler = KissConsoleHandler()  # pylint: disable=redefined-outer-name
                root_logger.addHandler(kiss_handler)
            _root_logger_configured = True
    
    return root_logger

# デフォルトでは標準ロガーを使用するように初期化
init_logging(False)

# getLoggerのみオーバーライド
logging.getLogger = getLogger

def basicConfig(**kwargs):
    """
    Provides the same functionality as standard logging.basicConfig, but uses KissConsoleHandler.

    Args:
        **kwargs: Accepts the same arguments as standard logging.basicConfig.
    """
    # Default to force=True
    if kwargs.get('force', True):
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

    # Default to INFO level
    level = kwargs.get('level', INFO)

    # Set logger level
    root_logger.setLevel(level)

    # Create handler
    handler = KissConsoleHandler()
    handler.setLevel(level)  # Set handler level
    root_logger.addHandler(handler)

    # Set logger handler levels
    for handler in root_logger.handlers:
        handler.setLevel(level)

    # Reset root logger
    logging.root = root_logger

def debug(msg: str, *args, **kwargs):
    """Output DEBUG level log"""
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['_filename'] = 'simplest.py'
    kwargs['extra']['_lineno'] = 11
    root_logger.debug(msg, *args, **kwargs)

def info(msg: str, *args, **kwargs):
    """Output INFO level log"""
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['_filename'] = 'simplest.py'
    kwargs['extra']['_lineno'] = 12
    root_logger.info(msg, *args, **kwargs)

def warning(msg: str, *args, **kwargs):
    """Output WARNING level log"""
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['_filename'] = 'simplest.py'
    kwargs['extra']['_lineno'] = 13
    root_logger.warning(msg, *args, **kwargs)

def error(msg: str, *args, **kwargs):
    """Output ERROR level log"""
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['_filename'] = 'simplest.py'
    kwargs['extra']['_lineno'] = 14
    root_logger.error(msg, *args, **kwargs)

def critical(msg: str, *args, **kwargs):
    """Output CRITICAL level log"""
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['_filename'] = 'simplest.py'
    kwargs['extra']['_lineno'] = 15
    root_logger.critical(msg, *args, **kwargs)

warn = warning

def exception(msg, *args, exc_info=True, **kwargs):
    """Output error message with exception information"""
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['_filename'] = 'simplest.py'
    kwargs['extra']['_lineno'] = 16
    root_logger.exception(msg, *args, exc_info=exc_info, **kwargs)

def log(level, msg, *args, **kwargs):
    """Output message at specified level"""
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['_filename'] = 'simplest.py'
    kwargs['extra']['_lineno'] = 17
    root_logger.log(level, msg, *args, **kwargs)

# Inherit standard logging module functions
BASIC_FORMAT = logging.BASIC_FORMAT
CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

# Inherit logging module functions
disable = logging.disable
shutdown = logging.shutdown
addLevelName = logging.addLevelName
getLevelName = logging.getLevelName
makeLogRecord = logging.makeLogRecord

def getLoggerClass() -> type:
    """Get current logger class"""
    return logging.getLoggerClass()

def setLoggerClass(cls: type) -> None:
    """Set logger class"""
    logging.setLoggerClass(cls)

# Inherit standard logging module classes
BufferingFormatter = logging.BufferingFormatter
Filter = logging.Filter
Formatter = logging.Formatter
Handler = logging.Handler
LogRecord = logging.LogRecord
Logger = logging.Logger
LoggerAdapter = logging.LoggerAdapter
Manager = logging.Manager
PlaceHolder = logging.PlaceHolder
StreamHandler = logging.StreamHandler
FileHandler = logging.FileHandler
NullHandler = logging.NullHandler
RotatingFileHandler = logging.handlers.RotatingFileHandler
TimedRotatingFileHandler = logging.handlers.TimedRotatingFileHandler

# Inherit other variables
raiseExceptions = logging.raiseExceptions

def use_console_handler(logger: Optional[logging.Logger] = None) -> None:
    """Use standard ConsoleHandler
    
    .. deprecated:: 2.2.0
       This function is deprecated. Use standard logging methods instead:
       
       .. code-block:: python
       
          # Remove existing handlers and add a standard one
          logger.handlers.clear()
          logger.addHandler(logging.StreamHandler())
    """
    import warnings
    warnings.warn(
        "use_console_handler is deprecated. Use standard logging methods instead: "
        "logger.handlers.clear() and logger.addHandler(logging.StreamHandler())",
        DeprecationWarning, 
        stacklevel=2
    )
    
    if logger is None:
        logger = logging.getLogger()
    
    # Remove KissConsoleHandler
    for handler in logger.handlers[:]:
        if isinstance(handler, KissConsoleHandler):
            logger.removeHandler(handler)
    
    # Add standard ConsoleHandler
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        fmt='%(asctime)s,%(msecs)03d %(levelname)-5s | %(filename)s:%(lineno)3d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(handler)

# Version information
__version__ = '2.2.1'
