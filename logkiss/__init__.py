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
    KissFileHandler, KissRotatingFileHandler, KissTimedRotatingFileHandler,
)

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
    'BASIC_FORMAT', 'CRITICAL', 'DEBUG', 'ERROR', 'FATAL', 'INFO',
    'NOTSET', 'WARN', 'WARNING', 'addLevelName', 'basicConfig',
    'critical', 'debug', 'disable', 'error', 'exception', 'fatal',
    'getLevelName', 'getLogger', 'getLoggerClass', 'info', 'log',
    'makeLogRecord', 'setLoggerClass', 'warn', 'warning',
]

# Register custom logger class
logging.setLoggerClass(KissLogger)

# Initialize root logger
root_logger = KissLogger('root')
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)
handler = KissConsoleHandler()
root_logger.addHandler(handler)
root_logger.setLevel(WARNING)  # Default to WARNING level

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
        # Use existing handlers for root logger
        return root_logger
    if not logger.handlers:
        handler = KissConsoleHandler()
        handler.setLevel(INFO)  # Set logger level to INFO
        logger.addHandler(handler)
    else:
        # Update handler levels
        for handler in logger.handlers:
            handler.setLevel(INFO)
    return logger

# Reset root logger
logging.getLogger = getLogger
logging.root = root_logger

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
    """Use standard ConsoleHandler"""
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
__version__ = '2.1.0'
