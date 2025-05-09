# LOGKISS Configuration Guide

LOGKISS allows you to customize log colors and styles using a YAML configuration file. This configuration file lets you control colors and styles for log levels, messages, and other elements in detail.

## Configuration File Structure

The configuration file consists of two main sections:

1. `levels`: Color settings for log level names
2. `elements`: Color settings for elements like timestamps, filenames, and messages

### Basic Structure

```yaml
levels:
  DEBUG:
    fg: blue
  INFO:
    fg: white
  WARNING:
    fg: yellow
  ERROR:
    fg: black
    bg: red
  CRITICAL:
    fg: black
    bg: bright_red
    style: bold

elements:
  timestamp:
    fg: white
  filename:
    fg: cyan
  message:
    DEBUG:
      fg: blue
    INFO:
      fg: white
    WARNING:
      fg: yellow
    ERROR:
      fg: black
      bg: red
    CRITICAL:
      fg: black
      bg: bright_red
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

This character limit is intended to keep log formatting clean. If you want to change the character limit, use the `LOGKISS_LEVEL_FORMAT` environment variable.

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
- reverse: Reversed colors
- hidden: Hidden text
- strike: Strikethrough text

## How to Use Configuration

1. Create a configuration file:

```python
# logkiss.yaml
levels:
  DEBUG:
    fg: cyan
    style: bold
  ERROR:
    fg: red
    style: bold
    bg: black
```

1. Specify the configuration file when initializing the logger:

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
  DEBUG:
    fg: blue
  INFO:
    fg: white
  WARNING:
    fg: yellow
  ERROR:
    fg: black
    bg: red
  CRITICAL:
    fg: black
    bg: bright_red
    style: bold

elements:
  timestamp:
    fg: white
  filename:
    fg: cyan
  message:
    DEBUG:
      fg: blue
    INFO:
      fg: white
    WARNING:
      fg: yellow
    ERROR:
      fg: black
      bg: red
    CRITICAL:
      fg: black
      bg: bright_red
      style: bold
```

## Environment Variables

Log coloring and configuration can be controlled using the following environment variables:

- `LOGKISS_DISABLE_COLOR`: Disable coloring (values: 1, true, yes)
- `NO_COLOR`: Industry standard for disabling colors (any value) - **DEPRECATED**: Use `LOGKISS_DISABLE_COLOR` instead
- `LOGKISS_LEVEL_FORMAT`: Specify the display length of log level names (value: number, default: 5)
  - Example: `LOGKISS_LEVEL_FORMAT=5` adjusts all log level names to 5 characters
  - WARNING is specially shortened to "WARN"
  - Level names longer than the specified length are truncated, and shorter names are padded with spaces
- `LOGKISS_CONFIG`: Specify the path to a configuration file
- `LOGKISS_SKIP_CONFIG`: Skip loading any configuration file (values: 1, true, yes)
- `LOGKISS_PATH_SHORTEN`: Shorten file paths in logs (value: number, default: 0, 0 means no shortening)

## Configuration File Search Order

When not explicitly specified, LOGKISS searches for configuration files in the following order:

1. Path specified in code when creating a logger
2. Path specified in `LOGKISS_CONFIG` environment variable
3. Standard locations:
   - Windows: `%APPDATA%\logkiss\config.yaml` or `%USERPROFILE%\.config\logkiss\config.yaml`
   - Other OS: `~/.config/logkiss/config.yaml`

## Notes

1. If the configuration file fails to load, default settings will be used
2. Undefined colors or styles are ignored
3. Each section (levels, elements) can be configured independently
4. If settings for specific log levels or elements are omitted, default settings will be used for those parts
5. In the configuration file, use `fg` instead of `color` and `bg` instead of `background`
