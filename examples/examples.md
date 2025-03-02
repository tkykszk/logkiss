# Logkiss Examples

This directory contains various sample codes demonstrating how to use the logkiss library.

## Basic Usage Examples

### 1. Simplest Examples
- `basic_logging.py`: Shows the most basic usage of logkiss.
- `simplest.py`: A simple logging output example.

### 2. Log Levels and Formatting
- `file_logging.py`: Demonstrates file logging and the use of different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
- `variable_logging.py`: Shows how to output log messages with variable data. Includes examples of various string formatting methods (%-style, str.format(), f-string).

## Customization Examples

### 1. Handler Customization
- `default_console_handler.py`: Shows how to replace KissConsoleHandler with the standard StreamHandler.
- `disable_color.py`: Demonstrates how to disable color output.

### 2. Configuration and Logger Management
- `simple_config.py` and `simple_config_2.py`: Examples of logging configuration methods.
- `multi_logger.py`: Shows how to use multiple loggers.

## Special Usage Examples

### 1. Graphical Output
- `matplot_example.py`: Example of integration with Matplotlib.

### 2. Others
- `usage_example.py`: A comprehensive example showing more advanced usage.
- `hello.py`: Demonstration of basic usage.
- `simple.py`: Example with simple configuration.

## How to Run Examples

You can run each example as follows:

```bash
python examples/[example_filename].py
```

For example:
```bash
python examples/basic_logging.py
```

## Notes

1. Samples that perform file output (like `file_logging.py`) will create log files in the current directory when executed.
2. Color output disabling (`disable_color.py`) may appear different depending on the terminal type.
3. Some samples may require additional Python packages (e.g., matplotlib) to run.

Each sample file contains detailed explanations in the code comments. Please refer to the actual code along with these comments.
