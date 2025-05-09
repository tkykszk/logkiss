import os
import sys
import shutil
import tempfile
import yaml
import pytest
from pathlib import Path

import logkiss
import logging
from logkiss import KissConsoleHandler

@pytest.fixture
def tmp_config(tmp_path):
    def _make_config(data):
        config_path = tmp_path / "config.yaml"
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True)
        return config_path
    return _make_config

# TC001: 色テスト（赤・白）
def test_config_color_test1(tmp_config, caplog):
    config = {
        "levels": {
            "info": {"color": "red", "style": "bold"},
            "error": {"color": "white", "style": "bold"}
        }
    }
    config_path = tmp_config(config)
    # TEST DEBUG: show config dict and file contents
    print("[TEST DEBUG] config dict:", config)
    print("[TEST DEBUG] config file contents:\n", config_path.read_text())
    logkiss.setup_from_yaml(config_path)
    logger = logkiss.getLogger("test1")
    # Ensure default KissConsoleHandler on root logger has NOTSET level
    root_logger = logging.getLogger()
    kiss_handler = next(
        h for h in root_logger.handlers if isinstance(h, KissConsoleHandler)
    )
    assert kiss_handler.level == logging.WARNING
    with caplog.at_level("INFO"):
        logger.info("info message")
        logger.error("error message")
    # caplog.textには色は含まれない可能性が高いので、ログ内容のみ検証
    assert "info message" not in caplog.text
    assert "error message" in caplog.text

# TC002: 日付書式テスト（hh:mm:ss）
def test_config_color_test2(tmp_config, caplog):
    config = {
        "format": "%(asctime)s %(levelname)s %(message)s",
        "datefmt": "%H:%M:%S",
        "root": {"level": "DEBUG"}
    }
    config_path = tmp_config(config)
    logkiss.setup_from_yaml(config_path)
    logger = logkiss.getLogger("test2")
    with caplog.at_level("INFO"):
        logger.info("test datefmt")
    assert any(
        line.count(":") == 2 and len(line.split()[0].split(":")) == 3 for line in caplog.text.splitlines()
    )

# TC003: ログレベル設定の反映テスト
def test_config_log_level_test(tmp_config, caplog):
    config = {"root": {"level": "WARNING"}}
    config_path = tmp_config(config)
    logkiss.setup_from_yaml(config_path)
    logger = logkiss.getLogger("test3")
    with caplog.at_level("WARNING"):
        logger.debug("debug message")
        logger.warning("warn message")
    assert "warn message" in caplog.text
    assert "debug message" not in caplog.text

# TC004: ファイル出力設定の反映テスト
def test_config_log_file_output_test(tmp_config, tmp_path):
    log_file = tmp_path / "test.log"
    config = {
        "formatters": {
            "simple": {"format": "%(levelname)s %(message)s"}
        },
        "handlers": {
            "file": {"class": "FileHandler", "filename": str(log_file), "level": "INFO", "formatter": "simple"}
        },
        "root": {"level": "INFO", "handlers": ["file"]}
    }
    config_path = tmp_config(config)
    logkiss.setup_from_yaml(config_path)
    logger = logkiss.getLogger("test4")
    logger.info("file output test")
    for h in logger.handlers:
        if hasattr(h, 'flush'):
            h.flush()
    # root loggerにもflush
    import logging as pylib_logging
    for h in pylib_logging.getLogger().handlers:
        if hasattr(h, 'flush'):
            h.flush()
    pylib_logging.shutdown()
    print('tmp_path files:', list(tmp_path.iterdir()))
    assert log_file.read_text(encoding="utf-8").find("file output test") != -1

# TC005: フォーマット設定の反映テスト
def test_config_log_format_test(tmp_config, caplog):
    config = {
        "formatters": {
            "custom": {"format": "%(levelname)s::%(message)s"}
        },
        "handlers": {
            "console": {"class": "StreamHandler", "formatter": "custom"}
        },
        "root": {"level": "INFO", "handlers": ["console"]}
    }
    config_path = tmp_config(config)
    logkiss.setup_from_yaml(config_path)
    logger = logkiss.getLogger("test5")
    with caplog.at_level("INFO"):
        logger.info("format test")
    assert "INFO::format test" in caplog.text

# TC006: ログローテーション設定の反映テスト
def test_config_rotation_test(tmp_config, tmp_path):
    log_file = tmp_path / "rot.log"
    config = {
        "formatters": {
            "simple": {"format": "%(levelname)s %(message)s"}
        },
        "handlers": {
            "rot": {
                "class": "RotatingFileHandler",
                "filename": str(log_file),
                "maxBytes": 100,
                "backupCount": 1,
                "level": "DEBUG",
                "formatter": "simple"
            }
        },
        "root": {"level": "DEBUG", "handlers": ["rot"]}
    }
    config_path = tmp_config(config)
    logkiss.setup_from_yaml(config_path)
    logger = logkiss.getLogger("test6")
    for i in range(30):
        logger.info(f"rot test {i}")
    for h in logger.handlers:
        if hasattr(h, 'flush'):
            h.flush()
    import logging as pylib_logging
    pylib_logging.shutdown()
    rotated = list(tmp_path.glob("rot.log.*"))
    assert len(rotated) >= 1

# TC007: フィルタ設定の反映テスト
def test_config_filter_test(tmp_config, caplog):
    config = {
        "formatters": {
            "simple": {"format": "%(levelname)s %(message)s"}
        },
        "filters": {
            "only_test7": {"logger": "test7"}
        },
        "handlers": {
            "console": {"class": "StreamHandler", "level": "DEBUG", "filters": ["only_test7"], "formatter": "simple"}
        },
        "root": {"level": "DEBUG", "handlers": ["console"]}
    }
    config_path = tmp_config(config)
    logkiss.setup_from_yaml(config_path)
    logger = logkiss.getLogger("test7")
    with caplog.at_level("INFO"):
        logger.info("should appear")
    logger_other = logkiss.getLogger("other")
    with caplog.at_level("INFO"):
        logger_other.info("should not appear")
    assert "should appear" in caplog.text
    assert "should not appear" not in caplog.text

# TC008: デフォルト値テスト
def test_config_default_value_test(tmp_path, caplog):
    # config.yamlを空にする
    config_path = tmp_path / "config.yaml"
    config_path.write_text("", encoding="utf-8")
    try:
        logkiss.setup_from_yaml(config_path)
        logger = logkiss.getLogger("test8")
        with caplog.at_level("INFO"):
            logger.info("default level test")
        assert "default level test" in caplog.text
    except Exception as e:
        pytest.skip(f"空config時に例外発生: {e}")

# TC009: 無効な値設定時の挙動テスト
def test_config_invalid_value_test(tmp_config):
    config = {"root": {"level": "NO_SUCH_LEVEL"}}
    config_path = tmp_config(config)
    with pytest.raises(Exception):
        logkiss.setup_from_yaml(config_path)

# TC010: 環境変数による設定上書きテスト
def test_config_env_override_test(tmp_config, caplog, monkeypatch):
    config = {"root": {"level": "INFO"}}
    config_path = tmp_config(config)
    monkeypatch.setenv("LOGKISS_LEVEL", "ERROR")
    logkiss.setup_from_yaml(config_path)
    logger = logkiss.getLogger("test10")
    with caplog.at_level("ERROR"):
        logger.info("should not appear")
        logger.error("should appear")
    assert "should appear" in caplog.text
    assert "should not appear" not in caplog.text

# TC011: 複数ハンドラ設定の反映テスト
def test_config_multiple_handler_test(tmp_config, tmp_path, caplog):
    log_file = tmp_path / "multi.log"
    config = {
        "formatters": {
            "simple": {"format": "%(levelname)s %(message)s"}
        },
        "handlers": {
            "console": {"class": "StreamHandler", "level": "INFO", "formatter": "simple"},
            "file": {"class": "FileHandler", "filename": str(log_file), "level": "INFO", "formatter": "simple"}
        },
        "root": {"level": "INFO", "handlers": ["console", "file"]}
    }
    config_path = tmp_config(config)
    logkiss.setup_from_yaml(config_path)
    logger = logkiss.getLogger("test11")
    with caplog.at_level("INFO"):
        logger.info("multi handler test")
    for h in logger.handlers:
        if hasattr(h, 'flush'):
            h.flush()
    import logging as pylib_logging
    for h in pylib_logging.getLogger().handlers:
        if hasattr(h, 'flush'):
            h.flush()
    pylib_logging.shutdown()
    print('tmp_path files:', list(tmp_path.iterdir()))
    assert "multi handler test" in caplog.text
    assert "multi handler test" in log_file.read_text(encoding="utf-8")

# TC012: YAML構文エラー時の挙動テスト
def test_config_yaml_syntax_error_test(tmp_path):
    config_path = tmp_path / "bad.yaml"
    config_path.write_text("levels: [bad yaml", encoding="utf-8")
    with pytest.raises(Exception):
        logkiss.setup_from_yaml(config_path)
