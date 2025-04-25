"""
Integration example for logkiss.

This demonstrates how to integrate logkiss with an existing 
application that already uses the standard logging module.
"""

# First, setup standard logging as it would be in an existing application
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
std_logger = logging.getLogger("std_app")

# Log some messages with standard logger
std_logger.warning("Standard logger: This is a standard warning")

# Now integrate logkiss
import logkiss  # 正しくlogkissをインポート

logkiss_logger = logkiss.getLogger("logkiss_app")  # logkissからロガーを取得
print(f"---- logkiss_logger.propagate = {logkiss_logger.propagate}")

# Log some messages with logkiss logger
logkiss_logger.warning("Logkiss logger: (1)  This is an enhanced warning")

# You can continue using both loggers side by side
std_logger.warning("Standard logger: (2)  Still working")
logkiss_logger.warning("Logkiss logger: (3)  Also working")

# Demonstrate error logging with both
try:
    result = 1 / 0
except Exception as e:
    print("STD ------------------------")
    std_logger.exception("Standard logger caught an error")
    print("LOGKISS------------------------")
    logkiss_logger.exception("Logkiss logger caught the same error")

print("\nCheck the console output above to see the log messages from both logging systems!")

import logging_tree

logging_tree.printout()
