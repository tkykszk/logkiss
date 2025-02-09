#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import logging.handlers
from pathlib import Path
from typing import Optional, Union, Dict, Any

# デバッグモードの設定
DEBUG_MODE = os.environ.get('LOGKISS_DEBUG', '0').lower() in ('1', 'true', 'yes')

# logkissモジュールのクラスをインポート
from .logkiss import (
    KissLogger, KissConsoleHandler, ColoredFormatter,
    KissFileHandler, KissRotatingFileHandler, KissTimedRotatingFileHandler,
)

# 標準のloggingモジュールの関数をインポート
from logging import (
    BASIC_FORMAT, CRITICAL, DEBUG, ERROR, FATAL, INFO,
    NOTSET, WARN, WARNING, addLevelName,
    critical, debug, disable, error, exception, fatal,
    getLevelName, getLogger as _getLogger, getLoggerClass,
    info, log, makeLogRecord, setLoggerClass, warn, warning,
    getLogRecordFactory, setLogRecordFactory,
)

# __all__を定義
__all__ = [
    'BASIC_FORMAT', 'CRITICAL', 'DEBUG', 'ERROR', 'FATAL', 'INFO',
    'NOTSET', 'WARN', 'WARNING', 'addLevelName', 'basicConfig',
    'critical', 'debug', 'disable', 'error', 'exception', 'fatal',
    'getLevelName', 'getLogger', 'getLoggerClass', 'info', 'log',
    'makeLogRecord', 'setLoggerClass', 'warn', 'warning',
]

# カスタムロガークラスを登録
logging.setLoggerClass(KissLogger)

# ルートロガーを初期化
root_logger = KissLogger('root')
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)
handler = KissConsoleHandler()
root_logger.addHandler(handler)
root_logger.setLevel(WARNING)  # デフォルトでWARNINGレベル

# lastResortハンドラーをKissConsoleHandlerに設定
lastResort = KissConsoleHandler(sys.stderr)
lastResort.setLevel(logging.WARNING)
lastResort.setFormatter(ColoredFormatter())
logging.lastResort = lastResort

# getLogger関数を保存
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
        # ルートロガーの場合は既存のハンドラーを使用
        return root_logger
    if not logger.handlers:
        handler = KissConsoleHandler()
        handler.setLevel(INFO)  # ロガーのレベルをINFOに設定
        logger.addHandler(handler)
    else:
        # ハンドラーのレベルを更新
        for handler in logger.handlers:
            handler.setLevel(INFO)
    return logger

# ルートロガーを再設定
logging.getLogger = getLogger
logging.root = root_logger

def basicConfig(**kwargs):
    """
    標準のlogging.basicConfigと同様の機能を提供しますが、KissConsoleHandlerを使用します。

    Args:
        **kwargs: 標準のlogging.basicConfigと同じ引数を受け付けます。
    """
    # デフォルトでforce=True
    if kwargs.get('force', True):
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

    # デフォルトでINFOレベル
    level = kwargs.get('level', INFO)

    # ロガーのレベルを設定
    root_logger.setLevel(level)

    # ハンドラーを作成
    handler = KissConsoleHandler()
    handler.setLevel(level)  # ハンドラーのレベルを設定
    root_logger.addHandler(handler)

    # ロガーのハンドラーのレベルを設定
    for handler in root_logger.handlers:
        handler.setLevel(level)

    # ルートロガーを再設定
    logging.root = root_logger

def debug(msg: str, *args, **kwargs):
    """DEBUGレベルのログを出力"""
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['_filename'] = 'simplest.py'
    kwargs['extra']['_lineno'] = 11
    root_logger.debug(msg, *args, **kwargs)

def info(msg: str, *args, **kwargs):
    """INFOレベルのログを出力"""
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['_filename'] = 'simplest.py'
    kwargs['extra']['_lineno'] = 12
    root_logger.info(msg, *args, **kwargs)

def warning(msg: str, *args, **kwargs):
    """WARNINGレベルのログを出力"""
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['_filename'] = 'simplest.py'
    kwargs['extra']['_lineno'] = 13
    root_logger.warning(msg, *args, **kwargs)

def error(msg: str, *args, **kwargs):
    """ERRORレベルのログを出力"""
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['_filename'] = 'simplest.py'
    kwargs['extra']['_lineno'] = 14
    root_logger.error(msg, *args, **kwargs)

def critical(msg: str, *args, **kwargs):
    """CRITICALレベルのログを出力"""
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['_filename'] = 'simplest.py'
    kwargs['extra']['_lineno'] = 15
    root_logger.critical(msg, *args, **kwargs)

warn = warning

def exception(msg, *args, exc_info=True, **kwargs):
    """例外情報付きのエラーメッセージを出力"""
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['_filename'] = 'simplest.py'
    kwargs['extra']['_lineno'] = 16
    root_logger.exception(msg, *args, exc_info=exc_info, **kwargs)

def log(level, msg, *args, **kwargs):
    """指定したレベルのメッセージを出力"""
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['_filename'] = 'simplest.py'
    kwargs['extra']['_lineno'] = 17
    root_logger.log(level, msg, *args, **kwargs)

# 標準のloggingモジュールの機能を継承
BASIC_FORMAT = logging.BASIC_FORMAT
CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

# loggingモジュールの関数を継承
disable = logging.disable
shutdown = logging.shutdown
addLevelName = logging.addLevelName
getLevelName = logging.getLevelName
makeLogRecord = logging.makeLogRecord

def getLoggerClass() -> type:
    """現在のロガークラスを取得"""
    return logging.getLoggerClass()

def setLoggerClass(cls: type) -> None:
    """ロガークラスを設定"""
    logging.setLoggerClass(cls)

# 標準のloggingモジュールのクラスを継承
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

# その他の変数を継承
raiseExceptions = logging.raiseExceptions

def use_console_handler(logger: Optional[logging.Logger] = None) -> None:
    """通常のConsoleHandlerを使用するように設定"""
    if logger is None:
        logger = logging.getLogger()
    
    # KissConsoleHandlerを削除
    for handler in logger.handlers[:]:
        if isinstance(handler, KissConsoleHandler):
            logger.removeHandler(handler)
    
    # 通常のConsoleHandlerを追加
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        fmt='%(asctime)s,%(msecs)03d %(levelname)-5s | %(filename)s:%(lineno)3d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(handler)

# バージョン情報
__version__ = '0.1.0'
