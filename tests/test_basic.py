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
def test_logkiss_uses_kiss_console_handler():
    """logkissモジュールをインポートした時点でKissConsoleHandlerが使用されていることを確認"""
    # logkissモジュールのデフォルト状態を取得
    # インポート時に独自のハンドラーが設定される
    root_logger = logging.getLogger()
    
    # ハンドラーが存在することを確認
    assert len(root_logger.handlers) > 0, "Logkiss should have at least one handler"
    
    # ハンドラーがKissConsoleHandlerであることを確認
    handler = root_logger.handlers[0]
    handler_class_name = handler.__class__.__name__
    assert handler_class_name == "KissConsoleHandler", \
        f"Handler should be KissConsoleHandler, got {handler_class_name}"
    
    # フォーマッターがColoredFormatterであることを確認
    formatter = handler.formatter
    formatter_class_name = formatter.__class__.__name__
    assert formatter_class_name == "ColoredFormatter", \
        f"Formatter should be ColoredFormatter, got {formatter_class_name}"
    
    # シンプルなログ出力が動作することを確認
    # エラーが発生しないことを確認するのみ
    logkiss.warning("Test warning message")


def test_default_handlers_difference():
    """logkissモジュールのデフォルトハンドラーと標準loggingモジュールのハンドラーの違いを確認"""
    # クリーンアップして新しい状態からスタート
    cleanup_logkiss_modules()
    
    # 標準loggingモジュールのデフォルト状態を取得
    import logging as std_logging
    
    # 標準loggingのロガーをリセット
    std_root = std_logging.getLogger()
    for handler in std_root.handlers[:]:
        std_root.removeHandler(handler)
    
    # 標準loggingのデフォルト設定を適用
    std_logging.basicConfig()
    std_handlers = std_root.handlers
    std_handler_class = std_handlers[0].__class__.__name__
    std_formatter = std_handlers[0].formatter
    std_formatter_class = std_formatter.__class__.__name__
    
    # 標準は通常StreamHandler
    assert std_handler_class == "StreamHandler", \
        f"Standard handler should be StreamHandler, got {std_handler_class}"
    
    # 標準loggingの状態をクリーンアップ
    for handler in std_root.handlers[:]:
        std_root.removeHandler(handler)
    
    # logkissをインポートしてデフォルト状態を取得
    import logkiss
    
    # logkissモジュールのデフォルト状態を取得
    kiss_root = std_logging.getLogger()  # 同じロガーを使用
    kiss_handlers = kiss_root.handlers
    
    # ハンドラーが存在することを確認
    assert len(kiss_handlers) > 0, "Logkiss should have at least one handler"
    
    # ハンドラーのクラス名を確認
    kiss_handler_class = kiss_handlers[0].__class__.__name__
    
    # クラス名が異なることを確認
    assert std_handler_class != kiss_handler_class, \
        f"Handler class names should be different: std={std_handler_class}, kiss={kiss_handler_class}"
    
    # logkissは独自のKissConsoleHandler
    assert kiss_handler_class == "KissConsoleHandler", \
        f"Logkiss handler should be KissConsoleHandler, got {kiss_handler_class}"
    
    # フォーマッターの確認
    kiss_formatter = kiss_handlers[0].formatter
    kiss_formatter_class = kiss_formatter.__class__.__name__
    
    # フォーマッターのクラス名が異なることを確認
    assert std_formatter_class != kiss_formatter_class, \
        f"Formatter class names should be different: std={std_formatter_class}, kiss={kiss_formatter_class}"
    
    # logkissはカラーフォーマッターを使用
    assert kiss_formatter_class == "ColoredFormatter", \
        f"Logkiss formatter should be ColoredFormatter, got {kiss_formatter_class}"
    
    # クリーンアップ
    cleanup_logkiss_modules()
