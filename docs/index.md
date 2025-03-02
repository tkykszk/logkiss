# logkiss

![logkiss logo](https://via.placeholder.com/200x100?text=logkiss)

**logkiss** is a simple and beautiful Python logging library.

## Features

- **Colorful Log Output** - Improved visibility with color-coded log levels
- **Simple API** - Easy-to-use API compatible with standard Python logging
- **Cloud Ready** - Support for AWS CloudWatch and Google Cloud Logging
- **Customizable** - Easily customize colors and formats

## Quick Start

```python
import logkiss as logging

# Get a logger
logger = logging.getLogger(__name__)

# Log output
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical error message")
```

## Installation

```bash
pip install logkiss
```

To use cloud logging features:

```bash
pip install "logkiss[cloud]"
```

## License

Distributed under the MIT License. See the [LICENSE](https://github.com/yourusername/logkiss/blob/main/LICENSE) file for details.
