"""Example of using standard default console handler.


"""

import logkiss as logging
import sys

# Get logkiss logger
logger = logging.getLogger(__name__)

# Remove KissConsoleHandler
for handler in logger.handlers[:]:
    if isinstance(handler, logging.KissConsoleHandler):
        logger.removeHandler(handler)

# Add standard StreamHandler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

# Test log output
logger.warning("This will be output in standard format")
logger.info("Information message")
logger.error("Error message")
