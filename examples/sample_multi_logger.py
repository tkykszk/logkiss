
"""Example of using multiple loggers.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.
"""

import os
import sys
from pathlib import Path
import logkiss as logging

# Log file path
log_file = os.path.join(os.path.dirname(__file__), "both.log")

# Create a console-only logger
console_logger = logging.getLogger("console")
for handler in console_logger.handlers[:]:
    console_logger.removeHandler(handler)
console_logger.setLevel(logging.DEBUG)
console_handler = logging.KissConsoleHandler()
console_logger.addHandler(console_handler)
console_logger.propagate = False

# Create a logger that outputs to both console and file
both_logger = logging.getLogger("both")
for handler in both_logger.handlers[:]:
    both_logger.removeHandler(handler)
both_logger.setLevel(logging.DEBUG)
both_logger.addHandler(logging.KissConsoleHandler())

# 標準のFileHandlerを使用し、ColoredFormatterを設定
file_handler = logging.FileHandler(log_file)
formatter = logging.ColoredFormatter(use_color=False)
file_handler.setFormatter(formatter)
both_logger.addHandler(file_handler)

both_logger.propagate = False


def main():
    """Main function"""
    print("\n1. Console-only logger:")
    console_logger.debug("Debug message (console only)")
    console_logger.info("Info message (console only)")
    console_logger.warning("Warning message (console only)")
    console_logger.error("Error message (console only)")
    console_logger.critical("Critical error message (console only)")

    print("\n2. Logger that outputs to both console and file:")
    both_logger.debug("Debug message (both)")
    both_logger.info("Info message (both)")
    both_logger.warning("Warning message (both)")
    both_logger.error("Error message (both)")
    both_logger.critical("Critical error message (both)")

    print(f"\nLog file created: {log_file}")
    print("File contents:")
    print("-" * 80)
    with open(log_file, "r") as f:
        print(f.read().rstrip())
    print("-" * 80)


if __name__ == "__main__":
    main()
