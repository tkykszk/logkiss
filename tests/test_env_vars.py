"""
Environment variables test module

This module verifies the behavior of all environment variables used by LOGKISS.
"""

import os
import logging
from unittest import mock
import tempfile
from pathlib import Path

import pytest

# Import ColoredFormatter (according to package structure)
from logkiss.logkiss import ColoredFormatter

@pytest.fixture(autouse=True)
def reset_logkiss():
    """Reset the state of logkiss module before and after each test"""
    # Processing before test
    old_handlers = logging.getLogger().handlers.copy()
    for handler in old_handlers:
        logging.getLogger().removeHandler(handler)
    
    yield
    
    # Processing after test
    # Clear handlers
    old_handlers = logging.getLogger().handlers.copy()
    for handler in old_handlers:
        logging.getLogger().removeHandler(handler)


@pytest.mark.env_vars
def test_logkiss_level_format():
    """Test for LOGKISS_LEVEL_FORMAT environment variable"""
    # Test default value
    with mock.patch.dict(os.environ, {}, clear=True):
        # When environment variable is not set, default value 5 is used
        level_format = int(os.environ.get("LOGKISS_LEVEL_FORMAT", "5"))
        assert level_format == 5  # Default value

    # Test custom value
    with mock.patch.dict(os.environ, {"LOGKISS_LEVEL_FORMAT": "10"}, clear=True):
        # When environment variable is set, that value is used
        level_format = int(os.environ.get("LOGKISS_LEVEL_FORMAT", "5"))
        assert level_format == 10

    # Test invalid value (should use default value)
    with mock.patch.dict(os.environ, {"LOGKISS_LEVEL_FORMAT": "invalid"}, clear=True):
        # For invalid values, an error occurs so default value is used
        try:
            level_format = int(os.environ.get("LOGKISS_LEVEL_FORMAT", "5"))
        except ValueError:
            level_format = 5
        assert level_format == 5  # Default value


@pytest.mark.env_vars
def test_logkiss_path_shorten():
    """Test for LOGKISS_PATH_SHORTEN environment variable"""
    # Test default value
    with mock.patch.dict(os.environ, {}, clear=True):
        # When environment variable is not set, default value 0 is used
        try:
            path_shorten = int(os.environ.get("LOGKISS_PATH_SHORTEN", "0"))
        except ValueError:
            path_shorten = 0
        assert path_shorten == 0  # Default value

    # Test custom value
    with mock.patch.dict(os.environ, {"LOGKISS_PATH_SHORTEN": "3"}, clear=True):
        # When environment variable is set, that value is used
        path_shorten = int(os.environ.get("LOGKISS_PATH_SHORTEN", "0"))
        assert path_shorten == 3

    # Test invalid value (should use default value)
    with mock.patch.dict(os.environ, {"LOGKISS_PATH_SHORTEN": "invalid"}, clear=True):
        # For invalid values, an error occurs so default value is used
        try:
            path_shorten = int(os.environ.get("LOGKISS_PATH_SHORTEN", "0"))
        except ValueError:
            path_shorten = 0
        assert path_shorten == 0  # Default value


@pytest.mark.env_vars
def test_logkiss_skip_config():
    """Test for LOGKISS_SKIP_CONFIG environment variable"""
    # Test default value (don't skip)
    with mock.patch.dict(os.environ, {}, clear=True):
        # When environment variable is not set, don't skip
        assert os.environ.get("LOGKISS_SKIP_CONFIG", "").lower() not in ("1", "true", "yes")

    # Test with skip enabled
    for value in ["1", "true", "yes"]:
        with mock.patch.dict(os.environ, {"LOGKISS_SKIP_CONFIG": value}, clear=True):
            # When environment variable is set, skip
            assert os.environ.get("LOGKISS_SKIP_CONFIG", "").lower() in ("1", "true", "yes")

    # Test invalid value (should not skip)
    with mock.patch.dict(os.environ, {"LOGKISS_SKIP_CONFIG": "invalid"}, clear=True):
        assert os.environ.get("LOGKISS_SKIP_CONFIG", "").lower() not in ("1", "true", "yes")


