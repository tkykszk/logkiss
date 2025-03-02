#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simplest example of logkiss usage.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.
"""

import logkiss as logging
#import logging

# If no settings are specified, the logging level should be set to logging.WARNING by default


print("Success if 3 lines are output")
# Output logs
logging.debug("Debug message")  ## Should not be displayed
logging.info("Info message")    ## Should not be displayed
logging.warning("Warning message") ## Should be displayed
logging.error("Error message")
logging.critical("Critical message")
