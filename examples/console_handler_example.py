#!/usr/bin/env python
"""
Sample of using logkiss's KissConsoleHandler additionally in a situation where existing logging is being used

This sample demonstrates how to output logs to the console
by combining the standard logging module and logkiss.
"""

import logging
import logkiss
from logkiss.logkiss import KissConsoleHandler

# Get logger
logger = logging.getLogger("console_example")
logger.setLevel(logging.DEBUG)

# Clear existing handlers (to avoid duplicate output)
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# logkiss の KissConsoleHandler を使用
kiss_handler = KissConsoleHandler()
logger.addHandler(kiss_handler)

# ログ出力
logger.debug("This is a debug message")
logger.info("This is an information message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical error message")

# Output structured log
logger.info("Example of structured log", extra={"user_id": 12345, "action": "login", "status": "success", "ip_address": "192.168.1.1"})

# Output nested structured log
logger.warning(
    "Example of complex structured log",
    extra={
        "request": {"method": "POST", "path": "/api/users", "headers": {"content-type": "application/json", "user-agent": "Mozilla/5.0"}},
        "response": {"status_code": 400, "body": {"error": "Invalid input", "details": ["Username is required", "Email is invalid"]}},
    },
)

print("\n--- Example of using root logger ---")

# Get and configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# すべてのハンドラーをクリア
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Clear all handlers (to avoid duplicate output)
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# logkiss の KissConsoleHandler を使用
root_kiss_handler = KissConsoleHandler()
root_logger.addHandler(root_kiss_handler)

# ログ出力
logging.info("Information message from root logger")
logging.warning("Warning message from root logger")
logging.error("Error message from root logger")
