#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LOGKISSのカスタム設定ファイルのテスト例

このスクリプトは、カスタム設定ファイル（funky_colors.yaml）を使用して
LOGKISSロガーをカスタマイズする方法を示します。
"""

import sys
from pathlib import Path

# ルートディレクトリをパスに追加して、logkissをインポートできるようにする
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import logkiss
import logging


def main():
    # 現在のディレクトリの設定ファイルへのパスを取得
    current_dir = Path(__file__).parent
    config_path = current_dir / "funky_colors.yaml"
    
    print(f"使用する設定ファイル: {config_path}")
    print("=" * 60)
    
    # 標準のロガーを取得して比較のためのメッセージを出力
    standard_logger = logkiss.getLogger("標準ロガー")
    standard_logger.info("これは標準の設定を使用したメッセージです")
    standard_logger.warning("これは標準の設定を使用した警告です")
    standard_logger.error("これは標準の設定を使用したエラーです")
    
    print("\n" + "-" * 60)
    print("カスタム設定ファイルを使用したロガーのテスト:")
    
    # 方法1: setup_from_yamlを使用して設定を読み込む
    # この方法では、ルートロガーの設定が変更されます
    root_logger = logkiss.setup_from_yaml(config_path)
    root_logger.info("ルートロガーにカスタム設定が適用されました")
    
    # カスタム設定を適用した後に作成する新しいロガーにも設定が反映される
    custom_logger = logkiss.getLogger("カスタムロガー")
    
    # 各種ログレベルでメッセージを出力
    custom_logger.debug("カスタム設定のDEBUGメッセージ - マゼンタ色のイタリック体になるはずです")
    custom_logger.info("カスタム設定のINFOメッセージ - シアン色の下線付きになるはずです")
    custom_logger.warning("カスタム設定のWARNメッセージ - 黄色の点滅になるはずです")
    custom_logger.error("カスタム設定のERRORメッセージ - 赤色の取り消し線になるはずです")
    custom_logger.critical("カスタム設定のCRITICALメッセージ - 白背景に赤の反転になるはずです")
    
    print("\n" + "-" * 60)
    print("スタックトレース付きのエラーを表示（カスタム設定）:")
    
    try:
        # エラーを意図的に発生させる
        _ = 10 / 0
    except ZeroDivisionError:
        custom_logger.exception("ゼロ除算エラーが発生しました")
    
    print("\n" + "=" * 60)
    print("異なるフォーマットのテスト:")
    
    # 方法2: 個別のロガーにカスタムハンドラーとフォーマッターを設定する
    # カスタムフォーマットとカスタム設定の組み合わせ
    formatter = logkiss.ColoredFormatter(
        fmt="%(asctime)s [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s",
        use_color=True
    )
    
    # ハンドラーを作成して、フォーマッターを設定
    handler = logkiss.KissConsoleHandler()
    handler.setFormatter(formatter)
    
    # 新しいロガーを作成し、すべてのハンドラーをクリアして、カスタムハンドラーを追加
    format_logger = logkiss.getLogger("フォーマットテスト")
    format_logger.handlers.clear()
    format_logger.addHandler(handler)
    
    # カスタムフォーマットでログを出力
    format_logger.info("カスタムフォーマットとカスタム色の組み合わせ")
    format_logger.warning("カスタムフォーマットの警告メッセージ")
    format_logger.error("カスタムフォーマットのエラーメッセージ")
    
    print("\n" + "=" * 60)
    print("設定のリロードテスト:")
    
    # 方法3: 設定のリロード（既存のロガーの設定を更新する場合）
    if hasattr(root_logger, "reload_config"):
        root_logger.reload_config()
        root_logger.info("設定がリロードされました")
    else:
        print("このバージョンのlogkissではreload_configメソッドはサポートされていません")


if __name__ == "__main__":
    main()
