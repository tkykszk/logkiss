"""Core module of logkiss.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.

This module provides the core functionality of logkiss,
including logging setup and configuration management.
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
from pathlib import Path
from typing import Optional, Union, TextIO, Dict, Any
from dataclasses import dataclass
from yaml import safe_load
from logging import FileHandler, LogRecord, StreamHandler, Formatter, Filter
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# Exported functions and classes
__all__ = [
    'KissConsoleHandler',
    'ColoredFormatter',
    'KissLogger',
    'use_console_handler',
    'PathShortenerFilter',
    'setup_from_yaml',
    'setup_from_env',
]

# Debug mode settings
DEBUG = os.environ.get('LOGKISS_DEBUG', '').lower() in ('1', 'true', 'yes')

# Level format settings
_level_format = os.environ.get('LOGKISS_LEVEL_FORMAT', '5')
try:
    LEVEL_FORMAT = int(_level_format)
except ValueError:
    LEVEL_FORMAT = 5

# Path shortening settings
_path_shorten = os.environ.get('LOGKISS_PATH_SHORTEN', '0')
try:
    PATH_SHORTEN = int(_path_shorten)
except ValueError:
    # Disable if not a number
    PATH_SHORTEN = 0

@dataclass
class ColorConfig:
    """Data class to hold color settings"""
    color: Optional[str] = None
    background: Optional[str] = None
    style: Optional[str] = None

class Colors:
    """ANSI escape sequences"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKE = '\033[9m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Bright foreground colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Bright background colors
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'
    
    @classmethod
    def get_color(cls, name: str) -> str:
        """Get ANSI escape sequence from color name"""
        if not name:
            return ''
        
        # Add prefix for background colors
        if name.startswith('bg_'):
            name = f'BG_{name[3:].upper()}'
        else:
            name = name.upper()
        
        return getattr(cls, name, '')

