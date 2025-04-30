"""
環境変数のテストモジュール

このモジュールは、LOGKISSが使用するすべての環境変数の動作を検証します。
"""

import os
import pytest
from unittest import mock
import importlib
import tempfile
import logging

import logkiss
from logkiss.logkiss import ColoredFormatter, KissConsoleHandler


@pytest.mark.env_vars
def test_logkiss_level_format():
    """LOGKISS_LEVEL_FORMAT環境変数のテスト"""
    # デフォルト値のテスト
    with mock.patch.dict(os.environ, {}, clear=True):
        # モジュールレベルの変数をリセット
        importlib.reload(logkiss.logkiss)
        from logkiss.logkiss import LEVEL_FORMAT
        assert LEVEL_FORMAT == 5  # デフォルト値

    # カスタム値のテスト
    with mock.patch.dict(os.environ, {"LOGKISS_LEVEL_FORMAT": "10"}, clear=True):
        importlib.reload(logkiss.logkiss)
        from logkiss.logkiss import LEVEL_FORMAT
        assert LEVEL_FORMAT == 10

    # 無効な値のテスト（デフォルト値を使用するはず）
    with mock.patch.dict(os.environ, {"LOGKISS_LEVEL_FORMAT": "invalid"}, clear=True):
        importlib.reload(logkiss.logkiss)
        from logkiss.logkiss import LEVEL_FORMAT
        assert LEVEL_FORMAT == 5  # デフォルト値


@pytest.mark.env_vars
def test_logkiss_path_shorten():
    """LOGKISS_PATH_SHORTEN環境変数のテスト"""
    # デフォルト値のテスト
    with mock.patch.dict(os.environ, {}, clear=True):
        importlib.reload(logkiss.logkiss)
        from logkiss.logkiss import PATH_SHORTEN
        assert PATH_SHORTEN == 0  # デフォルト値

    # カスタム値のテスト
    with mock.patch.dict(os.environ, {"LOGKISS_PATH_SHORTEN": "3"}, clear=True):
        importlib.reload(logkiss.logkiss)
        from logkiss.logkiss import PATH_SHORTEN
        assert PATH_SHORTEN == 3

    # 無効な値のテスト（デフォルト値を使用するはず）
    with mock.patch.dict(os.environ, {"LOGKISS_PATH_SHORTEN": "invalid"}, clear=True):
        importlib.reload(logkiss.logkiss)
        from logkiss.logkiss import PATH_SHORTEN
        assert PATH_SHORTEN == 0  # デフォルト値


@pytest.mark.env_vars
def test_logkiss_skip_config():
    """LOGKISS_SKIP_CONFIG環境変数のテスト"""
    # デフォルト値のテスト（スキップしない）
    with mock.patch.dict(os.environ, {}, clear=True):
        importlib.reload(logkiss.logkiss)
        assert not logkiss.logkiss.should_skip_config()

    # スキップを有効にしたテスト
    for value in ["1", "true", "yes"]:
        with mock.patch.dict(os.environ, {"LOGKISS_SKIP_CONFIG": value}, clear=True):
            importlib.reload(logkiss.logkiss)
            assert logkiss.logkiss.should_skip_config()

    # 無効な値のテスト（スキップしないはず）
    with mock.patch.dict(os.environ, {"LOGKISS_SKIP_CONFIG": "invalid"}, clear=True):
        importlib.reload(logkiss.logkiss)
        assert not logkiss.logkiss.should_skip_config()


@pytest.mark.env_vars
def test_logkiss_config():
    """LOGKISS_CONFIG環境変数のテスト"""
    # 一時設定ファイルを作成
    with tempfile.NamedTemporaryFile(suffix=".yaml") as temp_file:
        temp_path = temp_file.name
        
        # LOGKISS_CONFIGが設定されている場合のテスト
        with mock.patch.dict(os.environ, {"LOGKISS_CONFIG": temp_path}, clear=True):
            importlib.reload(logkiss.logkiss)
            config_path = logkiss.logkiss.find_config_file()
            assert config_path is not None
            assert str(config_path) == temp_path

        # LOGKISS_CONFIGが設定されていない場合のテスト
        with mock.patch.dict(os.environ, {}, clear=True):
            importlib.reload(logkiss.logkiss)
            # デフォルトの場所に設定ファイルが存在する場合は結果が異なるため、
            # 厳密な結果ではなく、関数が正常に動作することだけを確認
            logkiss.logkiss.find_config_file()  # エラーが発生しないことを確認


@pytest.mark.env_vars
def test_logkiss_disable_color():
    """LOGKISS_DISABLE_COLOR環境変数のテスト"""
    # 既存のハンドラーをクリア
    root_logger = logging.getLogger()
    handlers = root_logger.handlers.copy()
    for handler in handlers:
        root_logger.removeHandler(handler)

    try:
        # デフォルト値のテスト（カラー有効）
        with mock.patch.dict(os.environ, {}, clear=True):
            logger = logkiss.setup_from_env()
            assert logger.handlers
            formatter = logger.handlers[0].formatter
            assert hasattr(formatter, 'use_color')
            assert formatter.use_color  # デフォルトではカラーが有効

        # 既存のハンドラーをクリア
        handlers = root_logger.handlers.copy()
        for handler in handlers:
            root_logger.removeHandler(handler)

        # カラー無効のテスト
        with mock.patch.dict(os.environ, {"LOGKISS_DISABLE_COLOR": "true"}, clear=True):
            logger = logkiss.setup_from_env()
            assert logger.handlers
            formatter = logger.handlers[0].formatter
            assert hasattr(formatter, 'use_color')
            assert not formatter.use_color  # カラーが無効

        # 既存のハンドラーをクリア
        handlers = root_logger.handlers.copy()
        for handler in handlers:
            root_logger.removeHandler(handler)

        # 無効な値のテスト（カラー有効のまま）
        with mock.patch.dict(os.environ, {"LOGKISS_DISABLE_COLOR": "invalid"}, clear=True):
            logger = logkiss.setup_from_env()
            assert logger.handlers
            formatter = logger.handlers[0].formatter
            assert hasattr(formatter, 'use_color')
            assert formatter.use_color  # カラーが有効のまま
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
