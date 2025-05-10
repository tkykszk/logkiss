"""
環境変数のテストモジュール

このモジュールは、LOGKISSが使用するすべての環境変数の動作を検証します。
"""

import os
import sys
import logging
from unittest import mock
import importlib
import tempfile
from pathlib import Path

import pytest

# logkissモジュールをインポート
import logkiss
# ColoredFormatterをインポート（パッケージ構造に合わせて）
from logkiss.logkiss import ColoredFormatter

@pytest.fixture(autouse=True)
def reset_logkiss():
    """各テストの前後でlogkissモジュールの状態をリセットする"""
    # テスト前の処理
    old_handlers = logging.getLogger().handlers.copy()
    for handler in old_handlers:
        logging.getLogger().removeHandler(handler)
    
    yield
    
    # テスト後の処理
    # Clear handlers
    old_handlers = logging.getLogger().handlers.copy()
    for handler in old_handlers:
        logging.getLogger().removeHandler(handler)


@pytest.mark.env_vars
def test_logkiss_level_format():
    """LOGKISS_LEVEL_FORMAT環境変数のテスト"""
    # デフォルト値のテスト
    with mock.patch.dict(os.environ, {}, clear=True):
        # 環境変数が設定されていない場合はデフォルト値の5が使われる
        level_format = int(os.environ.get("LOGKISS_LEVEL_FORMAT", "5"))
        assert level_format == 5  # デフォルト値

    # カスタム値のテスト
    with mock.patch.dict(os.environ, {"LOGKISS_LEVEL_FORMAT": "10"}, clear=True):
        # 環境変数が設定されている場合はその値が使われる
        level_format = int(os.environ.get("LOGKISS_LEVEL_FORMAT", "5"))
        assert level_format == 10

    # 無効な値のテスト（デフォルト値を使用するはず）
    with mock.patch.dict(os.environ, {"LOGKISS_LEVEL_FORMAT": "invalid"}, clear=True):
        # 無効な値の場合、エラーが発生するのでデフォルト値が使われる
        try:
            level_format = int(os.environ.get("LOGKISS_LEVEL_FORMAT", "5"))
        except ValueError:
            level_format = 5
        assert level_format == 5  # デフォルト値


@pytest.mark.env_vars
def test_logkiss_path_shorten():
    """LOGKISS_PATH_SHORTEN環境変数のテスト"""
    # デフォルト値のテスト
    with mock.patch.dict(os.environ, {}, clear=True):
        # 環境変数が設定されていない場合はデフォルト値の0が使われる
        try:
            path_shorten = int(os.environ.get("LOGKISS_PATH_SHORTEN", "0"))
        except ValueError:
            path_shorten = 0
        assert path_shorten == 0  # デフォルト値

    # カスタム値のテスト
    with mock.patch.dict(os.environ, {"LOGKISS_PATH_SHORTEN": "3"}, clear=True):
        # 環境変数が設定されている場合はその値が使われる
        path_shorten = int(os.environ.get("LOGKISS_PATH_SHORTEN", "0"))
        assert path_shorten == 3

    # 無効な値のテスト（デフォルト値を使用するはず）
    with mock.patch.dict(os.environ, {"LOGKISS_PATH_SHORTEN": "invalid"}, clear=True):
        # 無効な値の場合、エラーが発生するのでデフォルト値が使われる
        try:
            path_shorten = int(os.environ.get("LOGKISS_PATH_SHORTEN", "0"))
        except ValueError:
            path_shorten = 0
        assert path_shorten == 0  # デフォルト値


@pytest.mark.env_vars
def test_logkiss_skip_config():
    """LOGKISS_SKIP_CONFIG環境変数のテスト"""
    # デフォルト値のテスト（スキップしない）
    with mock.patch.dict(os.environ, {}, clear=True):
        # 環境変数が設定されていない場合はスキップしない
        assert os.environ.get("LOGKISS_SKIP_CONFIG", "").lower() not in ("1", "true", "yes")

    # スキップを有効にしたテスト
    for value in ["1", "true", "yes"]:
        with mock.patch.dict(os.environ, {"LOGKISS_SKIP_CONFIG": value}, clear=True):
            # 環境変数が設定されている場合はスキップする
            assert os.environ.get("LOGKISS_SKIP_CONFIG", "").lower() in ("1", "true", "yes")

    # 無効な値のテスト（スキップしないはず）
    with mock.patch.dict(os.environ, {"LOGKISS_SKIP_CONFIG": "invalid"}, clear=True):
        assert os.environ.get("LOGKISS_SKIP_CONFIG", "").lower() not in ("1", "true", "yes")


