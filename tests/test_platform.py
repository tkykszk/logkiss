"""Test platform-specific functionality.

This module tests platform-specific features and ensures
cross-platform compatibility.
"""

import os
import sys
import logging
from pathlib import Path  # Path is needed for type annotation
from unittest import mock

import pytest
import yaml

import logkiss


@pytest.mark.windows
@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_windows_console():
    """Test Windows console output handling."""
    logger = logkiss.getLogger("test_windows")
    
    # Test with ANSICON environment
    with mock.patch.dict(os.environ, {"ANSICON": "1"}):
        assert logger.handlers[0].formatter.use_color
    
    # Test with NO_COLOR environment
    with mock.patch.dict(os.environ, {"NO_COLOR": "1"}):
        logger = logkiss.getLogger("test_windows_no_color")
        assert not logger.handlers[0].formatter.use_color
    
    # Test with Windows Terminal
    with mock.patch.dict(os.environ, {"WT_SESSION": "1"}):
        logger = logkiss.getLogger("test_wt")
        assert logger.handlers[0].formatter.use_color


@pytest.mark.macos
@pytest.mark.skipif(sys.platform != "darwin", reason="macOS-specific test")
def test_macos_console():
    """Test macOS console output handling."""
    # MacOSのデフォルトターミナルはカラーをサポートしているので、テストを調整
    logger = logkiss.getLogger("test_macos")
    
    # 特定の環境変数でカラーを無効化する
    with mock.patch.dict(os.environ, {"LOGKISS_DISABLE_COLOR": "true"}):
        # 新しいロガーを取得して設定を適用
        logkiss.logging.getLogger().handlers = []
        logger = logkiss.setup_from_env()
        assert not logger.handlers[0].formatter.use_color
    
    # Test with NO_COLOR environment
    with mock.patch.dict(os.environ, {"NO_COLOR": "1"}):
        # 既存のハンドラをクリア
        logkiss.logging.getLogger().handlers = []
        logger = logkiss.getLogger("test_macos_no_color")
        assert not logger.handlers[0].formatter.use_color


@pytest.mark.linux
@pytest.mark.skipif(sys.platform != "linux", reason="Linux-specific test")
def test_linux_console():
    """Test Linux console output handling."""
    logger = logkiss.getLogger("test_linux")
    
    # Test with TERM environment
    with mock.patch.dict(os.environ, {"TERM": "xterm-256color"}):
        assert logger.handlers[0].formatter.use_color
    
    # Test with NO_COLOR environment
    with mock.patch.dict(os.environ, {"NO_COLOR": "1"}):
        logger = logkiss.getLogger("test_linux_no_color")
        assert not logger.handlers[0].formatter.use_color


def test_file_paths(tmp_path):
    """Test file path handling across platforms."""
    # Create platform-agnostic path
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    log_file = log_dir / "test.log"
    
    # 既存のハンドラをクリア
    logger = logkiss.getLogger("test_paths")
    for h in logger.handlers.copy():
        logger.removeHandler(h)
    
    # ファイルハンドラを設定
    handler = logging.FileHandler(str(log_file), mode='w')
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # テストメッセージを書き込む
    test_message = "Test message"
    logger.info(test_message)
    
    # ハンドラをフラッシュして閉じる
    handler.flush()
    handler.close()
    
    # ファイルの内容を読み込んで検証
    with open(str(log_file), 'r') as f:
        content = f.read()
        assert test_message in content


@pytest.mark.config
def test_config_paths(tmp_path):
    """Test configuration file path handling across platforms."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    config = {
        "version": 1,
        "root": {
            "level": "INFO"
        }
    }
    
    # Test with forward slashes
    config1 = config_dir / "test1.yaml"
    with config1.open("w") as f:
        yaml.safe_dump(config, f)
    
    # Test with backslashes (Windows style)
    config2 = config_dir / "test2.yaml"
    with config2.open("w") as f:
        yaml.safe_dump(config, f)
    
    # Both should work regardless of platform
    logger1 = logkiss.setup_from_yaml(str(config1))
    assert logger1.level == logkiss.INFO
    
    # Use os.path.normpath to handle path separators in a platform-independent way
    config2_path = os.path.normpath(str(config2))
    logger2 = logkiss.setup_from_yaml(config2_path)
    assert logger2.level == logkiss.INFO
