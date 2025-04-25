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
from logkiss.logkiss import KissConsoleHandler, StreamHandler


def test_use_console_handler():
    """use_console_handler 関数のテスト"""
    # テスト用のロガーを作成
    logger = logging.getLogger("test_console_handler")
    logger.setLevel(logging.DEBUG)

    # 既存のハンドラーをクリア
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 標準エラー出力をキャプチャするための設定
    original_stderr = sys.stderr
    captured_stderr = io.StringIO()
    sys.stderr = captured_stderr

    try:
        # console_handler を使用
        logkiss.use_console_handler(logger)

        # ハンドラーが追加されたことを確認
        assert len(logger.handlers) == 1
        handler = logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler)

        # フォーマッターが正しく設定されていることを確認
        formatter = handler.formatter
        assert formatter is not None
        assert "%(asctime)s" in formatter._fmt
        assert "%(levelname)" in formatter._fmt
        assert "%(filename)s" in formatter._fmt
        assert "%(lineno)" in formatter._fmt
        assert "%(message)s" in formatter._fmt

        # ログ出力のテスト
        logger.info("テストメッセージ")
        output = captured_stderr.getvalue()

        # 出力形式の確認
        assert "INFO" in output
        assert "test_console_handler.py" in output
        assert "テストメッセージ" in output

    finally:
        # 標準エラー出力を元に戻す
        sys.stderr = original_stderr


def test_use_console_handler_with_root_logger():
    """ルートロガーに対する use_console_handler 関数のテスト"""
    # ルートロガーを取得
    root_logger = logging.getLogger()
    original_level = root_logger.level

    # 既存のハンドラーを保存
    original_handlers = root_logger.handlers[:]

    # ハンドラーをクリア
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    try:
        # ルートロガーに console_handler を使用
        logkiss.use_console_handler()

        # ハンドラーが追加されたことを確認
        assert len(root_logger.handlers) == 1
        handler = root_logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler)

        # フォーマッターが正しく設定されていることを確認
        formatter = handler.formatter
        assert formatter is not None

    finally:
        # ルートロガーを元の状態に戻す
        root_logger.setLevel(original_level)

        # ハンドラーをクリア
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # 元のハンドラーを復元
        for handler in original_handlers:
            root_logger.addHandler(handler)


def test_use_console_handler_removes_kiss_console_handler():
    """KissConsoleHandler が削除されることを確認するテスト"""
    # テスト用のロガーを作成
    logger = logging.getLogger("test_remove_kiss_handler")
    logger.setLevel(logging.DEBUG)

    # 既存のハンドラーをクリア
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # モックではなく実際の KissConsoleHandler クラスを使用
    # KissConsoleHandler を追加
    kiss_handler = KissConsoleHandler()
    logger.addHandler(kiss_handler)

    # console_handler を使用
    logkiss.use_console_handler(logger)

    # KissConsoleHandler が削除され、新しいハンドラーが追加されたことを確認
    assert len(logger.handlers) == 1
    assert not isinstance(logger.handlers[0], KissConsoleHandler)
    assert isinstance(logger.handlers[0], StreamHandler)