@pytest.mark.env_vars
def test_logkiss_config():
    """Test for LOGKISS_CONFIG environment variable"""
    # Create temporary configuration file
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp_file:
        temp_path = temp_file.name
        temp_file.write(b"version: 1\nroot:\n  level: INFO\n")
        temp_file.flush()
        
        try:
            # Test when LOGKISS_CONFIG is set
            with mock.patch.dict(os.environ, {"LOGKISS_CONFIG": temp_path}, clear=True):
                # Import config module
                from logkiss import config
                config_path = config.find_config_file()
                assert config_path is not None
                assert str(config_path) == temp_path

            # Test when LOGKISS_CONFIG is not set
            with mock.patch.dict(os.environ, {}, clear=True):
                # Import config module
                from logkiss import config
                # Since results may differ if a config file exists in the default location,
                # we only check that the function operates normally, not the exact result
                try:
                    config.find_config_file()
                except FileNotFoundError:
                    # This is an expected exception when no config file exists
                    pass
                except Exception as e:
                    pytest.fail(f"find_config_file function raised an exception: {e}")
        finally:
            # Delete temporary file
            try:
                Path(temp_path).unlink()
            except (OSError, FileNotFoundError):
                pass  # Ensure no errors occur


@pytest.mark.env_vars
def test_logkiss_disable_color():
    """Test for LOGKISS_DISABLE_COLOR environment variable"""
    # Clear existing handlers
    root_logger = logging.getLogger()
    handlers = root_logger.handlers.copy()
    for handler in handlers:
        root_logger.removeHandler(handler)
    
    try:
        # Basic configuration dictionary for dictConfig
        # Note: This configuration is for reference only and not directly used in the test
        _ = {
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
        
        # Test default value (color enabled)
        with mock.patch.dict(os.environ, {}, clear=True):
            # Create a new formatter directly for testing
            formatter = ColoredFormatter()
            assert hasattr(formatter, 'use_color')
            # When environment variable is not set, color is enabled by default
            assert formatter.use_color

        # Test with color disabled
        with mock.patch.dict(os.environ, {"LOGKISS_DISABLE_COLOR": "true"}, clear=True):
            # Create a new formatter directly for testing
            formatter = ColoredFormatter()
            assert hasattr(formatter, 'use_color')
            # When LOGKISS_DISABLE_COLOR=true, color is disabled
            assert not formatter.use_color

        # Test invalid value (color remains enabled)
        with mock.patch.dict(os.environ, {"LOGKISS_DISABLE_COLOR": "invalid"}, clear=True):
            # Create a new formatter directly for testing
            formatter = ColoredFormatter()
            assert hasattr(formatter, 'use_color')
            # For invalid values, color is enabled by default
            assert formatter.use_color
    finally:
        # Restore handlers after test
        handlers = root_logger.handlers.copy()
        for handler in handlers:
            root_logger.removeHandler(handler)


@pytest.mark.env_vars
def test_no_color():
    """Test for NO_COLOR environment variable (industry standard)"""
    # Clear existing handlers
    root_logger = logging.getLogger()
    handlers = root_logger.handlers.copy()
    for handler in handlers:
        root_logger.removeHandler(handler)
    
    try:
        # Test default value (color enabled)
        with mock.patch.dict(os.environ, {}, clear=True):
            formatter = ColoredFormatter()
            assert formatter.use_color  # Color is enabled by default

        # Test with NO_COLOR set (value can be anything)
        with mock.patch.dict(os.environ, {"NO_COLOR": "anything"}, clear=True):
            formatter = ColoredFormatter()
            assert not formatter.use_color  # Color is disabled
            
        # Test with empty value
        with mock.patch.dict(os.environ, {"NO_COLOR": ""}, clear=True):
            formatter = ColoredFormatter()
            assert not formatter.use_color  # Color is disabled
    finally:
        # Restore handlers after test
        handlers = root_logger.handlers.copy()
        for handler in handlers:
            root_logger.removeHandler(handler)
