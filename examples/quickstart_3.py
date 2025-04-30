

import logging
import logkiss

# Get a logger using the standard logging module
logger3 = logging.getLogger("example3")

# Clear existing handlers
logger3.handlers.clear()

# Add logkiss custom handler
handler = logkiss.KissConsoleHandler()  # Handler for colorful output
handler.setFormatter(logkiss.ColoredFormatter())
logger3.addHandler(handler)

# Output logs with customized handler
logger3.setLevel(logging.DEBUG)  # Set to display all log levels
logger3.debug("Debug message")
logger3.info("Info message")
logger3.warning("Warning message")
logger3.error("Error message")
logger3.critical("Critical error message")
