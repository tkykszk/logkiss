![](logkiss.svg)

# Usage

## Basic Usage

logkiss is compatible with the standard Python logging module and can be used in a similar way.

```python
import logkiss as logging

# Get a logger
logger = logging.getLogger(__name__)

# Set log level
logger.setLevel(logging.DEBUG)

# Output logs
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical error message")
```

## Using KissConsoleHandler

The main feature of logkiss is the `KissConsoleHandler` which provides colorful console output.

```python
import logkiss as logging

# Get a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Clear existing handlers
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Add KissConsoleHandler
console_handler = logging.KissConsoleHandler()
logger.addHandler(console_handler)

# Output logs
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical error message")
```

## Disabling Colors

In certain environments, you may not want colored output. You can disable colors as follows:

```python
import logkiss as logging

# Get a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Clear existing handlers
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Create a formatter with colors disabled
formatter = logging.ColoredFormatter(use_color=False)

# Add KissConsoleHandler and set formatter
console_handler = logging.KissConsoleHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Output logs
logger.debug("Debug message without color")
logger.info("Info message without color")
logger.warning("Warning message without color")
logger.error("Error message without color")
```

## Logging to a File

To log to a file, use standard `FileHandler` with `ColoredFormatter`:

```python
import logging
from logkiss import ColoredFormatter

# Create logger
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

# Add FileHandler with ColoredFormatter
file_handler = logging.FileHandler("app.log")
formatter = ColoredFormatter(use_color=False)  # Disable colors for file output
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Log messages
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

## Logging to AWS CloudWatch

To send logs to AWS CloudWatch, use `AWSCloudWatchHandler`:

```python
import logkiss as logging
from logkiss.handlers import AWSCloudWatchHandler

# Get a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Add AWSCloudWatchHandler
aws_handler = AWSCloudWatchHandler(
    log_group_name="my-log-group",
    log_stream_name="my-log-stream",
    region_name="ap-northeast-1"
)
logger.addHandler(aws_handler)

# Output logs
logger.info("Info message sent to AWS CloudWatch")
```

## Logging to Google Cloud Logging

To send logs to Google Cloud Logging, use `GCPCloudLoggingHandler`:

```python
import logkiss as logging
from logkiss.handlers import GCPCloudLoggingHandler

# Get a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Add GCPCloudLoggingHandler
gcp_handler = GCPCloudLoggingHandler(
    project_id="my-gcp-project",
    log_name="my-log"
)
logger.addHandler(gcp_handler)

# Output logs
logger.info("Info message sent to Google Cloud Logging")
