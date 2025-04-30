#!/usr/bin/env python
"""Example: Colorful console log output."""
import logkiss as logging

logger = logging.getLogger("example1")
logger.debug("Debug message")
logger.info("Info message")
logger.critical("Critical error message")