class ColorManager:
    """Class to manage color settings"""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Args:
            config_path: Path to color configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load color settings from file"""
        # Default color settings
        default_config = {
            'levels': {
                'DEBUG': {'fg': 'blue'},
                'INFO': {'fg': 'white'},
                'WARNING': {'fg': 'yellow'},
                'ERROR': {'fg': 'black', 'bg': 'red'},
                'CRITICAL': {'fg': 'black', 'bg': 'bright_red', 'style': 'bold'},
            },
            'elements': {
                'timestamp': {'fg': 'white'},
                'filename': {'fg': 'cyan'},
                'message': {
                    'DEBUG': {'fg': 'blue'},
                    'INFO': {'fg': 'white'},
                    'WARNING': {'fg': 'yellow'},
                    'ERROR': {'fg': 'black', 'bg': 'red'},
                    'CRITICAL': {'fg': 'black', 'bg': 'bright_red', 'style': 'bold'},
                }
            }
        }
        
        # Load configuration from file if available
        if self.config_path:
            try:
                with open(self.config_path) as f:
                    config = safe_load(f)
                return {**default_config, **config}
            except Exception:
                return default_config
        return default_config
    
    def get_level_color(self, level: Union[int, str]) -> Dict[str, Any]:
        """Get color settings for a log level"""
        if isinstance(level, int):
            level_name = logging.getLevelName(level)
        else:
            level_name = level
        return self.config['levels'].get(level_name, {})
    
    def get_message_color(self, level: Union[int, str]) -> Dict[str, Any]:
        """Get color settings for a log message"""
        if isinstance(level, int):
            level_name = logging.getLevelName(level)
        else:
            level_name = level
        return self.config['elements']['message'].get(level_name, {})
    
    def get_element_color(self, element: str) -> Dict[str, Any]:
        """Get color settings for a log element"""
        return self.config['elements'].get(element, {})
    
    def apply_color(self, text: str, config: Dict[str, Any]) -> str:
        """Apply color settings to text"""
        if not config:
            return text
        
        # Generate ANSI escape sequence
        codes = []
        
        # Foreground color
        if 'fg' in config:
            codes.append(getattr(Colors, config['fg'].upper(), ''))
        
        # Background color
        if 'bg' in config:
            codes.append(getattr(Colors, f"BG_{config['bg'].upper()}", ''))
        
        # Style
        if 'style' in config:
            codes.append(getattr(Colors, config['style'].upper(), ''))
        
        # Apply ANSI escape sequence
        return "".join(codes) + text + Colors.RESET
    
    def colorize_level(self, levelname: str, levelno: Optional[int] = None) -> str:
        """Colorize log level name"""
        if levelno is not None:
            level_config = self.get_level_color(levelno)
        else:
            level = logging.getLevelName(levelname)
            level_config = self.get_level_color(level)
        return self.apply_color(levelname, level_config)
    
    def colorize_filename(self, filename: str) -> str:
        """Colorize filename"""
        filename_config = self.get_element_color('filename')
        return self.apply_color(filename, filename_config)
    
    def colorize_timestamp(self, timestamp: str) -> str:
        """Colorize timestamp"""
        timestamp_config = self.get_element_color('timestamp')
        return self.apply_color(timestamp, timestamp_config)
    
    def colorize_message(self, message: str, level: int) -> str:
        """Colorize log message"""
        message_config = self.get_message_color(level)
        return self.apply_color(message, message_config)

class PathShortenerFilter(Filter):
    """Filter to shorten paths in log messages

    Shortens long paths to ".../<last_n_components>" format.
    Example: "/very/long/path/to/module.py" -> ".../to/module.py"

    Controlled by environment variable LOGKISS_PATH_SHORTEN:
    - 0 or invalid value: Disable path shortening
    - Positive integer: Show last n components
    """
    def __init__(self):
        super().__init__()
    
    def filter(self, record):
        if PATH_SHORTEN > 0:
            # Split path into components
            components = record.pathname.split('/')
            
            # Get last n components
            if len(components) > PATH_SHORTEN:
                shortened = '/'.join(['...'] + components[-PATH_SHORTEN:])
                record.filename = shortened
        
        return True

class ColoredFormatter(Formatter):
    """Formatter that applies colors to log messages based on their level.
    
    This formatter extends the standard logging.Formatter to add color
    to log messages based on their level. Colors can be customized through
    a configuration file.
    
    To disable colors, set use_color=False when creating the formatter:
        formatter = ColoredFormatter(use_color=False)
    
    Note:
        When using KissConsoleHandler, a ColoredFormatter is automatically
        created with use_color set based on the output stream. To disable
        colors with KissConsoleHandler, you need to create a ColoredFormatter
        with use_color=False and set it explicitly:
            handler = KissConsoleHandler()
            formatter = ColoredFormatter(use_color=False)
            handler.setFormatter(formatter)
    
    Environment Variables:
        The following environment variables can be used to control coloring:
        - LOGKISS_DISABLE_COLOR: Disable colors (values: 1, true, yes)
        - NO_COLOR: Industry standard to disable colors (any value)
        These environment variables override the use_color parameter.
        
        The following environment variable can be used to control level name formatting:
        - LOGKISS_LEVEL_FORMAT: Specify the length of level names (value: integer, default: 5)
          For example, LOGKISS_LEVEL_FORMAT=5 will adjust all level names to be 5 characters.
          WARNING is specially shortened to "WARN".
          Level names longer than the specified length will be truncated,
          and shorter ones will be padded with spaces.
    
    Args:
        fmt: Format string for log messages. Default is 
             '%(asctime)s %(levelname)s | %(filename)s: %(lineno)d | %(message)s'
        datefmt: Date format string. Default is None (ISO8601 format).
        style: Format style ('%', '{', '$'). Default is '%'.
        validate: Whether to validate format string. Default is True.
        color_config: Path to color configuration file. Default is None.
        use_color: Whether to apply colors to log messages. Default is True.
    """
    
    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None,
                 style: str = '%', validate: bool = True,
                 color_config: Optional[Union[str, Path]] = None,
                 use_color: bool = True,
                 format: Optional[str] = None):
        """
        Args:
            fmt: Format string
            datefmt: Date format string
            style: Format style ('%', '{', '$')
            validate: Validate format string
            color_config: Path to color configuration file
            use_color: Apply colors to log messages
        """
        if fmt is None and format is not None:
            fmt = format
        elif fmt is None:
            fmt = '%(asctime)s %(levelname)s | %(filename)s: %(lineno)d | %(message)s'
        super().__init__(fmt, datefmt, style, validate)
        self.color_manager = ColorManager(color_config)
        
        # Check if color should be disabled via environment variable
        disable_color = os.environ.get('LOGKISS_DISABLE_COLOR', '').lower() in ('1', 'true', 'yes')
        
        # Environment variables take precedence over the use_color parameter
        if disable_color:
            self.use_color = False
        else:
            self.use_color = use_color

    def format(self, record: LogRecord) -> str:
        """Format log record with colors"""
        # Save original levelname and level number
        orig_levelname = record.levelname
        levelno = record.levelno
        
        # Format level name based on LEVEL_FORMAT
        if LEVEL_FORMAT > 0:
            # Special case for WARNING -> WARN
            if orig_levelname == 'WARNING':
                display_levelname = 'WARN'
            else:
                display_levelname = orig_levelname
            
            # Truncate or pad level name
            if len(display_levelname) > LEVEL_FORMAT:
                # Truncate
                display_levelname = display_levelname[:LEVEL_FORMAT]
            elif len(display_levelname) < LEVEL_FORMAT:
                # Pad
                display_levelname = display_levelname.ljust(LEVEL_FORMAT)
                
            # Replace levelname with formatted version
            record.levelname = display_levelname
        
        # Apply colors
        if self.use_color:
            # Use original level for color lookup, but apply to formatted level name
            record.levelname = self.color_manager.colorize_level(record.levelname, levelno)
            
            record.filename = self.color_manager.colorize_filename(record.filename)
            record.asctime = self.color_manager.colorize_timestamp(self.formatTime(record, self.datefmt))
            record.message = self.color_manager.colorize_message(record.getMessage(), levelno)
        else:
            record.message = record.getMessage()

        # Format record
        return Formatter.format(self, record)

class KissConsoleHandler(StreamHandler):
    """Handler that outputs colored log messages to the console.
    
    This handler extends the standard logging.StreamHandler to add color
    to log messages based on their level. Colors can be customized through
    a configuration file.
    
    By default, colors are enabled when outputting to sys.stderr or sys.stdout.
    To disable colors, you need to create a ColoredFormatter with use_color=False
    and set it explicitly:
        handler = KissConsoleHandler()
        formatter = ColoredFormatter(use_color=False)
        handler.setFormatter(formatter)
    
    Environment Variables:
        The following environment variables can be used to control coloring:
        - LOGKISS_DISABLE_COLOR: Disable colors (values: 1, true, yes)
        - NO_COLOR: Industry standard to disable colors (any value)
        These environment variables override the use_color parameter of the formatter.
    
    Args:
        stream: Output stream. Default is sys.stderr.
        color_config: Path to color configuration file. Default is None.
    """
    
    def __init__(self, stream: Optional[TextIO] = None,
                 color_config: Optional[Union[str, Path]] = None):
        """
        Args:
            stream: Output stream
            color_config: Path to color configuration file
        """
        # Default to sys.stderr
        if stream is None:
            stream = sys.stderr
        
        super().__init__(stream)
        
        # Check environment variables for disabling color
        disable_color = os.environ.get('LOGKISS_DISABLE_COLOR', '').lower() in ('1', 'true', 'yes')
        
        # Apply colors if not disabled by env var and outputting to sys.stderr or sys.stdout
        use_color = not disable_color and (stream is None or stream is sys.stderr or stream is sys.stdout)
        
        self.formatter = ColoredFormatter(color_config=color_config, use_color=use_color)
        self.setFormatter(self.formatter)
        self.setLevel(logging.DEBUG)  # Set default level to DEBUG
        
        # Add path shortening filter
        self.addFilter(PathShortenerFilter())

    def format(self, record: LogRecord) -> str:
        """Format log record"""
        # Set default formatter if not set
        if self.formatter is None:
            self.formatter = ColoredFormatter()
        return self.formatter.format(record)

    def emit(self, record: LogRecord) -> None:
        """Output log record"""
        try:
            msg = self.format(record)
            stream = self.stream
            # if exception information is present, it's formatted as text and appended to msg
            stream.write(msg + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

class KissLogger(logging.Logger):
    """Logger that uses colored output by default"""

    def __init__(self, name: str):
        """Initialize the logger with the specified name"""
        super().__init__(name)
        self.setLevel(logging.WARNING)  # Set default level to WARNING

    def setLevel(self, level: int) -> None:
        """Set the logging level for both logger and handlers"""
        super().setLevel(level)  # Call parent's setLevel
        # Update handler levels
        for handler in self.handlers:
            handler.setLevel(level)
    
    def makeRecord(self, name: str, level: int, fn: str, lno: int, msg: str,
                   args: tuple, exc_info: Optional[bool],
                   func: Optional[str] = None,
                   extra: Optional[Dict[str, Any]] = None,
                   sinfo: Optional[str] = None) -> LogRecord:
        """Create a LogRecord with the given arguments"""
        # Get caller information from extra
        if extra is not None:
            if '_filename' in extra:
                fn = extra['_filename']
            if '_lineno' in extra:
                lno = extra['_lineno']

        # Shorten path if enabled
        if os.environ.get('LOGKISS_PATH_SHORTEN', '1').lower() in ('1', 'true', 'yes'):
            # Use only filename
            fn = os.path.basename(fn)

        # Create LogRecord
        record = super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
        return record

    def reload_config(self) -> None:
        """Reload configuration from the original source.
        
        This method reloads the logger configuration from the original YAML file
        if it was configured using setup_from_yaml, or from environment variables
        if it was configured using setup_from_env.
        
        Raises:
            ValueError: If the logger was not configured using setup_from_yaml
                      or setup_from_env.
        """
        # Check if config path is available
        if hasattr(self, 'config_path'):
            # Remove existing handlers
            for handler in self.handlers[:]:
                self.removeHandler(handler)
            
            # Reload from YAML
            setup_from_yaml(self.config_path)
        else:
            # Reload from environment variables
            setup_from_env()

# Helper function to use a standard ConsoleHandler
def use_console_handler(logger: Optional[logging.Logger] = None) -> None:
    """Configure the logger to use a standard StreamHandler instead of KissConsoleHandler.
    
    This function removes any existing KissConsoleHandler from the specified logger
    and adds a standard StreamHandler with a basic formatter. This is useful when
    you want to disable the colored output and use a simple console handler.
    
    Args:
        logger: Logger to configure. Default is None (root logger).
        
    Returns:
        None
        
    Example:
        >>> import logkiss as logging
        >>> logger = logging.getLogger(__name__)
        >>> logging.use_console_handler(logger)
        >>> logger.info('This message will be displayed without color')
    """
    # Get the root logger if no logger is specified
    if logger is None:
        logger = logging.getLogger()
    
    # Remove KissConsoleHandler
    for handler in logger.handlers[:]:
        if isinstance(handler, KissConsoleHandler):
            logger.removeHandler(handler)
    
    # Add standard ConsoleHandler
    handler = StreamHandler()
    handler.setFormatter(Formatter(
        fmt='%(asctime)s,%(msecs)03d %(levelname)-5s | %(filename)s:%(lineno)3d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(handler)


def setup_from_yaml(config_path: Union[str, Path]) -> logging.Logger:
    """Set up logging configuration from a YAML file.
    
    Args:
        config_path: Path to YAML configuration file
        
    Returns:
        Configured logger instance
        
    Raises:
        ValueError: If config file does not exist
        yaml.YAMLError: If config file is invalid YAML
    """
    config_path = Path(config_path)
    if not config_path.exists():
        raise ValueError(f"Configuration file not found: {config_path}")
    
    with open(config_path) as f:
        config = safe_load(f)
    
    # Get root logger
    logger = logging.getLogger()
    
    # Configure formatters
    formatters = {}
    for name, formatter_config in config.get('formatters', {}).items():
        formatters[name] = ColoredFormatter(**formatter_config)
    
    # Configure handlers
    for name, handler_config in config.get('handlers', {}).items():
        handler_class = handler_config.pop('class')
        formatter = handler_config.pop('formatter', None)
        
        # Create handler instance
        if handler_class == 'logging.StreamHandler':
            handler = KissConsoleHandler()
        elif handler_class == 'logging.FileHandler':
            handler = FileHandler(**handler_config)
        elif handler_class == 'logging.TimedRotatingFileHandler':
            handler = TimedRotatingFileHandler(**handler_config)
        else:
            continue
        
        # Set formatter if specified
        if formatter and formatter in formatters:
            handler.setFormatter(formatters[formatter])
        
        logger.addHandler(handler)
    
    # Configure root logger
    root_config = config.get('root', {})
    
    # Check environment variables first
    env_level = os.environ.get('LOGKISS_LEVEL')
    if env_level:
        logger.setLevel(getattr(logging, env_level.upper()))
    elif 'level' in root_config:
        logger.setLevel(getattr(logging, root_config['level']))
    
    # Store config path for reload
    logger.config_path = config_path
    
    return logger


def setup_from_env() -> logging.Logger:
    """Set up logging configuration from environment variables.
    
    Environment variables:
        LOGKISS_LEVEL: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        LOGKISS_FORMAT: Log format string
        LOGKISS_DISABLE_COLOR: Disable colored output if 'true'
        
    Returns:
        Configured logger instance
    """
    # Get root logger
    logger = logging.getLogger()
    
    # Configure level
    level = os.environ.get('LOGKISS_LEVEL', 'WARNING')
    logger.setLevel(getattr(logging, level.upper()))
    
    # Create a console handler
    handler = StreamHandler(sys.stderr)
    
    # Configure formatter
    fmt = os.environ.get('LOGKISS_FORMAT',
                        '%(asctime)s,%(msecs)03d %(levelname)-5s | %(filename)s:%(lineno)3d | %(message)s')
    datefmt = os.environ.get('LOGKISS_DATEFMT', '%Y-%m-%d %H:%M:%S')
    
    # Determine color usage based on environment variable
    use_color = True  # Default is to use color
    if os.environ.get('LOGKISS_DISABLE_COLOR', '').lower() in ('1', 'true', 'yes'):
        use_color = False
    
    # Create formatter with color settings
    formatter = ColoredFormatter(
        fmt=fmt,
        datefmt=datefmt,
        use_color=use_color
    )
    
    # Set the formatter on the handler
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger
