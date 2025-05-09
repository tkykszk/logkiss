import sys
from pathlib import Path
import logkiss

if __name__ == "__main__":
    # 設定ファイルのパスを取得
    config_path = Path(__file__).parent / "config_color_test2.yaml"
    # 設定ファイルを適用
    logkiss.setup_from_yaml(config_path)
    logger = logkiss.getLogger("test2")
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
