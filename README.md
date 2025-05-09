![LOGKISS](https://raw.githubusercontent.com/tkykszk/logkiss/main/docs/logkiss-logo-tiny.png)

[![Tests](https://github.com/tkykszk/logkiss/actions/workflows/test.yml/badge.svg)](https://github.com/tkykszk/logkiss/actions/workflows/test.yml) [![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![codecov](https://codecov.io/gh/tkykszk/logkiss/branch/main/graph/badge.svg)](https://codecov.io/gh/tkykszk/logkiss)

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
# examples/minimal_warning.py
import logging
logging.warning("Minimal example for beginners")
```

The same code works with logkiss:

```python
# examples/minimal_warning.py
import logkiss as logging
logging.warning("Minimal example for beginners")
```



LOGKISS provides three different ways to enhance your logging experience:

### 1. Colorful Console Logging

Use LOGKISS directly to get beautiful colored log output with minimal setup:

```python
# examples/quickstart_1.py
import logkiss

logger = logkiss.getLogger("example1")
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical error message")
```
![picture 0](https://raw.githubusercontent.com/tkykszk/logkiss/main/images/1744211555459.png)  


# 2. Using as a logging module replacement:


```python
# examples/quickstart_2.py
import logkiss as logging

logger2 = logging.getLogger("example2")
logger2.debug("Debug message")
logger2.info("Info message")
logger2.warning("Warning message")
logger2.error("Error message")
logger2.critical("Critical error message")
```

![picture 1](https://raw.githubusercontent.com/tkykszk/logkiss/main/images/1744211946693.png)  

# 3. Using custom handler configuration:
```python
# examples/quickstart_3.py
import logging
import logkiss
```

# Get a logger with standard logging module
```python
# examples/quickstart_3.py
logger3 = logging.getLogger("example3")
logger3.setLevel(logging.DEBUG)
logger3.debug("Debug message")
logger3.info("Info message")
logger3.warning("Warning message")
logger3.error("Error message")
logger3.critical("Critical error message")
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
- `NO_COLOR`: Disable colored output (the mere presence of this variable, regardless of its value, disables colors) - **DEPRECATED**: Use `LOGKISS_DISABLE_COLOR` instead

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

logkissは複数の設定方法をサポートしています。標準のloggingライブラリと互換性のある方法と、logkiss独自の便利な機能を組み合わせることができます。

### 自動設定

logkissをインポートするだけで、自動的に設定が適用されます。

```python
import logkiss
# 自動的に環境変数や設定ファイルから設定が読み込まれます
```

設定の優先順位は以下の通りです：

1. 環境変数 `LOGKISS_SKIP_CONFIG=1` が設定されている場合、設定ファイルの読み込みをスキップ
2. 環境変数 `LOGKISS_CONFIG` で指定された設定ファイル
3. デフォルトの場所にある設定ファイル（`~/.config/logkiss/config.yaml` など）
4. 環境変数から設定（`LOGKISS_LEVEL`, `LOGKISS_FORMAT` など）

主要な環境変数：

- `LOGKISS_LEVEL`: ログレベルを指定（DEBUG, INFO, WARNING, ERROR, CRITICAL）
- `LOGKISS_FORMAT`: ログフォーマット文字列
- `LOGKISS_DISABLE_COLOR`: 色付けを無効にする（値: 1, true, yes）
- `NO_COLOR`: 色付けを無効にする（値に関係なく、環境変数が存在するだけで無効化） - **非推奨**: 代わりに `LOGKISS_DISABLE_COLOR` を使用してください

### dictConfig による設定

標準の `logging.config.dictConfig` と互換性のある方法で設定できます。

```python
import logkiss
from logkiss import dictConfig

config = {
    "version": 1,
    "formatters": {
        "colored": {
            "()": "logkiss.ColoredFormatter",
            "format": "%(asctime)s %(levelname)s | %(filename)s: %(lineno)d | %(message)s",
            "colors": {  # logkiss独自の色設定
                "levels": {
                    "WARNING": {"fg": "black", "bg": "yellow"}
                }
            }
        }
    },
    "handlers": {
        "console": {
            "class": "logkiss.KissConsoleHandler",
            "level": "DEBUG",
            "formatter": "colored"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG"
        }
    }
}

dictConfig(config)
```

### YAMLファイルによる設定

YAMLファイルから設定を読み込むこともできます。

```python
import logkiss
from logkiss import yaml_config

yaml_config("path/to/config.yaml")
```

YAMLファイルの例：

```yaml
version: 1
formatters:
  colored:
    (): logkiss.ColoredFormatter
    format: "%(asctime)s %(levelname)s | %(filename)s: %(lineno)d | %(message)s"
    colors:
      levels:
        WARNING:
          fg: black
          bg: yellow
handlers:
  console:
    class: logkiss.KissConsoleHandler
    level: DEBUG
    formatter: colored
loggers:
  "":
    handlers: [console]
    level: DEBUG
```

### 色設定のカスタマイズ

logkissでは、各ログレベルの色をカスタマイズできます。dictConfigまたはYAMLファイルで以下のように設定します：

```python
"colors": {
    "levels": {
        "DEBUG": {"fg": "blue"},
        "INFO": {"fg": "white"},
        "WARNING": {"fg": "black", "bg": "yellow"},  # 黄色地に黒字
        "ERROR": {"fg": "black", "bg": "red"},
        "CRITICAL": {"fg": "black", "bg": "bright_red", "style": "bold"}
    },
    "elements": {
        "timestamp": {"fg": "white"},
        "filename": {"fg": "cyan"},
        "message": {
            "DEBUG": {"fg": "blue"},
            "INFO": {"fg": "white"},
            "WARNING": {"fg": "black", "bg": "yellow"},
            "ERROR": {"fg": "black", "bg": "red"},
            "CRITICAL": {"fg": "black", "bg": "bright_red", "style": "bold"}
        }
    }
}
```

利用可能な色とスタイル：

- 前景色（`fg`）: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`, `bright_black`, `bright_red`, `bright_green`, `bright_yellow`, `bright_blue`, `bright_magenta`, `bright_cyan`, `bright_white`
- 背景色（`bg`）: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`, `bright_black`, `bright_red`, `bright_green`, `bright_yellow`, `bright_blue`, `bright_magenta`, `bright_cyan`, `bright_white`
- スタイル（`style`）: `bold`, `dim`, `italic`, `underline`, `reverse`, `hidden`, `strike`

詳細な設定オプションについては、[CONFIG.md](CONFIG.md)を参照してください。

## Acknowledgments

The output format of logkiss is inspired by [deigan / loguru](https://github.com/Delgan/loguru)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Other Languages

- [日本語](README_JAPANESE.md)
