![LOGKISS](https://raw.githubusercontent.com/tkykszk/logkiss/main/docs/logkiss-logo-tiny.png)

[![Tests](https://github.com/tkykszk/logkiss/actions/workflows/test.yml/badge.svg)](https://github.com/tkykszk/logkiss/actions/workflows/test.yml) [![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![codecov](https://codecov.io/gh/tkykszk/logkiss/branch/main/graph/badge.svg)](https://codecov.io/gh/tkykszk/logkiss)

LOGKISS (Keep It Simple and Stupid Logger) is a user-friendly logging library for Python.
Built on top of the standard logging module, it provides an interface with sensible defaults out of the box.

## Features

- **Colorful by Default**: LOGKISS uses `KissConsoleHandler` by default, which outputs logs in different colors based on log levels.
- **Drop-in Replacement**: Use it as a drop-in replacement for the standard `logging` module with `import logkiss as logging`.
- **Flexible Switching**: Easily switch back to the standard `ConsoleHandler` when needed.


## Installation

```bash
pip install logkiss
```

## Usage

### Minimal Example (Standard logging & logkiss compatibility)

```python
import logging
logging.warning("省略メソッドの最小例")
```

The same code works with logkiss:

```python
import logkiss as logging
logging.warning("初学者を惑わせがちな省略メソッド")
```



LOGKISS provides three different ways to enhance your logging experience:

### 1. Colorful Console Logging

Use LOGKISS directly to get beautiful colored log output with minimal setup:

```python
import logkiss

logger = logkiss.getLogger("example1")
logger.warning("Colorful output in your terminal")
```
![picture 0](https://raw.githubusercontent.com/tkykszk/logkiss/main/images/1744211555459.png)  


# 2. Using as a logging module replacement:


```python
import logkiss as logging

logger2 = logging.getLogger("example2")
logger2.warning("Also colorful warning")
logger2.error("Also colorful error")
```

![picture 1](https://raw.githubusercontent.com/tkykszk/logkiss/main/images/1744211946693.png)  

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

### Sample Output

When you run the above code, you will see output similar to the following:

```text
# Output from logger1.info():
2025-04-08 12:27:43,215 INFO  | example.py:5   | Colorful output

# Output from logger2.warning():
2025-04-08 12:27:43,219 WARN  | example.py:11  | Also colorful output

# Output from logger3.error():
2025-04-08 12:27:43,224,123 ERROR | example.py:21 | Standard monochrome output
```

The first two log messages will be displayed with color formatting in your terminal, while the third message will use the standard logging format without colors.

![logkiss-terminal-demo](https://raw.githubusercontent.com/tkykszk/logkiss/main/docs/logkiss-terminal-demo.png)

## Environment Variables

LOGKISS can be configured using the following environment variables:

- `LOGKISS_DEBUG`: Enable debug mode by setting to `1`, `true`, or `yes`. When enabled:
  - Root logger's level is set to `DEBUG` instead of `INFO`
  - More detailed logging information is displayed
- `LOGKISS_DISABLE_COLOR`: Disable colored output by setting to `1`, `true`, or `yes`
- `NO_COLOR`: variable to disable colors (any value)

Example:

```bash
# Enable debug mode
export LOGKISS_DEBUG=1

# Run your Python script
python your_script.py
```

## Behavior with Modules and Libraries

Logkiss modifies the behavior of the Python logging system. This has some implications you should be aware of:

### Module Interactions

- When you import logkiss in a module, it affects the global logging configuration for the entire Python process
- If you import logkiss in module A, and then import standard logging in module B, the logging in module B will also use logkiss's colorful output
- To switch a specific logger back to standard behavior, use `logkiss.use_console_handler(logger)`

### Third-Party Library Compatibility

- Most Python libraries that use the standard logging module will automatically benefit from logkiss's colorful output
- However, libraries that define custom handlers or formatters (like matplotlib) may not display colored output
- Libraries that redirect their logs or use advanced logging configurations might have varying results

### Best Practices

- In simple applications, importing logkiss at the entry point will colorize logs throughout the application
- For more complex applications, you may want to be more selective about which loggers use colorful output

## Configuration

For detailed configuration options, please refer to [CONFIG.md](CONFIG.md).

## Acknowledgments

The output format of logkiss is inspired by [deigan / loguru](https://github.com/Delgan/loguru)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Other Languages

- [日本語](README_JAPANESE.md)
