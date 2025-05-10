#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sample code to display WARNING level with black text on yellow background (direct configuration version)
"""

import logging
import logkiss
from logkiss.logkiss import ColorManager, ColoredFormatter, KissConsoleHandler

def main():
    """Demo to display WARNING level with black text on yellow background (direct configuration)"""
    # Reset logger initialization
    logging.root.handlers = []
    
    # Create custom color manager
    color_manager = ColorManager()
    
    # Explicitly override WARNING level colors
    color_manager.config["levels"]["WARNING"] = {"fg": "black", "bg": "yellow"}
    color_manager.config["elements"]["message"]["WARNING"] = {"fg": "black", "bg": "yellow"}
    
    # Create custom formatter
    formatter = ColoredFormatter(use_color=True)
    formatter.color_manager = color_manager
    
    # Create and configure handler
    handler = KissConsoleHandler()
    handler.setFormatter(formatter)
    
    # Configure logger
    logger = logging.getLogger()
    logger.handlers = []  # Clear existing handlers
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    # Output messages at each log level
    logger.debug("This is a DEBUG level message (blue)")
    logger.info("This is an INFO level message (white)")
    logger.warning("This is a WARNING level message (black text on yellow background)")
    logger.error("This is an ERROR level message (black text on red background)")
    logger.critical("This is a CRITICAL level message (black text on bright red background, bold)")

if __name__ == "__main__":
    main()
