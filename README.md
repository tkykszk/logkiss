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

### 1. Using KissConsoleHandler by default:


```python
import logkiss

logger = logkiss.getLogger("example1")
logger.warning("Colorful output in your terminal")
```
![picture 0](images/1744211555459.png)  


# 2. Using as a logging module replacement:


```python
import logkiss as logging

logger2 = logging.getLogger("example2")
logger2.warning("Also colorful warning")
logger2.error("Also colorful error")
```

![picture 1](images/1744211946693.png)  

# 3. Using custom handler configuration:
```
import logging
import logkiss
```

# Get a logger with standard logging module
```
logger3 = logging.getLogger("example3")
```

# Clear existing handlers
```
logger3.handlers.clear()
```

# Add logkiss custom handler
```
handler = logkiss.KissConsoleHandler()  # カラフルな出力用のハンドラー
handler.setFormatter(logkiss.ColoredFormatter(use_color=True))
logger3.addHandler(handler)
```

# Log with customized handler
```
logger3.error("Customized colorful output")
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
