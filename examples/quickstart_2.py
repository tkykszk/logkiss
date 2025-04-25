#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logkiss as logging

# Example: Use as a drop-in replacement for the logging module
logger2 = logging.getLogger("example2")
logger2.debug("Debug message")
logger2.info("Info message")
logger2.warning("Warning message")
logger2.error("Error message")
logger2.critical("Critical error message")
