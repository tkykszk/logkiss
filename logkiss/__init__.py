#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import logging.handlers
from pathlib import Path
from typing import Optional, Union

from .logkiss import KissConsoleHandler, ColoredFormatter, KissLogger

# 標準のloggingモジュールの__all__と同じ内容をエクスポート
__all__ = ['BASIC_FORMAT', 'CRITICAL', 'DEBUG', 'ERROR', 'FATAL', 'INFO',
           'NOTSET', 'WARN', 'WARNING',
           'BufferingFormatter', 'Filter', 'Formatter', 'Handler', 'LogRecord',
           'Logger', 'LoggerAdapter', 'Manager', 'PlaceHolder', 'StreamHandler',
           'FileHandler', 'NullHandler', 'RotatingFileHandler', 'TimedRotatingFileHandler',
           'basicConfig', 'critical', 'debug', 'disable', 'error',
           'exception', 'fatal', 'getLevelName', 'getLogger', 'getLoggerClass',
           'info', 'log', 'makeLogRecord', 'setLoggerClass', 'shutdown',
           'warn', 'warning', 'captureWarnings', 'addLevelName', 'lastResort',
           'raiseExceptions', 'getLogRecordFactory', 'setLogRecordFactory',
           # logkissの独自機能
           'KissConsoleHandler', 'ColoredFormatter', 'KissLogger',
           'use_console_handler']

# デバッグモードの設定
DEBUG = os.environ.get('LOGKISS_DEBUG', '').lower() in ('1', 'true', 'yes')

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
debug = logging.debug
info = logging.info
warning = logging.warning
warn = logging.warn
error = logging.error
critical = logging.critical
fatal = logging.fatal
exception = logging.exception
log = logging.log
disable = logging.disable
shutdown = logging.shutdown
addLevelName = logging.addLevelName
getLevelName = logging.getLevelName
makeLogRecord = logging.makeLogRecord
getLogRecordFactory = logging.getLogRecordFactory
setLogRecordFactory = logging.setLogRecordFactory
basicConfig = logging.basicConfig
captureWarnings = logging.captureWarnings

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
lastResort = logging.lastResort
raiseExceptions = logging.raiseExceptions

# カスタムロガークラスを登録
logging.setLoggerClass(KissLogger)

# ルートロガーを取得
root_logger = logging.getLogger()

# 通常のConsoleHandlerを使用する場合のヘルパー関数
def use_console_handler(logger: Optional[logging.Logger] = None) -> None:
    """通常のConsoleHandlerを使用するように設定"""
    if logger is None:
        logger = root_logger
    
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

# getLoggerをカスタマイズ
def getLogger(name: str = None) -> logging.Logger:
    """Get a logger with the specified name.

    Args:
        name (str, optional): Name of the logger. Defaults to None.

    Returns:
        logging.Logger: Logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:  # ハンドラーが設定されていない場合のみ追加
        logger.setLevel(logging.INFO)  # デフォルトレベルをINFOに設定
        handler = KissConsoleHandler()
        handler.setFormatter(ColoredFormatter())
        logger.addHandler(handler)
    return logger

# getLoggerClassをカスタマイズ
def getLoggerClass() -> type:
    """現在のロガークラスを取得"""
    return logging.getLoggerClass()

# setLoggerClassをカスタマイズ
def setLoggerClass(cls: type) -> None:
    """ロガークラスを設定"""
    logging.setLoggerClass(cls)

# ルートロガーを初期化（最初の1回のみ）
if not root_logger.handlers:
    handler = KissConsoleHandler()
    handler.setFormatter(ColoredFormatter())
    root_logger.addHandler(handler)

    # デバッグモードの場合はログレベルをDEBUGに設定
    if DEBUG:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

# バージョン情報
__version__ = '0.1.0'
