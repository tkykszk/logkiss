# LOGKISS

![LOGKISS](docs/logkiss-logo-tiny.png)

[![Tests](https://github.com/tkykszk/logkiss/actions/workflows/test.yml/badge.svg)](https://github.com/tkykszk/logkiss/actions/workflows/test.yml)
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

```python
# 1. Using KissConsoleHandler by default:
import logkiss

logger1 = logkiss.getLogger("example1")
logger1.info("Colorful output")

# 2. Using as a logging module replacement:
import logkiss as logging

logger2 = logging.getLogger("example2")
logger2.warning("Also colorful output")

# 3. Switching to standard ConsoleHandler:
import logkiss

# Get a logger and switch it to standard console handler
logger3 = logkiss.getLogger("example3")
logkiss.use_console_handler(logger3)
logger3.error("Standard monochrome output")
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

![logkiss-terminal-demo](docs/logkiss-terminal-demo.png)

## Environment Variables

LOGKISS can be configured using the following environment variables:

- `LOGKISS_DEBUG`: Enable debug mode by setting to `1`, `true`, or `yes`. When enabled:
  - Root logger's level is set to `DEBUG` instead of `INFO`
  - More detailed logging information is displayed
- `LOGKISS_DISABLE_COLOR`: Disable colored output by setting to `1`, `true`, or `yes`
- `NO_COLOR`: Industry standard environment variable to disable colors (any value)

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
- If you need to maintain specific formatting for certain modules, use `logkiss.use_console_handler()` selectively

## Configuration

For detailed configuration options, please refer to [CONFIG.md](CONFIG.md).

## Acknowledgments

The output format of logkiss is inspired by [deigan / loguru](https://github.com/Delgan/loguru)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Other Languages

- [日本語](README_JAPANESE.md)
