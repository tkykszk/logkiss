"""
logkiss の console_handler のテスト

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
"""

import io
import sys
import logging
import pytest
import logkiss
from logkiss.logkiss import KissConsoleHandler
from logging import StreamHandler


def test_use_console_handler():
    """use_console_handler 関数のテスト"""
    # Create a logger for testing
    logger = logging.getLogger("test_console_handler")
    logger.setLevel(logging.DEBUG)

    # 既存のハンドラーをクリア
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Setup to capture standard error output
    original_stderr = sys.stderr
    captured_stderr = io.StringIO()
    sys.stderr = captured_stderr

    try:
        # Use console_handler
        logkiss.use_console_handler(logger)

        # Verify that the handler was added
        assert len(logger.handlers) == 1
        handler = logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler)

        # Verify that the formatter is correctly configured
        formatter = handler.formatter
        assert formatter is not None
        assert "%(asctime)s" in formatter._fmt
        assert "%(levelname)" in formatter._fmt
        assert "%(filename)s" in formatter._fmt
        assert "%(lineno)" in formatter._fmt
        assert "%(message)s" in formatter._fmt

        # Test log output
        logger.info("テストメッセージ")
        output = captured_stderr.getvalue()

        # Check output format
        assert "INFO" in output
        assert "test_console_handler.py" in output
        assert "テストメッセージ" in output

    finally:
        # Restore standard error output
        sys.stderr = original_stderr


def test_use_console_handler_with_root_logger():
    """ルートロガーに対する use_console_handler 関数のテスト"""
    # Get the root logger
    root_logger = logging.getLogger()
    original_level = root_logger.level

    # Save existing handlers
    original_handlers = root_logger.handlers[:]

    # Clear handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    try:
        # Use console_handler with the root logger
        logkiss.use_console_handler()

        # Verify that the handler was added
        assert len(root_logger.handlers) == 1
        handler = root_logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler)

        # Verify that the formatter is correctly configured
        formatter = handler.formatter
        assert formatter is not None

    finally:
        # ルートロガーを元の状態に戻す
        root_logger.setLevel(original_level)

        # Clear handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # 元のハンドラーを復元
        for handler in original_handlers:
            root_logger.addHandler(handler)


def test_use_console_handler_removes_kiss_console_handler():
    """KissConsoleHandler が削除されることを確認するテスト"""
    # Create a logger for testing
    logger = logging.getLogger("test_remove_kiss_handler")
    logger.setLevel(logging.DEBUG)

    # 既存のハンドラーをクリア
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # モックではなく実際の KissConsoleHandler クラスを使用
    # KissConsoleHandler を追加
    kiss_handler = KissConsoleHandler()
    logger.addHandler(kiss_handler)

    # Use console_handler
    logkiss.use_console_handler(logger)

    # KissConsoleHandler が削除され、新しいハンドラーが追加されたことを確認
    assert len(logger.handlers) == 1
    assert not isinstance(logger.handlers[0], KissConsoleHandler)
    
    # ハンドラーの型をチェック - StreamHandlerまたはその派生クラスであることを確認
    # logkiss.logkiss.StreamHandlerとlogging.StreamHandlerのどちらも許容する
    assert hasattr(logger.handlers[0], 'stream'), "ハンドラーにstreamプロパティがありません"
    assert callable(getattr(logger.handlers[0], 'emit', None)), "ハンドラーにemitメソッドがありません"
    
    # ハンドラーのクラス名をチェック
    handler_class_name = logger.handlers[0].__class__.__name__
    assert "StreamHandler" in handler_class_name, f"ハンドラーの型が不正です: {handler_class_name}"
