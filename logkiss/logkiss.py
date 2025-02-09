#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import yaml
from dataclasses import dataclass
from logging import LogRecord, Formatter, StreamHandler, Filter
from pathlib import Path
from typing import Optional, Union, Dict, Any, TextIO

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
    """色の管理を行うクラス"""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """設定ファイルを読み込む"""
        if not config_path:
            return {}
        
        try:
            with open(config_path) as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Failed to load color config: {e}", file=sys.stderr)
            return {}
    
    def get_level_color(self, level: int) -> ColorConfig:
        """ログレベルに対応する色設定を取得"""
        # デフォルトの色設定
        default_colors = {
            logging.DEBUG: ColorConfig(color='cyan', style='bold'),
            logging.INFO: ColorConfig(color='white', style='bold'),
            logging.WARNING: ColorConfig(color='bright_yellow', style='bold'),
            logging.ERROR: ColorConfig(color='bright_red', style='bold'),
            logging.CRITICAL: ColorConfig(color='bright_white', style='bold', background='bright_red'),
        }
        
        # 設定ファイルから色設定を取得
        level_name = logging.getLevelName(level).lower()
        config = self.config.get('levels', {}).get(level_name, {})
        
        # デフォルト値を取得
        default = default_colors.get(level, ColorConfig())
        
        # 設定ファイルの値とデフォルト値をマージ
        return ColorConfig(
            color=config.get('color', default.color),
            background=config.get('background', default.background),
            style=config.get('style', default.style)
        )
    
    def get_message_color(self, level: int) -> ColorConfig:
        """メッセージに対応する色設定を取得"""
        # 設定ファイルから色設定を取得
        level_name = logging.getLevelName(level).lower()
        config = self.config.get('messages', {}).get(level_name, {})
        
        # デフォルト値を取得
        default = ColorConfig()
        
        # 設定ファイルの値とデフォルト値をマージ
        return ColorConfig(
            color=config.get('color', default.color),
            background=config.get('background', default.background),
            style=config.get('style', default.style)
        )
    
    def get_element_color(self, element: str) -> ColorConfig:
        """要素に対応する色設定を取得"""
        # デフォルトの色設定
        default_colors = {
            'timestamp': ColorConfig(color='blue', style='dim'),
            'filename': ColorConfig(color='bright_black', style='dim'),
        }
        
        # 設定ファイルから色設定を取得
        config = self.config.get('elements', {}).get(element, {})
        
        # デフォルト値を取得
        default = default_colors.get(element, ColorConfig())
        
        # 設定ファイルの値とデフォルト値をマージ
        return ColorConfig(
            color=config.get('color', default.color),
            background=config.get('background', default.background),
            style=config.get('style', default.style)
        )
    
    def apply_color(self, text: str, config: ColorConfig) -> str:
        """テキストに色を適用"""
        if not any([config.color, config.background, config.style]):
            return text
        
        # 各エスケープシーケンスを取得
        style = Colors.get_color(config.style) if config.style else ''
        color = Colors.get_color(config.color) if config.color else ''
        background = Colors.get_color(f'bg_{config.background}') if config.background else ''
        
        # エスケープシーケンスを結合して適用（順番が重要）
        if any([style, color, background]):
            # 1. リセット
            # 2. 背景色
            # 3. 文字色
            # 4. スタイル
            # 5. テキスト
            # 6. リセット
            return f"\033[0m{background}{color}{style}{text}\033[0m"
        
        return text

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
    """カラー対応のカスタムFormatter"""
    
    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None,
                 color_config: Optional[Union[str, Path]] = None):
        """
        Args:
            fmt: フォーマット文字列
            datefmt: 日付フォーマット文字列
            color_config: 色設定ファイルのパス
        """
        self.default_filename_width = 6
        self.current_filename_width = self.default_filename_width
        self._base_fmt = '%(asctime)s,%(msecs)03d %(levelname)-5s | %(filename){}s:%(lineno)3d | %(message)s'
        
        super().__init__(
            fmt or self._base_fmt.format(self.current_filename_width),
            datefmt or '%Y-%m-%d %H:%M:%S'
        )
        
        # 色設定を読み込む
        self.color_manager = ColorManager(color_config)
    
    def update_format(self, filename_width: int) -> None:
        """フォーマット文字列を更新"""
        self._fmt = self._base_fmt.format(filename_width)
        self.current_filename_width = filename_width
    
    def format(self, record: LogRecord) -> str:
        # ファイル名の長さをチェックして必要に応じてフォーマットを更新
        filename_length = len(record.filename)
        if filename_length > self.current_filename_width:
            self.update_format(filename_length)
        
        # 元のレベル名とメッセージを保存
        original_levelname = record.levelname
        original_msg = record.msg
        
        # レベル名を5文字に調整（4文字の場合は右パディング）
        level_map = {
            logging.DEBUG: "DEBUG",    # 5文字
            logging.INFO: "INFO ",     # 4文字+パディング
            logging.WARNING: "WARN ",  # 4文字+パディング
            logging.ERROR: "ERROR",    # 5文字
            logging.CRITICAL: "CRIT "  # 4文字+パディング
        }
        record.levelname = level_map.get(record.levelno, record.levelname[:5].ljust(5))
        
        # 各部分の色設定を取得
        level_config = self.color_manager.get_level_color(record.levelno)
        msg_config = self.color_manager.get_message_color(record.levelno)
        timestamp_config = self.color_manager.get_element_color('timestamp')
        filename_config = self.color_manager.get_element_color('filename')
        
        # タイムスタンプ部分を色付け
        timestamp = self.formatTime(record, self.datefmt)
        msecs = int(record.msecs)  # floatをintに変換
        colored_timestamp = self.color_manager.apply_color(
            f"{timestamp},{msecs:03d}",
            timestamp_config
        )
        
        # レベル名を色付け
        colored_levelname = self.color_manager.apply_color(record.levelname, level_config)
        
        # ファイル名と行番号を色付け
        filename_info = f"{record.filename:>{self.current_filename_width}}:{record.lineno:3d}"
        colored_filename = self.color_manager.apply_color(filename_info, filename_config)
        
        # メッセージを色付け
        colored_msg = self.color_manager.apply_color(str(record.msg), msg_config)
        
        # 各部分を結合
        formatted = f"{colored_timestamp} {colored_levelname} | {colored_filename} | {colored_msg}"
        
        # 元の値を復元
        record.levelname = original_levelname
        record.msg = original_msg
        
        # 最後にリセットコードを追加
        return f"{Colors.RESET}{formatted}{Colors.RESET}"

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

class KissLogger(logging.Logger):
    """KISSLOGの拡張ロガー"""
    
    def __init__(self, name: str, level: int = logging.NOTSET):
        """
        Args:
            name: ロガー名
            level: ログレベル
        """
        super().__init__(name, level)
        self._path_shortener = None

    def enable_path_shortening(self, max_components: int = 2):
        """パスの短縮表示を有効にする

        Args:
            max_components (int): パスの最後から何個のコンポーネントを表示するか
        """
        if self._path_shortener:
            self.removeFilter(self._path_shortener)
        
        self._path_shortener = PathShortenerFilter()
        self.addFilter(self._path_shortener)

    def disable_path_shortening(self):
        """パスの短縮表示を無効にする"""
        if self._path_shortener:
            self.removeFilter(self._path_shortener)
            self._path_shortener = None

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
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        fmt='%(asctime)s,%(msecs)03d %(levelname)-5s | %(filename)s:%(lineno)3d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(handler)

# バージョン情報
__version__ = '0.1.0'
