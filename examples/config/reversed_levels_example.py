#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
反転表示されたログレベル名の設定を使用するサンプル

このスクリプトは、reversed_levels.yamlの設定を使用して
すべてのログレベル名を反転表示する例を示します。
"""

import sys
from pathlib import Path

# ルートディレクトリをパスに追加して、logkissをインポートできるようにする
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import logkiss


def main():
    # 現在のディレクトリの設定ファイルへのパスを取得
    current_dir = Path(__file__).parent
    config_path = current_dir / "reversed_levels.yaml"

    print(f"使用する設定ファイル: {config_path}")
    print("=" * 60)

    # 標準のロガーを取得して比較のためのメッセージを出力
    print("標準設定のロガー出力例:")
    standard_logger = logkiss.getLogger("標準設定")

    # ログレベルをDEBUGに設定して全メッセージを表示
    standard_logger.setLevel(logkiss.logging.DEBUG)

    standard_logger.debug("DEBUGメッセージ（標準設定）")
    standard_logger.info("INFOメッセージ（標準設定）")
    standard_logger.warning("WARNINGメッセージ（標準設定）")
    standard_logger.error("ERRORメッセージ（標準設定）")
    standard_logger.critical("CRITICALメッセージ（標準設定）")

    print("\n" + "-" * 60)
    print("反転表示レベル設定の適用:")

    # 設定ファイルを読み込み適用
    try:
        root_logger = logkiss.setup_from_yaml(config_path)
        # ルートロガーもDEBUGレベルに設定
        root_logger.setLevel(logkiss.logging.DEBUG)
        print("反転表示設定を適用しました（ログレベル: DEBUG）")
    except Exception as e:
        print(f"設定の適用に失敗しました: {e}")
        return

    # 反転表示設定を使用したロガー
    reversed_logger = logkiss.getLogger("反転表示")

    # ログレベルをDEBUGに設定して全メッセージを表示
    reversed_logger.setLevel(logkiss.logging.DEBUG)

    print("\n反転表示設定のロガー出力例:")
    reversed_logger.debug("DEBUGメッセージ（反転表示設定）")
    reversed_logger.info("INFOメッセージ（反転表示設定）")
    reversed_logger.warning("WARNINGメッセージ（反転表示設定）")
    reversed_logger.error("ERRORメッセージ（反転表示設定）")
    reversed_logger.critical("CRITICALメッセージ（反転表示設定）")

    print("\n" + "=" * 60)
    print("追加テスト: 例外出力")
    try:
        # エラーを意図的に発生させる
        _ = 10 / 0
    except ZeroDivisionError:
        reversed_logger.exception("ゼロ除算エラーが発生しました")


if __name__ == "__main__":
    main()
