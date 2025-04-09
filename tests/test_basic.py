#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic test cases for logkiss.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.
"""

import sys
import logging
import logkiss

def test_logger_creation():
    """Test logger creation"""
    logger = logkiss.getLogger("test")
    assert logger is not None
    assert isinstance(logger, logging.Logger)

def test_log_levels():
    """Test log levels"""
    logger = logkiss.getLogger("test_levels")
    assert logger.level == logging.WARNING  # Default level
    
    # Verify each log level is set correctly
    assert logkiss.DEBUG == logging.DEBUG
    assert logkiss.INFO == logging.INFO
    assert logkiss.WARNING == logging.WARNING
    assert logkiss.ERROR == logging.ERROR
    assert logkiss.CRITICAL == logging.CRITICAL

def test_handler_creation():
    """Test handler creation"""
    logger = logkiss.getLogger("test_handler")
    
    # デフォルトでは少なくとも1つのハンドラーが追加されている
    # 具体的な型ではなく、StreamHandlerのインスタンスであることを確認
    handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
    assert len(handlers) > 0

def test_file_handler():
    """Test file handler"""
    logger = logkiss.getLogger("test_file")
    handler = logkiss.FileHandler("test.log")
    logger.addHandler(handler)
    
    # FileHandler should be added correctly
    handlers = [h for h in logger.handlers if isinstance(h, logkiss.FileHandler)]
    assert len(handlers) > 0

def test_formatter():
    """Test formatter"""
    formatter = logkiss.ColoredFormatter()
    assert formatter is not None
    
    # Basic format string should be set
    assert formatter._fmt is not None
    assert "%(levelname)" in formatter._fmt
    assert "%(message)" in formatter._fmt
