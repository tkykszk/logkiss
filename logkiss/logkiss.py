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
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime

# Exported functions and classes
__all__ = [
    'KissConsoleHandler',
    'ColoredFormatter',
    'KissLogger',
    'use_console_handler',
    'PathShortenerFilter',
    'KissFileHandler',
    'KissRotatingFileHandler',
    'KissTimedRotatingFileHandler',
]

# Debug mode settings
DEBUG = os.environ.get('LOGKISS_DEBUG', '').lower() in ('1', 'true', 'yes')

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
                'ERROR': {'fg': 'red'},
                'CRITICAL': {'fg': 'red', 'style': 'bold'},
            },
            'elements': {
                'timestamp': {'fg': 'white'},
                'filename': {'fg': 'cyan'},
                'message': {
                    'DEBUG': {'fg': 'blue'},
                    'INFO': {'fg': 'white'},
                    'WARNING': {'fg': 'yellow'},
                    'ERROR': {'fg': 'red'},
                    'CRITICAL': {'fg': 'red', 'style': 'bold'},
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
    
    def get_level_color(self, level: int) -> Dict[str, Any]:
        """Get color settings for a log level"""
        level_name = logging.getLevelName(level)
        return self.config['levels'].get(level_name, {})
    
    def get_message_color(self, level: int) -> Dict[str, Any]:
        """Get color settings for a log message"""
        level_name = logging.getLevelName(level)
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
    
    def colorize_level(self, levelname: str) -> str:
        """Colorize log level name"""
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
    """Formatter that applies colors to log messages based on their level"""

    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None,
                 style: str = '%', validate: bool = True,
                 color_config: Optional[Union[str, Path]] = None,
                 use_color: bool = True):
        """
        Args:
            fmt: Format string
            datefmt: Date format string
            style: Format style ('%', '{', '$')
            validate: Validate format string
            color_config: Path to color configuration file
            use_color: Apply colors to log messages
        """
        if fmt is None:
            fmt = '%(asctime)s %(levelname)s | %(filename)s: %(lineno)d | %(message)s'
        super().__init__(fmt, datefmt, style, validate)
        self.color_manager = ColorManager(color_config)
        self.use_color = use_color

    def format(self, record: LogRecord) -> str:
        """Format log record with colors"""
        # Apply colors
        if self.use_color:
            record.levelname = self.color_manager.colorize_level(record.levelname)
            record.filename = self.color_manager.colorize_filename(record.filename)
            record.asctime = self.color_manager.colorize_timestamp(self.formatTime(record, self.datefmt))
            record.message = self.color_manager.colorize_message(record.getMessage(), record.levelno)
        else:
            record.message = record.getMessage()

        # Format record
        return Formatter.format(self, record)

class KissConsoleHandler(StreamHandler):
    """Handler that outputs colored log messages to the console"""
    
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
        # Apply colors if outputting to sys.stderr or sys.stdout
        use_color = stream is None or stream is sys.stderr or stream is sys.stdout
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

class KissFileHandler(FileHandler):
    """Handler that outputs colored log messages to a file"""

    def __init__(self, filename: str,
                 mode: str = 'a', encoding: Optional[str] = None,
                 delay: bool = False,
                 color_config: Optional[Union[str, Path]] = None):
        """
        Args:
            filename: Log file path
            mode: File open mode
            encoding: File encoding
            delay: Delay file open
            color_config: Path to color configuration file
        """
        super().__init__(filename, mode, encoding, delay)
        self.formatter = ColoredFormatter(color_config=color_config, use_color=False)
        self.setFormatter(self.formatter)

class KissRotatingFileHandler(RotatingFileHandler):
    """Handler that outputs colored log messages to a rotating file"""

    def __init__(self, filename: str,
                 mode: str = 'a', maxBytes: int = 0,
                 backupCount: int = 0, encoding: Optional[str] = None,
                 delay: bool = False,
                 color_config: Optional[Union[str, Path]] = None):
        """
        Args:
            filename: Log file path
            mode: File open mode
            maxBytes: Maximum log file size
            backupCount: Number of backup files
            encoding: File encoding
            delay: Delay file open
            color_config: Path to color configuration file
        """
        super().__init__(filename, mode, maxBytes, backupCount, encoding, delay)
        self.formatter = ColoredFormatter(color_config=color_config, use_color=False)
        self.setFormatter(self.formatter)

class KissTimedRotatingFileHandler(TimedRotatingFileHandler):
    """Handler that outputs colored log messages to a timed rotating file"""

    def __init__(self, filename: str,
                 when: str = 'h', interval: int = 1,
                 backupCount: int = 0, encoding: Optional[str] = None,
                 delay: bool = False, utc: bool = False,
                 atTime: Optional[datetime.time] = None,
                 color_config: Optional[Union[str, Path]] = None):
        """
        Args:
            filename: Log file path
            when: Rotation timing
            interval: Rotation interval
            backupCount: Number of backup files
            encoding: File encoding
            delay: Delay file open
            utc: Use UTC time
            atTime: Rotation time
            color_config: Path to color configuration file
        """
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime)
        self.formatter = ColoredFormatter(color_config=color_config, use_color=False)
        self.setFormatter(self.formatter)

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

# Helper function to use a standard ConsoleHandler
def use_console_handler(logger: Optional[logging.Logger] = None) -> None:
    """Configure the logger to use a standard ConsoleHandler"""
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

# Version information
__version__ = '0.1.0'
