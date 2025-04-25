#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Example of advanced configuration.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.
"""

import logkiss as logging

logging.basicConfig(level=logging.INFO)

# Get logger
logger = logging.getLogger()  # Use root logger
logger.setLevel(logging.ERROR)

print("Success if 2 lines are output")
# Output logs
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
