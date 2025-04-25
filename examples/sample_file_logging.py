"""Example of logging to a file.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.
"""

import logkiss as logging

# Configure logging to file
logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

# Output messages at different log levels
logger.debug("Debug info: Detailed diagnostic message")
logger.info("Info: Confirmation that things are working as expected")
logger.warning("Warning: Indication of potential issues or unexpected events")
logger.error("Error: Serious problem preventing function execution")
logger.critical("Critical: Program may be unable to continue running")
