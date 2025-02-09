#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logkiss as logging

# Get logger
logger = logging.getLogger()  # Use root logger

print("Success if 3 lines are output")
# Output logs
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
