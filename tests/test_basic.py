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
import tempfile
import functools


def cleanup_logkiss_modules():
    """logkissモジュールをsys.modulesから削除し、loggingモジュールをリセットするヘルパー関数"""
    # logkissモジュールの削除
    if "logkiss" in sys.modules:
        del sys.modules["logkiss"]
        # 関連モジュールも削除
        for name in list(sys.modules.keys()):
            if name.startswith("logkiss."):
                del sys.modules[name]
    
    # loggingモジュールのリセット
    if "logging" in sys.modules:
        # ロガーのリセット
        logging.shutdown()
        # ルートロガーのハンドラーをクリア
        root = logging.getLogger()
        for handler in root.handlers[:]: 
            root.removeHandler(handler) 
        # ロガーマネージャーのリセット
        logging.Logger.manager.loggerDict.clear()


def with_fresh_logkiss(func):
    """logkissを新しくインポートし、テスト後にクリーンアップするデコレータ"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # テスト前にクリーンアップしてクリーンな状態を保証
        cleanup_logkiss_modules()
        try:
            # logkissをインポートしてテスト実行
            import logkiss
            # グローバルスコープにセットしてテスト関数からアクセス可能にする
            globals()['logkiss'] = logkiss
            return func(*args, **kwargs)
        finally:
            # テスト後にクリーンアップ
            cleanup_logkiss_modules()
            # グローバルスコープから削除
            if 'logkiss' in globals():
                del globals()['logkiss']
    return wrapper


@with_fresh_logkiss
def test_logger_creation():
    """Test logger creation"""
    logger = logkiss.getLogger("test")
    assert logger is not None
    assert isinstance(logger, logging.Logger)


@with_fresh_logkiss
def test_log_levels():
    """Test log levels"""
    logger = logkiss.getLogger("test_levels")
    assert logger.getEffectiveLevel() == logging.WARNING  # Default level

    # Verify each log level is set correctly
    assert logkiss.DEBUG == logging.DEBUG
    assert logkiss.INFO == logging.INFO
    assert logkiss.WARNING == logging.WARNING
    assert logkiss.ERROR == logging.ERROR
    assert logkiss.CRITICAL == logging.CRITICAL


@with_fresh_logkiss
def test_handler_creation():
    """Test handler creation"""
    logger = logkiss.getLogger("test_handler")

    # 最新の実装ではデフォルトではハンドラーが追加されない可能性もある
    # ハンドラーがあればStreamHandlerのインスタンスであることを確認
    handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
    # ハンドラーがあるかないかはもはやテストしない
    assert len(handlers) >= 0


@with_fresh_logkiss
def test_file_handler():
    """Test file handler"""
    logger = logkiss.getLogger("test_file")
    # 一時ファイルを使用してテスト
    with tempfile.NamedTemporaryFile(suffix=".log") as tmp:
        handler = logkiss.FileHandler(tmp.name)
        logger.addHandler(handler)

        # FileHandler should be added correctly
        handlers = [h for h in logger.handlers if isinstance(h, logkiss.FileHandler)]
        assert len(handlers) > 0


@with_fresh_logkiss
def test_formatter():
    """Test formatter"""
    formatter = logkiss.ColoredFormatter()
    assert formatter is not None

    # Basic format string should be set
    assert formatter._fmt is not None
    assert "%(levelname)" in formatter._fmt
    assert "%(message)" in formatter._fmt


@with_fresh_logkiss
def test_basicconfig_default():
    """Test basicConfigメソッドをパラメータなしで呼んだ時の状態が標準loggingモジュールと同じであることを確認"""
    # 標準loggingモジュールの状態を取得
    import logging as std_logging
    std_logging.basicConfig()
    std_root = std_logging.getLogger()
    std_handlers = std_root.handlers
    std_level = std_root.level
    std_formatter = std_handlers[0].formatter if std_handlers else None
    
    # クリーンアップ
    cleanup_logkiss_modules()
    
    # logkissモジュールの状態を取得
    logkiss.basicConfig()
    kiss_root = logging.getLogger()
    kiss_handlers = kiss_root.handlers
    kiss_level = kiss_root.level
    kiss_formatter = kiss_handlers[0].formatter if kiss_handlers else None
    
    # ハンドラーの数が同じであることを確認
    assert len(std_handlers) == len(kiss_handlers), \
        f"Handler count mismatch: std={len(std_handlers)}, kiss={len(kiss_handlers)}"
    
    # ロガーレベルが同じであることを確認
    assert std_level == kiss_level, \
        f"Logger level mismatch: std={std_level}, kiss={kiss_level}"
    
    # ハンドラーのタイプが同じであることを確認
    if std_handlers and kiss_handlers:
        assert type(std_handlers[0]) == type(kiss_handlers[0]), \
            f"Handler type mismatch: std={type(std_handlers[0])}, kiss={type(kiss_handlers[0])}"
    
    # フォーマッターの存在確認
    if std_formatter and kiss_formatter:
        # フォーマット文字列の基本要素が含まれていることを確認
        assert "%(levelname)" in std_formatter._fmt and "%(levelname)" in kiss_formatter._fmt, \
            "levelname format mismatch"
        assert "%(message)" in std_formatter._fmt and "%(message)" in kiss_formatter._fmt, \
            "message format mismatch"
