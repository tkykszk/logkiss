#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logkiss

# Example: Colorful console log output
logger = logkiss.getLogger("example1")
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical error message")
