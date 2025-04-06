# Logkiss Examples

This directory contains various sample codes demonstrating how to use the logkiss library.

## Basic Usage Examples

### 1. Simple Examples

- `basic_logging.py`: Shows the most basic usage of logkiss.
- `hello.py`: A Hello World example.
- `sample.py`: Basic sample.
- `sample_usage.py`: General usage example.

### 2. Log Levels and Formatting

- `sample_file_logging.py`: Demonstrates file logging and various log levels.
- `sample_variable_logging.py`: Shows how to output log messages with variable data.
- `sample_matplot_debug_log.py`: Example of debug logging with matplotlib.

## Exception Handling and Error Logging

- `sample_exception.py`: Basic example of exception handling.
- `sample_test_exc_info.py`: Example of using exc_info.

## Multiple Loggers and Existing Loggers

- `sample_multi_logger.py`: Example of using multiple loggers.
- `sample_existing_logger.py`: Example of integrating with existing loggers.

## Cloud Logging

### 1. AWS CloudWatch Logs

- `sample_aws.py`: Example of logging to AWS CloudWatch Logs.
- `sample_exception_aws.py`: Example of exception logging with AWS CloudWatch.

### 2. Google Cloud Logging

- `sample_gcp.py`: Example of logging to Google Cloud Logging.
- `sample_exception_gcp.py`: Example of exception logging with Google Cloud.
- `sample_gcloud_handler.py`: Detailed example of using Google Cloud Logging handler.

## Customization Examples

### 1. Handler Customization

- `console_handler_example.py`: Example of customizing console handler.
- `default_console_handler.py`: Example of replacing with standard StreamHandler.
- `disable_color.py`: Example of disabling color output.

### 2. Configuration and Logger Management

- `sample_config.py`: Basic example of logging configuration.
- `sample_config_2.py`: Advanced example of logging configuration.

## How to Run Examples

You can run each example directly using Python. Make sure you have installed logkiss in development mode:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

Then run any example:

```bash
python examples/hello.py
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
