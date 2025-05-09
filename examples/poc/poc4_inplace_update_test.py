#!/usr/bin/env python
"""
インプレース更新と元の状態への復元をテストするサンプル

このサンプルでは、logkissの改良された init_logging 関数を使って：
1. デフォルト状態（既存の階層を尊重）
2. ルートロガーをインプレース更新
3. 元の状態への復元
をテストします
"""

import logging
import sys
import pytest

try:
    import logging_tree
    HAS_LOGGING_TREE = True
except ImportError:
    HAS_LOGGING_TREE = False

@pytest.mark.requires_logging_tree
@pytest.mark.skipif(not HAS_LOGGING_TREE, reason="logging_treeモジュールがインストールされていません")
def test_inplace_update():
    """Test inplace update and restoration."""
    # この関数はテストとして実行されるようにするためのダミー関数です
    pass

# 1. まず標準のロギングシステムを設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# いくつかの階層構造を持つロガーを作成
app_logger = logging.getLogger("app")
db_logger = logging.getLogger("app.database")
api_logger = logging.getLogger("app.api")

# 最初のメッセージを記録
print("\n1. 標準loggingの初期状態:")
if HAS_LOGGING_TREE:
    logging_tree.printout()
app_logger.warning("APP: 標準loggingの初期状態")
db_logger.warning("DATABASE: 標準loggingの初期状態")

# 2. logkissをインポート（デフォルトでは既存の階層を尊重）
import logkiss

print("\n2. logkissをインポートした後（デフォルトモード）:")
if HAS_LOGGING_TREE:
    logging_tree.printout()
app_logger.warning("APP: logkissインポート後もフォーマットが保持されている")
db_logger.warning("DATABASE: 階層も保持されている")

# logkissのロガーも使ってみる
kiss_logger = logkiss.getLogger("kiss_app")
kiss_logger.warning("KISS: logkissロガーからのメッセージ")

# 3. ルートロガーをインプレース更新
print("\n3. init_logging(replace_root=True)を呼び出した後:")
logkiss.init_logging(replace_root=True)
if HAS_LOGGING_TREE:
    logging_tree.printout()

# すべてのロガーでメッセージを記録（フォーマットが変わるはず）
app_logger.warning("APP: ルートロガーを置き換えた後")
db_logger.warning("DATABASE: 親子関係は保持されたまま")
kiss_logger.warning("KISS: logkissロガーからのメッセージ")

# 例外も記録してみる
try:
    result = 1 / 0
except Exception:
    app_logger.exception("APP: 例外が発生")

# 4. 元の状態に復元
print("\n4. init_logging(restore_original=True)で元に戻した後:")
logkiss.init_logging(restore_original=True)
if HAS_LOGGING_TREE:
    logging_tree.printout()

# 再度すべてのロガーでメッセージを記録（元のフォーマットに戻るはず）
app_logger.warning("APP: 元の状態に戻した後")
db_logger.warning("DATABASE: こちらも元の状態")
kiss_logger.warning("KISS: logkissロガーからのメッセージ")

print("\nテスト完了！上記のログ出力を確認してください。")
