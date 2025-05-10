#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo script to display colors for each log level in logkiss
For screenshot capture
"""

import logging
import logkiss
import os

def main():
    """Main function to display colors for each log level"""
    # ロガーの初期化をリセット
    logging.root.handlers = []
    
    # Setup logkiss
    # Create configuration dictionary for dictConfig
    config = {
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
    
    logkiss.dictConfig(config)
    logger = logging.getLogger()
    
    # Set to DEBUG level to display all log levels
    logger.setLevel(logging.DEBUG)
    
    # Output messages at each log level
    logger.debug("This is a DEBUG level message (blue)")
    logger.info("This is an INFO level message (white)")
    logger.warning("This is a WARNING level message (yellow)")
    logger.error("This is an ERROR level message (black text on red background)")
    logger.critical("This is a CRITICAL level message (black text on bright red background, bold)")
    
    # Separator line
    print("\n" + "-" * 80 + "\n")
    
    # Demo to disable colors by setting the NO_COLOR environment variable
    print("Demo to disable colors by setting the NO_COLOR environment variable:")
    os.environ["NO_COLOR"] = "1"
    
    # ロガーの初期化をリセット
    logging.root.handlers = []
    
    # Create a new logger (NO_COLOR environment variable will be reflected)
    # Create configuration dictionary for dictConfig
    config = {
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
    
    logkiss.dictConfig(config)
    no_color_logger = logging.getLogger()
    no_color_logger.setLevel(logging.DEBUG)
    
    # Output messages at each log level (without colors)
    no_color_logger.debug("This is a DEBUG level message (no color)")
    no_color_logger.info("This is an INFO level message (no color)")
    no_color_logger.warning("This is a WARNING level message (no color)")
    no_color_logger.error("This is an ERROR level message (no color)")
    no_color_logger.critical("This is a CRITICAL level message (no color)")

if __name__ == "__main__":
    main()
