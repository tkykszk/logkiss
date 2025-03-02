"""Example of disabling color output in logkiss.

This example demonstrates how to disable colored output in logkiss logs.
The key is to create a ColoredFormatter with use_color=False and set it
to the handler explicitly.

Usage:
    python disable_color.py

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.
"""

import logkiss as logging

# Get logkiss logger and configure it with color disabled
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set log level to INFO to see all messages

# Clear existing handlers to avoid duplicates
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Create a formatter with color disabled
formatter = logging.ColoredFormatter(use_color=False)

# Add a new console handler with color disabled formatter
console_handler = logging.KissConsoleHandler()
console_handler.setFormatter(formatter)  # This is the key step to disable colors
logger.addHandler(console_handler)

# Test log output
logger.debug('This debug message will not be displayed due to log level')
logger.info('This information message will be displayed without color')
logger.warning('This warning message will be displayed without color')
logger.error('This error message will be displayed without color')
