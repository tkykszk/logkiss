#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import logkiss

def test_logger_creation():
    """ロガーの作成テスト"""
    logger = logkiss.getLogger("test")
    assert logger is not None
    assert isinstance(logger, logging.Logger)

def test_log_levels():
    """ログレベルのテスト"""
    logger = logkiss.getLogger("test_levels")
    assert logger.level == logging.INFO  # デフォルトレベル
    
    # 各ログレベルが正しく設定されているか確認
    assert logkiss.DEBUG == logging.DEBUG
    assert logkiss.INFO == logging.INFO
    assert logkiss.WARNING == logging.WARNING
    assert logkiss.ERROR == logging.ERROR
    assert logkiss.CRITICAL == logging.CRITICAL

def test_handler_creation():
    """ハンドラーの作成テスト"""
    logger = logkiss.getLogger("test_handler")
    
    # デフォルトのハンドラーがKissConsoleHandlerであることを確認
    handlers = [h for h in logger.handlers if isinstance(h, logkiss.KissConsoleHandler)]
    assert len(handlers) > 0

def test_file_handler():
    """FileHandlerのテスト"""
    logger = logkiss.getLogger("test_file")
    handler = logkiss.FileHandler("test.log")
    logger.addHandler(handler)
    
    # FileHandlerが正しく追加されたか確認
    handlers = [h for h in logger.handlers if isinstance(h, logkiss.FileHandler)]
    assert len(handlers) > 0

def test_formatter():
    """フォーマッターのテスト"""
    formatter = logkiss.ColoredFormatter()
    assert formatter is not None
    
    # 基本的なフォーマット文字列が設定されているか確認
    assert formatter._fmt is not None
    assert "%(levelname)" in formatter._fmt
    assert "%(message)" in formatter._fmt
