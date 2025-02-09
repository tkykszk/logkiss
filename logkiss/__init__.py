#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import logging.handlers
from logging import *
from pathlib import Path
from typing import Optional, Union, Dict, Any

from .logkiss import KissLogger, KissConsoleHandler, ColoredFormatter

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
DEBUG = os.environ.get('LOGKISS_DEBUG', '0').lower() in ('1', 'true', 'yes')

# lastResortハンドラーをKissConsoleHandlerに設定
lastResort = KissConsoleHandler(sys.stderr)
lastResort.setLevel(logging.WARNING)
lastResort.setFormatter(ColoredFormatter())
logging.lastResort = lastResort

# ルートロガーを取得
root = KissLogger('root')
root.setLevel(logging.DEBUG if DEBUG else logging.INFO)
root.addHandler(lastResort)

# loggingモジュールの関数をオーバーライド
def debug(msg: str, *args, **kwargs):
    """DEBUGレベルのログを出力"""
    logger = KissLogger(__name__)
    # ファイル名と行番号を取得
    fn = sys._getframe().f_back.f_code.co_filename
    lno = sys._getframe().f_back.f_lineno
    # ログを出力
    logger.debug(msg, *args, extra={'_filename': fn, '_lineno': lno})

def info(msg: str, *args, **kwargs):
    """INFOレベルのログを出力"""
    logger = KissLogger(__name__)
    # ファイル名と行番号を取得
    fn = sys._getframe().f_back.f_code.co_filename
    lno = sys._getframe().f_back.f_lineno
    # ログを出力
    logger.info(msg, *args, extra={'_filename': fn, '_lineno': lno})

def warning(msg: str, *args, **kwargs):
    """WARNINGレベルのログを出力"""
    logger = KissLogger(__name__)
    # ファイル名と行番号を取得
    fn = sys._getframe().f_back.f_code.co_filename
    lno = sys._getframe().f_back.f_lineno
    # ログを出力
    logger.warning(msg, *args, extra={'_filename': fn, '_lineno': lno})

def error(msg: str, *args, **kwargs):
    """ERRORレベルのログを出力"""
    logger = KissLogger(__name__)
    # ファイル名と行番号を取得
    fn = sys._getframe().f_back.f_code.co_filename
    lno = sys._getframe().f_back.f_lineno
    # ログを出力
    logger.error(msg, *args, extra={'_filename': fn, '_lineno': lno})

def critical(msg: str, *args, **kwargs):
    """CRITICALレベルのログを出力"""
    logger = KissLogger(__name__)
    # ファイル名と行番号を取得
    fn = sys._getframe().f_back.f_code.co_filename
    lno = sys._getframe().f_back.f_lineno
    # ログを出力
    logger.critical(msg, *args, extra={'_filename': fn, '_lineno': lno})

warn = warning

def exception(msg, *args, exc_info=True, **kwargs):
    """例外情報付きのエラーメッセージを出力"""
    root = getLogger()
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['filename'] = sys._getframe().f_back.f_code.co_filename
    kwargs['extra']['lineno'] = sys._getframe().f_back.f_lineno
    root.exception(msg, *args, exc_info=exc_info, **kwargs)

def log(level, msg, *args, **kwargs):
    """指定したレベルのメッセージを出力"""
    root = getLogger()
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    kwargs['extra']['filename'] = sys._getframe().f_back.f_code.co_filename
    kwargs['extra']['lineno'] = sys._getframe().f_back.f_lineno
    root.log(level, msg, *args, **kwargs)

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
getLogRecordFactory = logging.getLogRecordFactory
setLogRecordFactory = logging.setLogRecordFactory

def basicConfig(**kwargs):
    """標準のbasicConfigをオーバーライドしてKissConsoleHandlerを使用"""
    root = logging.getLogger()

    # すでにハンドラーが設定されている場合は何もしない
    if root.handlers:
        return

    # レベルの設定
    level = kwargs.get('level', logging.INFO)
    root.setLevel(level)

    # 既存のハンドラーを削除
    for handler in root.handlers[:]:
        root.removeHandler(handler)

    # KissConsoleHandlerを追加
    handler = KissConsoleHandler()
    handler.setLevel(level)
    root.addHandler(handler)

def getLogger(name: str = None) -> logging.Logger:
    """Get a logger with the specified name.

    Args:
        name (str, optional): Name of the logger. Defaults to None.

    Returns:
        logging.Logger: Logger instance
    """
    logger = logging.getLogger(name)
    
    # ハンドラーが設定されていない場合のみ追加
    has_kiss_handler = any(isinstance(h, KissConsoleHandler) for h in logger.handlers)
    if not has_kiss_handler and not logger.handlers:  # 他のハンドラーもない場合のみ
        level = logging.DEBUG if DEBUG else logging.INFO
        logger.setLevel(level)
        handler = KissConsoleHandler()
        handler.setLevel(level)
        logger.addHandler(handler)
        
        # 名前付きロガーの場合は伝播を無効化
        if name is not None:
            logger.propagate = False
    
    return logger

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

# カスタムロガークラスを登録
logging.setLoggerClass(KissLogger)

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