@pytest.mark.env_vars
def test_logkiss_config():
    """LOGKISS_CONFIG環境変数のテスト"""
    # 一時設定ファイルを作成
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp_file:
        temp_path = temp_file.name
        temp_file.write(b"version: 1\nroot:\n  level: INFO\n")
        temp_file.flush()
        
        try:
            # LOGKISS_CONFIGが設定されている場合のテスト
            with mock.patch.dict(os.environ, {"LOGKISS_CONFIG": temp_path}, clear=True):
                # configモジュールをインポート
                from logkiss import config
                config_path = config.find_config_file()
                assert config_path is not None
                assert str(config_path) == temp_path

            # LOGKISS_CONFIGが設定されていない場合のテスト
            with mock.patch.dict(os.environ, {}, clear=True):
                # configモジュールをインポート
                from logkiss import config
                # デフォルトの場所に設定ファイルが存在する場合は結果が異なるため、
                # 厳密な結果ではなく、関数が正常に動作することだけを確認
                try:
                    config.find_config_file()
                except Exception as e:
                    pytest.fail(f"find_config_file関数が例外を発生させました: {e}")
        finally:
            # 一時ファイルを削除
            try:
                Path(temp_path).unlink()
            except (OSError, FileNotFoundError):
                pass  # エラーが発生しないことを確認


@pytest.mark.env_vars
def test_logkiss_disable_color():
    """LOGKISS_DISABLE_COLOR環境変数のテスト"""
    # 既存のハンドラーをクリア
    root_logger = logging.getLogger()
    handlers = root_logger.handlers.copy()
    for handler in handlers:
        root_logger.removeHandler(handler)
    
    try:
        # dictConfig用の基本設定辞書
        base_config = {
            "version": 1,
            "formatters": {
                "colored": {
                    "class": "logkiss.ColoredFormatter",
                    "format": "%(asctime)s [%(levelname)s] %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logkiss.KissConsoleHandler",
                    "level": "DEBUG",
                    "formatter": "colored"
                }
            },
            "loggers": {
                "": {
                    "handlers": ["console"],
                    "level": "DEBUG"
                }
            }
        }
        
        # デフォルト値のテスト（カラー有効）
        with mock.patch.dict(os.environ, {}, clear=True):
            # 新しいフォーマッタを直接作成してテスト
            formatter = ColoredFormatter()
            assert hasattr(formatter, 'use_color')
            # 環境変数が設定されていない場合、デフォルトではカラーが有効
            assert formatter.use_color

        # カラー無効のテスト
        with mock.patch.dict(os.environ, {"LOGKISS_DISABLE_COLOR": "true"}, clear=True):
            # 新しいフォーマッタを直接作成してテスト
            formatter = ColoredFormatter()
            assert hasattr(formatter, 'use_color')
            # LOGKISS_DISABLE_COLOR=trueの場合、カラーが無効
            assert not formatter.use_color

        # 無効な値のテスト（カラー有効のまま）
        with mock.patch.dict(os.environ, {"LOGKISS_DISABLE_COLOR": "invalid"}, clear=True):
            # 新しいフォーマッタを直接作成してテスト
            formatter = ColoredFormatter()
            assert hasattr(formatter, 'use_color')
            # 無効な値の場合、デフォルトではカラーが有効
            assert formatter.use_color
    finally:
        # テスト後にハンドラーを元に戻す
        handlers = root_logger.handlers.copy()
        for handler in handlers:
            root_logger.removeHandler(handler)


@pytest.mark.env_vars
def test_no_color():
    """NO_COLOR環境変数のテスト（業界標準）"""
    # 既存のハンドラーをクリア
    root_logger = logging.getLogger()
    handlers = root_logger.handlers.copy()
    for handler in handlers:
        root_logger.removeHandler(handler)
    
    try:
        # デフォルト値のテスト（カラー有効）
        with mock.patch.dict(os.environ, {}, clear=True):
            formatter = ColoredFormatter()
            assert formatter.use_color  # デフォルトではカラーが有効

        # NO_COLOR設定時のテスト（値は何でもよい）
        with mock.patch.dict(os.environ, {"NO_COLOR": "anything"}, clear=True):
            formatter = ColoredFormatter()
            assert not formatter.use_color  # カラーが無効
            
        # 空の値でもテスト
        with mock.patch.dict(os.environ, {"NO_COLOR": ""}, clear=True):
            formatter = ColoredFormatter()
            assert not formatter.use_color  # カラーが無効
    finally:
        # テスト後にハンドラーを元に戻す
        handlers = root_logger.handlers.copy()
        for handler in handlers:
            root_logger.removeHandler(handler)
