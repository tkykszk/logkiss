# LOGKISS

![LOGKISS](docs/logkiss-logo-tiny.png)

[![Tests](https://github.com/tkykszk/logkiss/actions/workflows/test.yml/badge.svg)](https://github.com/tkykszk/logkiss/actions/workflows/test.yml) [![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![codecov](https://codecov.io/gh/tkykszk/logkiss/branch/main/graph/badge.svg)](https://codecov.io/gh/tkykszk/logkiss)

LOGKISS (Keep It Simple and Stupid Logger) is a user-friendly logging library for Python.
Built on top of the standard logging module, it provides an interface with sensible defaults out of the box.

## Features

- **Colorful by Default**: LOGKISS uses `KissConsoleHandler` by default, which outputs logs in different colors based on log levels.
- **Drop-in Replacement**: Use it as a drop-in replacement for the standard `logging` module with `import logkiss as logging`.
- **Flexible Switching**: Easily switch back to the standard `ConsoleHandler` when needed.


## Innovations

- Aggregate log volume statistics per logger
- Guided configuration for logger-level suppression
- Handler sharing capabilities
- Console UI


## Installation

```bash
pip install logkiss
```

## Usage

LOGKISS provides three different ways to enhance your logging experience:

### 1. Colorful Console Logging

Use LOGKISS directly to get beautiful colored log output with minimal setup:

```python
import logkiss

logger = logkiss.getLogger("example1")
logger.info("Colorful output in your terminal")
```

### 2. Drop-in Replacement Mode

Use LOGKISS as a direct replacement for the standard logging module - ideal for existing projects:

```python
import logkiss as logging

logger = logging.getLogger("example2")
logger.warning("Colorful warnings without changing your code")
```

### 3. Standard Output Mode

For environments where color isn't needed (CI/CD, log parsing), use standard output format:

```python
# Use the standard logging module
import logging

# Get a logger
logger = logging.getLogger("example3")

# Create a standard output handler
handler = logging.StreamHandler()

# Set a formatted output pattern
handler.setFormatter(logging.Formatter(
    fmt='%(asctime)s,%(msecs)03d %(levelname)-5s | %(filename)s:%(lineno)3d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

# Add the handler to the logger
logger.addHandler(handler)

# Output an error message
logger.error("Standard monochrome output")
```

## Environment Variables

LOGKISS can be configured using the following environment variables:

- `LOGKISS_DEBUG`: Enable debug mode by setting to `1`, `true`, or `yes`. When enabled:
  - Root logger's level is set to `DEBUG` instead of `INFO`
  - More detailed logging information is displayed

Example:
```bash
# Enable debug mode
export LOGKISS_DEBUG=1

# Run your Python script
python your_script.py
```

## Configuration

For detailed configuration options, please refer to [CONFIG.md](CONFIG.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Other Languages

- [日本語](README_JAPAN.md)
