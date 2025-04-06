"""Test platform-specific functionality.

This module tests platform-specific features and ensures
cross-platform compatibility.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest

import logkiss


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


@pytest.mark.skipif(sys.platform != "darwin", reason="macOS-specific test")
def test_macos_console():
    """Test macOS console output handling."""
    logger = logkiss.getLogger("test_macos")
    assert logger.handlers[0].formatter.use_color
    
    # Test with NO_COLOR environment
    with mock.patch.dict(os.environ, {"NO_COLOR": "1"}):
        logger = logkiss.getLogger("test_macos_no_color")
        assert not logger.handlers[0].formatter.use_color


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


def test_file_paths():
    """Test file path handling across platforms."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create platform-agnostic path
        log_dir = Path(tmpdir) / "logs"
        log_dir.mkdir()
        log_file = log_dir / "test.log"
        
        # Test file handler creation
        logger = logkiss.getLogger("test_paths")
        handler = logging.FileHandler(str(log_file))
        logger.addHandler(handler)
        
        # Test logging
        test_message = "Test message"
        logger.info(test_message)
        
        # Verify file contents
        with open(log_file, "r") as f:
            content = f.read()
            assert test_message in content


def test_config_paths():
    """Test configuration file path handling across platforms."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir) / "config"
        config_dir.mkdir()
        
        # Test with forward slashes
        config1 = config_dir / "test1.yaml"
        with open(config1, "w") as f:
            f.write("version: 1\n")
        
        # Test with backslashes (Windows style)
        config2 = str(config_dir / "test2.yaml").replace("/", "\\")
        with open(config2, "w") as f:
            f.write("version: 1\n")
        
        # Both should work regardless of platform
        logkiss.setup_from_yaml(str(config1))
        logkiss.setup_from_yaml(config2)
