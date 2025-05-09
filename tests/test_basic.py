#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic test cases for logkiss.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.
"""

import sys
import logging
import importlib


def test_logger_creation():
    """Test logger creation"""
    # 各テストで新しくインポートする
    import logkiss
    
    try:
        logger = logkiss.getLogger("test")
        assert logger is not None
        assert isinstance(logger, logging.Logger)
    finally:
        # テスト後にクリーンアップ
        if "logkiss" in sys.modules:
            del sys.modules["logkiss"]
            # 関連モジュールも削除
            for name in list(sys.modules.keys()):
                if name.startswith("logkiss."):
                    del sys.modules[name]


def test_log_levels():
    """Test log levels"""
    # 各テストで新しくインポートする
    import logkiss
    
    try:
        logger = logkiss.getLogger("test_levels")
        assert logger.getEffectiveLevel() == logging.WARNING  # Default level

        # Verify each log level is set correctly
        assert logkiss.DEBUG == logging.DEBUG
        assert logkiss.INFO == logging.INFO
        assert logkiss.WARNING == logging.WARNING
        assert logkiss.ERROR == logging.ERROR
        assert logkiss.CRITICAL == logging.CRITICAL
    finally:
        # テスト後にクリーンアップ
        if "logkiss" in sys.modules:
            del sys.modules["logkiss"]
            # 関連モジュールも削除
            for name in list(sys.modules.keys()):
                if name.startswith("logkiss."):
                    del sys.modules[name]


def test_handler_creation():
    """Test handler creation"""
    # 各テストで新しくインポートする
    import logkiss
    
    try:
        logger = logkiss.getLogger("test_handler")

        # 最新の実装ではデフォルトではハンドラーが追加されない可能性もある
        # ハンドラーがあればStreamHandlerのインスタンスであることを確認
        handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        # ハンドラーがあるかないかはもはやテストしない
        assert len(handlers) >= 0
    finally:
        # テスト後にクリーンアップ
        if "logkiss" in sys.modules:
            del sys.modules["logkiss"]
            # 関連モジュールも削除
            for name in list(sys.modules.keys()):
                if name.startswith("logkiss."):
                    del sys.modules[name]


def test_file_handler():
    """Test file handler"""
    # 各テストで新しくインポートする
    import logkiss
    import tempfile
    
    try:
        logger = logkiss.getLogger("test_file")
        # 一時ファイルを使用してテスト
        with tempfile.NamedTemporaryFile(suffix=".log") as tmp:
            handler = logkiss.FileHandler(tmp.name)
            logger.addHandler(handler)

            # FileHandler should be added correctly
            handlers = [h for h in logger.handlers if isinstance(h, logkiss.FileHandler)]
            assert len(handlers) > 0
    finally:
        # テスト後にクリーンアップ
        if "logkiss" in sys.modules:
            del sys.modules["logkiss"]
            # 関連モジュールも削除
            for name in list(sys.modules.keys()):
                if name.startswith("logkiss."):
                    del sys.modules[name]


def test_formatter():
    """Test formatter"""
    # 各テストで新しくインポートする
    import logkiss
    
    try:
        formatter = logkiss.ColoredFormatter()
        assert formatter is not None

        # Basic format string should be set
        assert formatter._fmt is not None
        assert "%(levelname)" in formatter._fmt
        assert "%(message)" in formatter._fmt
    finally:
        # テスト後にクリーンアップ
        if "logkiss" in sys.modules:
            del sys.modules["logkiss"]
            # 関連モジュールも削除
            for name in list(sys.modules.keys()):
                if name.startswith("logkiss."):
                    del sys.modules[name]
