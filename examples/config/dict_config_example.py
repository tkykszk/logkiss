#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LOGKISSのconfigモジュールとdictConfig機能を使用するサンプル

このスクリプトでは、標準logging.config.dictConfigに類似した
形式でLOGKISSの設定を行う方法を示します。
"""

import sys
from pathlib import Path

# ルートディレクトリをパスに追加して、logkissをインポートできるようにする
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# dictConfig機能はまだ実装されていない未来の機能なので、
# 現時点では以下のコードは実際には動作しません
# このサンプルコードは将来の仕様変更の参考です

# 将来的なインポート
import logging
import logkiss
# import logkiss.config  # 将来的に追加される予定


def main():
    # 将来の機能: dictConfigで設定する例
    # 以下は標準のlogging.config.dictConfigに似た形式
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'kiss_config': {
            'levels': {
                'debug': {
                    'color': 'cyan',
                    'style': 'bold'
                },
                'info': {
                    'color': 'green',
                    'style': 'bold'
                },
                'warning': {
                    'color': 'yellow',
                    'style': 'bold'
                },
                'error': {
                    'color': 'white',
                    'background': 'red',
                    'style': 'bold'
                },
                'critical': {
                    'color': 'white',
                    'background': 'bright_magenta',
                    'style': ['bold', 'blink']
                }
            },
            'messages': {
                'debug': {'color': 'cyan'},
                'info': {'color': 'green'},
                'warning': {'color': 'yellow'},
                'error': {'color': 'red', 'style': 'bold'},
                'critical': {'color': 'bright_red', 'style': 'bold'}
            },
            'elements': {
                'timestamp': {'color': 'blue', 'style': 'dim'},
                'filename': {'color': 'bright_green', 'style': 'underline'},
                'lineno': {'color': 'bright_yellow'}
            }
        },
        'formatters': {
            'kiss_default': {
                '()': 'logkiss.ColoredFormatter',
                'fmt': '%(asctime)s %(levelname)s | %(filename)s:%(lineno)d | %(message)s',
                'use_color': True
            },
            'kiss_detailed': {
                '()': 'logkiss.ColoredFormatter',
                'fmt': '[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d] - %(name)s - %(message)s',
                'use_color': True
            }
        },
        'handlers': {
            'console': {
                '()': 'logkiss.KissConsoleHandler',
                'level': 'DEBUG',
                'formatter': 'kiss_default'
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'kiss_detailed',
                'filename': 'application.log',
                'mode': 'a'
            },
            'rotating_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'WARNING',
                'formatter': 'kiss_detailed',
                'filename': 'warnings.log',
                'mode': 'a',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'loggers': {
            'app': {
                'level': 'DEBUG',
                'handlers': ['console', 'file'],
                'propagate': False
            },
            'app.errors': {
                'level': 'ERROR',
                'handlers': ['console', 'rotating_file'],
                'propagate': False
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console']
        }
    }
    
    print("将来的なdictConfigの使用例:")
    print("=" * 60)
    print("設定内容:")
    print_nested_dict(config)
    print()
    
    # 将来的にはこのようなコードで設定を適用する
    # logkiss.config.dictConfig(config)
    
    # 現時点での代替方法:
    print("現在の代替方法:")
    print("=" * 60)
    
    # ロガーを取得
    logger = logkiss.getLogger("app")
    
    # ログメッセージの出力
    print("\nログ出力例:")
    print("-" * 60)
    logger.debug("デバッグメッセージ")
    logger.info("情報メッセージ")
    logger.warning("警告メッセージ")
    logger.error("エラーメッセージ")
    
    # エラー例外付きログの出力
    try:
        1/0
    except ZeroDivisionError:
        logger.exception("ゼロ除算エラーが発生しました")


def print_nested_dict(d, indent=0):
    """ネストされた辞書を整形して出力する補助関数"""
    for key, value in d.items():
        if isinstance(value, dict):
            print(' ' * indent + str(key) + ':')
            print_nested_dict(value, indent + 2)
        else:
            print(' ' * indent + str(key) + ': ' + str(value))


if __name__ == "__main__":
    main()
