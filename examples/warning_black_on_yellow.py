#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sample code to display WARNING level with black text on yellow background
"""

import logging
import os
from logkiss.logkiss import setup

def main():
    """Demo to display WARNING level with black text on yellow background"""
    # Reset logger initialization
    logging.root.handlers = []
    
    # Setup logkiss with specified configuration file
    config_path = os.path.join(os.path.dirname(__file__), "custom_color_config.yaml")
    logger = setup(config_path)
    
    # Set to DEBUG level to display all log levels
    logger.setLevel(logging.DEBUG)
    
    # Output messages at each log level
    logger.debug("This is a DEBUG level message (blue)")
    logger.info("This is an INFO level message (white)")
    logger.warning("This is a WARNING level message (black text on yellow background)")
    logger.error("This is an ERROR level message (black text on red background)")
    logger.critical("This is a CRITICAL level message (black text on bright red background, bold)")

if __name__ == "__main__":
    main()
