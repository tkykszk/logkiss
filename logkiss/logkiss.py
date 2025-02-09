#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
from logging import LogRecord, StreamHandler, Formatter, Filter
from pathlib import Path
from typing import Optional, Union, TextIO, Dict, Any
from dataclasses import dataclass
from yaml import safe_load

# エクスポートする関数やクラスを定義
__all__ = [
    'KissConsoleHandler',
    'ColoredFormatter',
    'KissLogger',
    'use_console_handler',
    'PathShortenerFilter',
]

# デバッグモードの設定
DEBUG = os.environ.get('LOGKISS_DEBUG', '').lower() in ('1', 'true', 'yes')

# パス短縮の設定
_path_shorten = os.environ.get('LOGKISS_PATH_SHORTEN', '0')
try:
    PATH_SHORTEN = int(_path_shorten)
except ValueError:
    # 数値以外の場合は無効化
    PATH_SHORTEN = 0

@dataclass
class ColorConfig:
    """色設定を保持するデータクラス"""
    color: Optional[str] = None
    background: Optional[str] = None
    style: Optional[str] = None

class Colors:
    """ANSIエスケープシーケンス"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKE = '\033[9m'
    
    # 前景色（文字色）
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # 背景色
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # 明るい前景色
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # 明るい背景色
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
        """色名からエスケープシーケンスを取得"""
        if not name:
            return ''
        
        # 背景色の場合はプレフィックスを追加
        if name.startswith('bg_'):
            name = f'BG_{name[3:].upper()}'
        else:
            name = name.upper()
        
        return getattr(cls, name, '')

class ColorManager:
    """色設定を管理するクラス"""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Args:
            config_path: 色設定ファイルのパス
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """色設定を読み込む"""
        # デフォルトの色設定
        default_config = {
            'levels': {
                'DEBUG': {'fg': 'blue'},
                'INFO': {'fg': 'green'},
                'WARNING': {'fg': 'yellow'},
                'ERROR': {'fg': 'red'},
                'CRITICAL': {'fg': 'red', 'style': 'bold'},
            },
            'elements': {
                'timestamp': {'fg': 'white'},
                'filename': {'fg': 'cyan'},
                'message': {
                    'DEBUG': {'fg': 'blue'},
                    'INFO': {'fg': 'green'},
                    'WARNING': {'fg': 'yellow'},
                    'ERROR': {'fg': 'red'},
                    'CRITICAL': {'fg': 'red', 'style': 'bold'},
                }
            }
        }
        
        # 設定ファイルがあれば読み込む
        if self.config_path:
            try:
                with open(self.config_path) as f:
                    config = safe_load(f)
                return {**default_config, **config}
            except Exception:
                return default_config
        return default_config
    
    def get_level_color(self, level: int) -> Dict[str, Any]:
        """レベルに応じた色設定を取得"""
        level_name = logging.getLevelName(level)
        return self.config['levels'].get(level_name, {})
    
    def get_message_color(self, level: int) -> Dict[str, Any]:
        """メッセージの色設定を取得"""
        level_name = logging.getLevelName(level)
        return self.config['elements']['message'].get(level_name, {})
    
    def get_element_color(self, element: str) -> Dict[str, Any]:
        """要素の色設定を取得"""
        return self.config['elements'].get(element, {})
    
    def apply_color(self, text: str, config: Dict[str, Any]) -> str:
        """テキストに色を適用"""
        if not config:
            return text
        
        # コードを生成
        codes = []
        
        # 前景色
        if 'fg' in config:
            codes.append(getattr(Colors, config['fg'].upper(), ''))
        
        # 背景色
        if 'bg' in config:
            codes.append(getattr(Colors, f"BG_{config['bg'].upper()}", ''))
        
        # スタイル
        if 'style' in config:
            codes.append(getattr(Colors, config['style'].upper(), ''))
        
        # コードを適用
        return "".join(codes) + text + Colors.RESET
    
    def colorize_level(self, levelname: str) -> str:
        """レベル名を色付け"""
        level = logging.getLevelName(levelname)
        level_config = self.get_level_color(level)
        return self.apply_color(levelname, level_config)
    
    def colorize_filename(self, filename: str) -> str:
        """ファイル名を色付け"""
        filename_config = self.get_element_color('filename')
        return self.apply_color(filename, filename_config)
    
    def colorize_timestamp(self, timestamp: str) -> str:
        """タイムスタンプを色付け"""
        timestamp_config = self.get_element_color('timestamp')
        return self.apply_color(timestamp, timestamp_config)
    
    def colorize_message(self, message: str, level: int) -> str:
        """メッセージを色付け"""
        message_config = self.get_message_color(level)
        return self.apply_color(message, message_config)

class PathShortenerFilter(Filter):
    """パスを短縮して表示するフィルター

    長いパスを ".../<last_n_components>" の形式に短縮します。
    例: "/very/long/path/to/module.py" -> ".../to/module.py"

    環境変数 LOGKISS_PATH_SHORTEN で制御:
    - 0または無効な値: パス短縮を無効化
    - 正の整数: 最後からその数のコンポーネントを表示
    """
    def __init__(self):
        super().__init__()
    
    def filter(self, record):
        if PATH_SHORTEN > 0:
            # パスを分割
            components = record.pathname.split('/')
            
            # ファイル名を含む最後のPATH_SHORTEN個を取得
            if len(components) > PATH_SHORTEN:
                shortened = '/'.join(['...'] + components[-PATH_SHORTEN:])
                record.filename = shortened
        
        return True

class ColoredFormatter(Formatter):
    """カラー対応のフォーマッター"""

    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None,
                 style: str = '%', validate: bool = True,
                 color_config: Optional[Union[str, Path]] = None):
        """
        Args:
            fmt: フォーマット文字列
            datefmt: 日付フォーマット文字列
            style: フォーマットスタイル（'%', '{', '$'のいずれか）
            validate: フォーマット文字列を検証するかどうか
            color_config: 色設定ファイルのパス
        """
        if fmt is None:
            fmt = '%(asctime)s %(levelname)s | %(filename)s: %(lineno)d | %(message)s'
        super().__init__(fmt, datefmt, style, validate)
        self.color_manager = ColorManager(color_config)

    def format(self, record: LogRecord) -> str:
        """ログレコードをフォーマット"""
        # 色を設定
        record.levelname = self.color_manager.colorize_level(record.levelname)
        record.filename = self.color_manager.colorize_filename(record.filename)
        record.asctime = self.color_manager.colorize_timestamp(self.formatTime(record, self.datefmt))
        record.message = self.color_manager.colorize_message(record.getMessage(), record.levelno)

        # フォーマット
        return Formatter.format(self, record)

class KissConsoleHandler(StreamHandler):
    """カラー対応のコンソールハンドラー"""
    
    def __init__(self, stream: Optional[TextIO] = None, force_color: bool = True,
                 color_config: Optional[Union[str, Path]] = None):
        """
        Args:
            stream: 出力先のストリーム。デフォルトはsys.stderr
            force_color: 強制的に色付き出力を有効にするかどうか
            color_config: 色設定ファイルのパス
        """
        # デフォルトはsys.stderr
        if stream is None:
            stream = sys.stderr
        
        super().__init__(stream)
        self.force_color = force_color
        self.color_config = color_config
        self.formatter = ColoredFormatter(color_config=color_config)
        self.setFormatter(self.formatter)
        
        # パス短縮フィルターを追加
        self.addFilter(PathShortenerFilter())

    def format(self, record: LogRecord) -> str:
        """ログレコードをフォーマット"""
        # フォーマッターが設定されていない場合は、デフォルトのフォーマッターを設定
        if self.formatter is None:
            self.formatter = ColoredFormatter()
        return self.formatter.format(record)

    def emit(self, record: LogRecord) -> None:
        """ログレコードを出力"""
        try:
            msg = self.format(record)
            stream = self.stream
            # if exception information is present, it's formatted as text and appended to msg
            stream.write(msg + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

class KissLogger(logging.Logger):
    """カラー対応のロガー"""
    
    def __init__(self, name: str):
        """
        Args:
            name: ロガー名
        """
        super().__init__(name)
    
    def makeRecord(self, name: str, level: int, fn: str, lno: int, msg: str,
                  args: tuple, exc_info: Optional[bool],
                  func: Optional[str] = None,
                  extra: Optional[Dict[str, Any]] = None,
                  sinfo: Optional[str] = None) -> LogRecord:
        """ログレコードを作成"""
        # extraから渡されたファイル名と行番号を使用
        if extra is not None and '_filename' in extra and '_lineno' in extra:
            fn = extra['_filename']
            lno = extra['_lineno']
            # extraから削除
            extra = None
        
        # ファイル名を相対パスに変換
        if fn and os.path.isabs(fn):
            try:
                fn = os.path.relpath(fn)
            except ValueError:
                # 相対パスに変換できない場合は、ファイル名のみを使用
                fn = os.path.basename(fn)
        
        # 親クラスのメソッドを呼び出し
        return super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)

# 通常のConsoleHandlerを使用する場合のヘルパー関数
def use_console_handler(logger: Optional[logging.Logger] = None) -> None:
    """通常のConsoleHandlerを使用するように設定"""
    if logger is None:
        logger = logging.getLogger()
    
    # KissConsoleHandlerを削除
    for handler in logger.handlers[:]:
        if isinstance(handler, KissConsoleHandler):
            logger.removeHandler(handler)
    
    # 通常のConsoleHandlerを追加
    handler = StreamHandler()
    handler.setFormatter(Formatter(
        fmt='%(asctime)s,%(msecs)03d %(levelname)-5s | %(filename)s:%(lineno)3d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(handler)

# バージョン情報
__version__ = '0.1.0'
