"""Test configuration functionality of logkiss.

This module tests the configuration loading and management functionality,
including YAML config files, environment variables, and priority handling.
"""

import os
import tempfile
from pathlib import Path
from unittest import mock

import pytest
import yaml

import logkiss


def test_load_yaml_config():
    """Test loading configuration from YAML file."""
    config = {
        "version": 1,
        "formatters": {
            "simple": {
                "format": "%(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"]
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config, f)
        config_path = f.name
    
    try:
        # Test loading the config
        logger = logkiss.setup_from_yaml(config_path)
        assert logger is not None
        assert logger.level == logkiss.INFO
    finally:
        os.unlink(config_path)


def test_env_var_config():
    """Test configuration through environment variables."""
    with mock.patch.dict(os.environ, {
        'LOGKISS_LEVEL': 'DEBUG',
        'LOGKISS_FORMAT': '%(asctime)s - %(levelname)s - %(message)s',
        'LOGKISS_DISABLE_COLOR': 'true'
    }):
        logger = logkiss.setup_from_env()
        assert logger.level == logkiss.DEBUG
        assert not logger.handlers[0].formatter.use_color


def test_config_priority():
    """Test configuration priority (env vars should override file config)."""
    config = {
        "version": 1,
        "root": {
            "level": "WARNING"
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config, f)
        config_path = f.name
    
    try:
        with mock.patch.dict(os.environ, {'LOGKISS_LEVEL': 'DEBUG'}):
            logger = logkiss.setup_from_yaml(config_path)
            assert logger.level == logkiss.DEBUG  # env var should override file
    finally:
        os.unlink(config_path)


def test_invalid_config():
    """Test handling of invalid configuration."""
    with pytest.raises(ValueError):
        logkiss.setup_from_yaml("nonexistent.yaml")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("invalid: yaml: content:")
        config_path = f.name
    
    try:
        with pytest.raises(yaml.YAMLError):
            logkiss.setup_from_yaml(config_path)
    finally:
        os.unlink(config_path)


def test_config_reload():
    """Test configuration reload functionality."""
    config = {
        "version": 1,
        "root": {
            "level": "INFO"
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config, f)
        config_path = f.name
    
    try:
        logger = logkiss.setup_from_yaml(config_path)
        assert logger.level == logkiss.INFO
        
        # Modify config
        config["root"]["level"] = "DEBUG"
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
        
        # Test reload
        logger.reload_config()
        assert logger.level == logkiss.DEBUG
    finally:
        os.unlink(config_path)
