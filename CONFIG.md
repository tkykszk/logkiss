# LOGKISS Configuration Guide

LOGKISS allows you to customize log colors and styles using a YAML configuration file. This configuration file lets you control colors and styles for log levels, messages, and other elements in detail.

## Configuration File Structure

The configuration file consists of three main sections:

1. `levels`: Color settings for log level names
2. `messages`: Color settings for log messages
3. `elements`: Color settings for elements like timestamps and filenames

### Basic Structure

```yaml
levels:
  debug:
    color: cyan
    style: bold
  info:
    color: white
    style: bold
  warning:
    color: yellow
    style: bold
  error:
    color: black
    background: red
    style: bold
  critical:
    color: black
    background: bright_red
    style: bold

messages:
  debug:
    color: cyan
  info:
    color: white
  warning:
    color: yellow
  error:
    color: black
    background: red
  critical:
    color: black
    background: bright_red

elements:
  timestamp:
    color: blue
    style: dim
  filename:
    color: green
    style: bold
```

## Configuration Options

### Log Level Display

By default, log levels are limited to 5 characters, so they are displayed as follows:

- DEBUG → DEBUG
- INFO → INFO
- WARNING → WARN
- ERROR → ERROR
- CRITICAL → CRITI

This character limit is intended to keep log formatting clean. If you want to change the character limit, use a custom formatter.

### Available Colors

#### Foreground Colors (Text)
- black
- red
- green
- yellow
- blue
- magenta
- cyan
- white
- bright_black
- bright_red
- bright_green
- bright_yellow
- bright_blue
- bright_magenta
- bright_cyan
- bright_white

#### Background Colors
- black
- red
- green
- yellow
- blue
- magenta
- cyan
- white
- bright_black
- bright_red
- bright_green
- bright_yellow
- bright_blue
- bright_magenta
- bright_cyan
- bright_white

### Styles
- bold: Bold text
- dim: Dimmed text
- italic: Italic text
- underline: Underlined text
- blink: Blinking text
- reverse: Reversed colors
- hidden: Hidden text
- strike: Strikethrough text

## How to Use Configuration

1. Create a configuration file:
```python
# logkiss.yaml
levels:
  debug:
    color: cyan
    style: bold
  error:
    color: red
    style: bold
    background: black
```

2. Specify the configuration file when initializing the logger:
```python
import logkiss
from pathlib import Path

config_path = Path('logkiss.yaml')
logger = logkiss.getLogger(__name__, color_config=config_path)
```

## Default Configuration

If you don't specify a configuration file, the following default configuration is used:

```yaml
levels:
  debug:
    color: cyan
    style: bold
  info:
    color: white
    style: bold
  warning:
    color: yellow
    style: bold
  error:
    color: black
    background: red
    style: bold
  critical:
    color: black
    background: bright_red
    style: bold
```

## Environment Variables

Log coloring can be controlled using the following environment variables:

- `LOGKISS_DISABLE_COLOR`: Disable coloring (values: 1, true, yes)
- `NO_COLOR`: Industry standard for disabling colors (any value)
- `LOGKISS_LEVEL_FORMAT`: Specify the display length of log level names (value: number, default: 5)
  - Example: `LOGKISS_LEVEL_FORMAT=5` adjusts all log level names to 5 characters
  - WARNING is specially shortened to "WARN"
  - Level names longer than the specified length are truncated, and shorter names are padded with spaces

## Notes

1. If the configuration file fails to load, default settings will be used
2. Undefined colors or styles are ignored
3. Each section (levels, messages, elements) can be configured independently
4. If settings for specific log levels or elements are omitted, default settings will be used for those parts
